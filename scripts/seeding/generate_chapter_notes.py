import os
import sys
import django
import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from django.db.models import QuerySet
from main.models import Chapter, ChapterNote, Subject, Grade

# Configure Gemini API
# Provide your API key here or in environment variable GEMINI_API_KEY
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable is not set!")
    print("Please set it in your terminal or script before running this.")
    print("Example: set GEMINI_API_KEY=your_api_key_here")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Use rapid Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_note_with_gemini(chapter):
    """Generates an HTML string for the chapter note using Gemini."""
    prompt = f"""
    You are an expert educator. Write a high-quality, comprehensive, and engaging study note for the chapter '{chapter.name}' in the subject of '{chapter.subject.name}' for students.
    
    The output MUST be formatted as clean HTML. Do not wrap it in a markdown block like ```html.
    Use the following exact structure:
    <div class="chapter-note-container">
        <div class="note-content">
            <h3>Overview</h3>
            <p>[A detailed 2-3 paragraph overview of the chapter's core concepts]</p>
            
            <h3>Key Takeaways</h3>
            <ul>
                <li>[Important concept 1]</li>
                <li>[Important concept 2]</li>
                ...
            </ul>
        </div>
    </div>
    """
    
    try:
        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        # Strip potential markdown formatting if model didn't listen
        content = response.text.strip()
        if content.startswith("```html"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print(f"    [!] Rate Limit hit. Waiting 60 seconds...")
            time.sleep(60)
            return generate_note_with_gemini(chapter)  # Recursive retry
        print(f"    [!] Error generating note with Gemini: {e}")
        return None

def process_chapters(limit=None):
    chapters = Chapter.objects.all().order_by('id')
    if limit:
        chapters = chapters[:limit]
        
    total = chapters.count()
    print(f"Found {total} chapters to process. Fetching via Gemini API...")
    
    success_count = 0
    fail_count = 0
    
    for i, chapter in enumerate(chapters, 1):
        print(f"[{i}/{total}] Generating: {chapter.name} ({chapter.subject.name})")
        
        # Generation
        while True:
            html_content = generate_note_with_gemini(chapter)
            
            if html_content:
                note, created = ChapterNote.objects.update_or_create(
                    chapter=chapter,
                    defaults={'content': html_content}
                )
                success_count += 1
                print(f"  -> [OK] Successfully saved Gemini notes.")
                break
            else:
                # Check for rate limit error in log output (passed as None here but let's refine)
                # In practice, usually errors return None in the current function.
                # Let's improve generate_note_with_gemini to raise or return specific info.
                fail_count += 1
                print(f"  -> [FAIL] Skipping/Failed for this chapter.")
                break
            
        # Modest throttle to respect Gemini free-tier rate limits (15 RPM usually)
        time.sleep(5)

    print("\n--- Summary ---")
    print(f"Total processed: {total}")
    print(f"Gemini successful: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == '__main__':
    limit = None
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            pass
            
    try:
        process_chapters(limit)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
