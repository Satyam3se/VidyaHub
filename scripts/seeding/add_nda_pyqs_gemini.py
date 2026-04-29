import os
import sys
import django
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from main.models import Grade, Chapter, MCQQuestion

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable is not set!", flush=True)
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_mcqs_for_chapter(chapter_name, subject_name, count=15):
    prompt = f"""
    You are an expert exam creator for the Indian NDA (National Defence Academy) entrance exam.
    Generate EXACTLY {count} highly unique, syllabus-aligned Previous Year Question (PYQ) styled Multiple Choice Questions (MCQs) for the topic '{chapter_name}' in the subject of '{subject_name}'.
    Ensure even technical and complex concepts are covered. DO NOT provide any repetitive questions. Ensure all options are realistic and detailed.

    Return the result strictly as a valid JSON array of objects. Do not include markdown formatting or extra text outside the JSON block.
    Format of each object:
    [
      {{
        "q": "Question text here?",
        "a": "Option A text",
        "b": "Option B text",
        "c": "Option C text",
        "d": "Option D text",
        "ans": "A", 
        "exp": "Detailed explanation for the correct answer."
      }}
    ]
    """
    
    try:
        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        mcqs_data = json.loads(content.strip())
        return mcqs_data
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print(f"    [!] Rate Limit hit. Waiting 60 seconds...", flush=True)
            time.sleep(60)
            return generate_mcqs_for_chapter(chapter_name, subject_name, count)
        print(f"    [!] Error generating MCQs: {e}", flush=True)
        return None

def process_chapters():
    grade = Grade.objects.get(slug='nda')
    chapters = list(Chapter.objects.filter(subject__grade=grade).order_by('id'))
    total = len(chapters)
    
    print(f"Ensuring at least 15 unique MCQs each for {total} NDA chapters...", flush=True)
    
    for i, chapter in enumerate(chapters, 1):
        existing_count = MCQQuestion.objects.filter(chapter=chapter).count()
        if existing_count >= 15:
            print(f"[{i}/{total}] {chapter.subject.name} - {chapter.name} already has {existing_count} MCQs. Skipping.", flush=True)
            continue

        print(f"[{i}/{total}] {chapter.subject.name} - {chapter.name} (has {existing_count})...", flush=True)
        
        while True:
            mcqs_data = generate_mcqs_for_chapter(chapter.name, chapter.subject.name, 15)
            if mcqs_data and isinstance(mcqs_data, list) and len(mcqs_data) >= 15:
                # We overwrite the 5 placeholder ones with 15 high-quality ones
                MCQQuestion.objects.filter(chapter=chapter).delete()
                for order, q_data in enumerate(mcqs_data):
                    try:
                        ans = q_data['ans'].strip().upper()
                        if ans not in ['A', 'B', 'C', 'D']:
                            ans = 'A'
                        MCQQuestion.objects.create(
                            chapter=chapter,
                            question_text=q_data['q'],
                            option_a=q_data['a'],
                            option_b=q_data['b'],
                            option_c=q_data['c'],
                            option_d=q_data['d'],
                            correct_option=ans,
                            explanation=q_data.get('exp', ''),
                            order=order
                        )
                    except Exception as e:
                        print(f"      [!] Error saving a question: {e}", flush=True)
                print(f"  -> [OK] Successfully saved {len(mcqs_data)} high-quality NDA questions.", flush=True)
                break
            else:
                l = len(mcqs_data) if mcqs_data else 0
                print(f"  -> [RETRY] Failed to get 15 valid MCQs (got {l}). Retrying in 10s...", flush=True)
                time.sleep(10)
                
        # Small sleep to respect rate limits
        time.sleep(3)
        
    print("Done! All NDA chapters now have at least 15 unique MCQs.", flush=True)

if __name__ == '__main__':
    process_chapters()
