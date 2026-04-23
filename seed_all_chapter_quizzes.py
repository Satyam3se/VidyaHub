"""
VidyaHub - Comprehensive Chapter Quiz Seeder
Generates 20 MCQ questions per chapter using Ollama/Groq API
Usage: python seed_all_chapter_quizzes.py [--force] [--grade CLASS_NAME] [--subject SUBJECT_NAME]
"""

import os
import sys
import django
import json
import time
import re
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion
from django.conf import settings

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:7b"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

PROMPT_TEMPLATE = """Generate exactly 20 MCQ quiz questions for the chapter "{chapter_name}" from {subject_name} (Grade: {grade_name}).

Requirements:
1. Each question must test a different concept from the chapter
2. Language: Simple, appropriate for {grade_name} students
3. Options should be plausible but only ONE correct
4. Return ONLY valid JSON in this exact format:

{{
  "questions": [
    {{
      "question": "Question text here?",
      "option_a": "First option",
      "option_b": "Second option",
      "option_c": "Third option",
      "option_d": "Fourth option",
      "correct_option": "A",
      "explanation": "Brief explanation for why this is correct"
    }}
  ]
}}

Generate all 20 questions now. Return ONLY the JSON."""

PROMPT_CLASS_1_2 = """Generate 20 simple MCQ quiz questions for the chapter "{chapter_name}" from {subject_name} (Grade: {grade_name}).

Requirements:
1. Use VERY SIMPLE language for young children (ages 6-8)
2. Questions should be about basic concepts, counting, shapes, colors, etc.
3. Make options short and clear (1-3 words each)
4. Only ONE correct answer
5. Return ONLY valid JSON:

{{
  "questions": [
    {{
      "question": "Simple question ending with ?",
      "option_a": "Option A",
      "option_b": "Option B",
      "option_c": "Option C",
      "option_d": "Option D",
      "correct_option": "A",
      "explanation": "Simple one-line explanation"
    }}
  ]
}}

Generate all 20 questions now. Return ONLY the JSON."""

NOTE_PROMPT = """Generate detailed study notes for the chapter "{chapter_name}" from {subject_name} (Grade: {grade_name}).

Requirements:
1. Language: Simple, appropriate for {grade_name} students
2. Format: Return ONLY valid JSON with this structure:
{{
  "title": "Brief title for the chapter",
  "key_concepts": ["concept 1", "concept 2", "concept 3"],
  "notes": "Detailed markdown-formatted study notes covering all important topics",
  "tips": ["Study tip 1", "Study tip 2", "Study tip 3"]
}}

Return ONLY the JSON."""

def get_prompt(chapter_name, subject_name, grade_name):
    grade_num = int(re.search(r'\d+', grade_name).group()) if re.search(r'\d+', grade_name) else 6
    if grade_num <= 2:
        return PROMPT_CLASS_1_2.format(chapter_name=chapter_name, subject_name=subject_name, grade_name=grade_name)
    return PROMPT_TEMPLATE.format(chapter_name=chapter_name, subject_name=subject_name, grade_name=grade_name)

def parse_ai_response(text):
    text = text.strip()
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0].strip()
    elif '```' in text:
        parts = text.split('```')
        text = parts[1] if len(parts) > 1 else parts[0]
        text = text.strip()
    try:
        data = json.loads(text)
        if 'questions' in data:
            return data['questions']
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return None

def parse_note_response(text):
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
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        print(f"  [!] Groq failed: {e}")
        return None

def generate_with_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 3000}
            },
            timeout=300
        )
        response.raise_for_status()
        return response.json().get('response', '')
    except Exception as e:
        print(f"  [!] Ollama failed: {e}")
        return None

def generate_questions(chapter, force=False):
    existing_count = MCQQuestion.objects.filter(chapter=chapter).count()
    if not force and existing_count >= 20:
        print(f"  [=] Chapter already has {existing_count} questions, skipping...")
        return 0
    
    if force:
        MCQQuestion.objects.filter(chapter=chapter).delete()
        print(f"  [X] Deleted existing questions")
    
    prompt = get_prompt(chapter.name, chapter.subject.name, chapter.subject.grade.name)
    
    text = generate_with_groq(prompt)
    if not text:
        text = generate_with_ollama(prompt)
    if not text:
        return 0
    
    questions_data = parse_ai_response(text)
    if not questions_data:
        return 0
    
    count = 0
    for i, q_data in enumerate(questions_data[:20]):
        try:
            MCQQuestion.objects.create(
                chapter=chapter,
                question_text=q_data.get('question', ''),
                option_a=q_data.get('option_a', ''),
                option_b=q_data.get('option_b', ''),
                option_c=q_data.get('option_c', ''),
                option_d=q_data.get('option_d', ''),
                correct_option=q_data.get('correct_option', 'A')[0].upper(),
                explanation=q_data.get('explanation', ''),
                order=i + 1
            )
            count += 1
        except Exception as e:
            continue
    
    return count

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Seed chapter quizzes')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--grade', type=str)
    parser.add_argument('--subject', type=str)
    parser.add_argument('--chapter-id', type=int)
    args = parser.parse_args()
    
    print("=" * 60)
    print("  VidyaHub - Chapter Quiz Seeder")
    print("  Using Groq API (primary) / Ollama (fallback)")
    print("=" * 60)
    
    chapters = Chapter.objects.all()
    
    if args.chapter_id:
        chapters = chapters.filter(id=args.chapter_id)
    else:
        if args.grade:
            chapters = chapters.filter(subject__grade__name__icontains=args.grade)
        if args.subject:
            chapters = chapters.filter(subject__name__icontains=args.subject)
    
    chapters = list(chapters.select_related('subject', 'subject__grade').order_by('subject__grade__order', 'subject__pk', 'order'))
    
    total = len(chapters)
    total_q = 0
    
    print(f"\nFound {total} chapters to process\n")
    
    for idx, chapter in enumerate(chapters, 1):
        print(f"[{idx}/{total}] {chapter.subject.grade.name} > {chapter.subject.name} > {chapter.name}")
        try:
            count = generate_questions(chapter, force=args.force)
            total_q += count
            if count > 0:
                print(f"  [OK] Added {count} questions")
            time.sleep(0.5)
        except Exception as e:
            print(f"  [ERROR] {e}")
            time.sleep(2)
    
    print(f"\n{'='*60}\n  COMPLETE: {total_q} questions for {total} chapters\n{'='*60}")

if __name__ == '__main__':
    main()