"""
VidyaHub - Chapter Notes Seeder
Generates study notes for each chapter using Groq/Ollama API
Usage: python seed_chapter_notes.py [--force] [--grade CLASS_NAME]
"""

import os
import sys
import django
import json
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, ChapterNote


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:7b"

PROMPT = """Generate detailed study notes for the chapter "{chapter_name}" from {subject_name} (Grade: {grade_name}).

Requirements:
1. Language: Simple, appropriate for {grade_name} students
2. Format: Return ONLY valid JSON:
{{
  "title": "Brief title",
  "key_concepts": ["concept 1", "concept 2", "concept 3"],
  "notes": "## Chapter Name\\n\\nDetailed markdown notes...",
  "tips": ["Study tip 1", "Study tip 2"]
}}

Return ONLY JSON."""

def parse_response(text):
    text = text.strip()
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0].strip()
    elif '```' in text:
        parts = text.split('```')
        text = parts[1] if len(parts) > 1 else parts[0]
        text = text.strip()
    try:
        return json.loads(text)
    except:
        return None

def generate_with_groq(prompt):
    try:
        response = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3, "max_tokens": 4000},
            timeout=60
        )
        res_data = response.json()
        if 'choices' in res_data:
            return res_data['choices'][0]['message']['content']
        else:
            print(f"  [!] Groq API Error: {res_data}")
            return None
    except Exception as e:
        print(f"  [!] Groq Exception: {e}")
        return None


def generate_with_ollama(prompt):
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.3, "num_predict": 3000}}, timeout=300)
        return response.json().get('response', '')
    except Exception as e:
        print(f"  [!] Ollama: {e}")
        return None

def generate_notes(chapter, force=False):
    if not force and ChapterNote.objects.filter(chapter=chapter).exists():
        print(f"  [=] Notes exist, skipping...")
        return False
    
    if force:
        ChapterNote.objects.filter(chapter=chapter).delete()
    
    prompt = PROMPT.format(chapter_name=chapter.name, subject_name=chapter.subject.name, grade_name=chapter.subject.grade.name)
    
    text = generate_with_groq(prompt)
    if not text:
        text = generate_with_ollama(prompt)
    
    data = None
    if text:
        data = parse_response(text)
    
    # FALLBACK: If AI fails, provide a structured template so the page isn't empty
    if not data:
        data = {
            'notes': f"""# {chapter.name}
            
## Introduction
Welcome to the study notes for **{chapter.name}** in {chapter.subject.name}. This chapter covers essential concepts required for your CBSE curriculum.

## Key Learning Objectives
* Understand the core principles of {chapter.name}.
* Master the practical applications of these concepts.
* Prepare for exam-style questions.

## Summary
Study material is being updated with AI-enhanced insights. In the meantime, please refer to your NCERT textbook for this chapter. 

*Stay tuned for interactive maps and deep-dives!*
"""
        }
    
    try:
        ChapterNote.objects.create(
            chapter=chapter,
            content=data.get('notes', f"# {chapter.name}\n\nStudy material coming soon.")
        )
        return True
    except Exception as e:
        print(f"  [!] Database Error: {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--grade', type=str)
    parser.add_argument('--chapter-id', type=int)
    args = parser.parse_args()
    
    print("=" * 60)
    print("  VidyaHub - Chapter Notes Seeder")
    print("=" * 60)
    
    chapters = Chapter.objects.all()
    if args.chapter_id:
        chapters = chapters.filter(id=args.chapter_id)
    elif args.grade:
        chapters = chapters.filter(subject__grade__name__icontains=args.grade)
    
    chapters = list(chapters.select_related('subject', 'subject__grade'))
    
    total = len(chapters)
    created = 0
    
    for idx, chapter in enumerate(chapters, 1):
        print(f"[{idx}/{total}] {chapter.subject.grade.name} > {chapter.subject.name} > {chapter.name}")
        if generate_notes(chapter, force=args.force):
            created += 1
            print(f"  [OK] Notes created")
        time.sleep(0.5)
    
    print(f"\n{'='*60}\n  Created {created} notes for {total} chapters\n{'='*60}")

if __name__ == '__main__':
    main()