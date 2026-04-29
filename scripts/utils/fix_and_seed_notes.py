import os
import django
import json
import time
import requests
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, ChapterNote, Grade

GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', os.getenv('GROQ_API_KEY'))
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_html_notes(chapter, model="llama-3.3-70b-versatile"):
    """Generate high-quality HTML study notes for a chapter."""
    prompt = f"""
    You are 'Vidya AI', an expert educator. Write a high-quality, comprehensive, and engaging study note for the chapter '{chapter.name}' in the subject of '{chapter.subject.name}' (Grade: {chapter.subject.grade.name}).
    
    The output MUST be formatted as clean HTML. Do NOT wrap it in markdown blocks like ```html.
    
    Structure requirements:
    1. Use <div class="chapter-note-container"> as the root.
    2. Include an 'Overview' section with 2-3 paragraphs.
    3. Include a 'Key Concepts' section with a bulleted list.
    4. CRITICAL: For each item in the 'Key Concepts' list, append a clarify icon at the end of the text like this: 
       `<span class="clarify-icon" onclick="window.openVidyaAI('Tell me more about [Concept Name] in the context of {chapter.name}')"><i data-lucide="help-circle"></i></span>`
    5. Include a 'Detailed Breakdown' section with subheadings (h4) for major topics.
    6. Include a 'Study Tips' section with 3-4 actionable tips.
    7. Use premium educational tone: encouraging, clear, and insightful.
    """
    
    try:
        response = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a specialized educational content creator. Return ONLY clean HTML."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 2500
            },
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"  [!] Groq Error: {response.status_code} - {response.text}")
            return None
            
        html_content = response.json()['choices'][0]['message']['content'].strip()
        
        # Strip potential markdown backticks
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        elif html_content.startswith("```"):
            html_content = html_content[3:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
            
        return html_content.strip()
        
    except Exception as e:
        print(f"  [!] Exception: {e}")
        return None

def generate_html_notes_gemini(chapter):
    """Generate high-quality HTML study notes using Gemini."""
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""
    You are 'Vidya AI', an expert educator. Write a high-quality, comprehensive, and engaging study note for the chapter '{chapter.name}' in the subject of '{chapter.subject.name}' (Grade: {chapter.subject.grade.name}).
    
    The output MUST be formatted as clean HTML. Do NOT wrap it in markdown blocks like ```html.
    
    Structure requirements:
    1. Use <div class="chapter-note-container"> as the root.
    2. Include an 'Overview' section with 2-3 paragraphs.
    3. Include a 'Key Concepts' section with a bulleted list.
    4. CRITICAL: For each item in the 'Key Concepts' list, append a clarify icon at the end of the text like this: 
       `<span class="clarify-icon" onclick="window.openVidyaAI('Tell me more about [Concept Name] in the context of {chapter.name}')"><i data-lucide="help-circle"></i></span>`
    5. Include a 'Detailed Breakdown' section with subheadings (h4) for major topics.
    6. Include a 'Study Tips' section with 3-4 actionable tips.
    7. Use premium educational tone: encouraging, clear, and insightful.
    """
    
    model_names = [
        'gemini-2.0-flash',
        'gemini-flash-latest',
        'models/gemini-2.0-flash',
        'models/gemini-flash-latest',
        'gemini-1.5-flash', 
        'gemini-1.5-flash-latest'
    ]
    
    for m_name in model_names:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            if not response.candidates or not response.candidates[0].content.parts:
                continue
                
            html_content = response.text.strip()
            
            # Strip potential markdown backticks
            if html_content.startswith("```html"):
                html_content = html_content[7:]
            elif html_content.startswith("```"):
                html_content = html_content[3:]
            if html_content.endswith("```"):
                html_content = html_content[:-3]
                
            return html_content.strip()
        except Exception as e:
            print(f"  [!] Gemini ({m_name}) Error: {e}")
            continue
            
    return None

def generate_html_notes_openai(chapter):
    """Generate high-quality HTML study notes using OpenAI."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        prompt = f"""
        You are 'Vidya AI', an expert educator. Write a high-quality, comprehensive, and engaging study note for the chapter '{chapter.name}' in the subject of '{chapter.subject.name}' (Grade: {chapter.subject.grade.name}).
        
        The output MUST be formatted as clean HTML. Do NOT wrap it in markdown blocks like ```html.
        
        Structure requirements:
        1. Use <div class="chapter-note-container"> as the root.
        2. Include an 'Overview' section with 2-3 paragraphs.
        3. Include a 'Key Concepts' section with a bulleted list.
        4. CRITICAL: For each item in the 'Key Concepts' list, append a clarify icon at the end of the text like this: 
           `<span class="clarify-icon" onclick="window.openVidyaAI('Tell me more about [Concept Name] in the context of {chapter.name}')"><i data-lucide="help-circle"></i></span>`
        5. Include a 'Detailed Breakdown' section with subheadings (h4) for major topics.
        6. Include a 'Study Tips' section with 3-4 actionable tips.
        7. Use premium educational tone: encouraging, clear, and insightful.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a specialized educational content creator. Return ONLY clean HTML."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        html_content = response.choices[0].message.content.strip()
        
        # Strip potential markdown backticks
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        elif html_content.startswith("```"):
            html_content = html_content[3:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
            
        return html_content.strip()
    except Exception as e:
        print(f"  [!] OpenAI Error: {e}")
        return None

def main():
    print("=" * 60)
    print("  VidyaHub - HTML Notes Generator (Class 1-10 Focus)")
    print("=" * 60)
    
    # Focus on Class 1-10
    grades = Grade.objects.filter(name__icontains='Class').exclude(name__in=['Class 11', 'Class 12']).order_by('id')
    
    for grade in grades:
        print(f"\n>>> Processing {grade.name}...")
        chapters = Chapter.objects.filter(subject__grade=grade).order_by('id')
        total = chapters.count()
        
        for idx, chapter in enumerate(chapters, 1):
            note = ChapterNote.objects.filter(chapter=chapter).first()
            
            # Check if we need to (re)generate (Upgrade to clarify-icons)
            needs_generation = False
            if not note:
                needs_generation = True
                status = "Missing"
            elif not note.content.strip().startswith('<'):
                needs_generation = True
                status = "Markdown (needs fix)"
            elif 'clarify-icon' not in note.content:
                needs_generation = True
                status = "Old HTML (needs upgrade)"
            
            if needs_generation:
                print(f"  [{idx}/{total}] {chapter.subject.name} > {chapter.name} ({status})...", end="", flush=True)
                
                html = generate_html_notes(chapter, "llama-3.3-70b-versatile")
                if not html:
                    print(" (Trying Groq 8B)...", end="", flush=True)
                    html = generate_html_notes(chapter, "llama-3.1-8b-instant")
                if not html:
                    print(" (Falling back to OpenAI)...", end="", flush=True)
                    html = generate_html_notes_openai(chapter)
                if not html:
                    print(" (Falling back to Gemini)...", end="", flush=True)
                    html = generate_html_notes_gemini(chapter)
                
                if html:
                    if note:
                        note.content = html
                        note.save()
                        print(" [UPDATED]")
                    else:
                        ChapterNote.objects.create(chapter=chapter, content=html)
                        print(" [CREATED]")
                    time.sleep(15) # Sleep 15s to stay under Gemini Free Tier RPM (5 RPM)
                else:
                    print(" [FAILED ALL PROVIDERS]")
                    time.sleep(5)
            else:
                pass

    print("\n" + "=" * 60)
    print("  Class 1-10 Progress Completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
