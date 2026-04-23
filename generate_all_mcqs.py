"""
Generate MCQs for ALL chapters using GROQ API
Usage: python generate_all_mcqs.py [--limit N] [--grade CLASS]
"""
import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

import django
import json
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion
from django.conf import settings

GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', os.getenv('GROQ_API_KEY'))
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

print("=" * 60)
print("VidyaHub - Generate All Chapter MCQs")
print("=" * 60)


def generate_with_groq(prompt, retries=3, delay=15):
    for attempt in range(retries):
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
                timeout=120
            )

            if response.status_code == 429:
                wait_time = delay * (attempt + 1)
                print(f"  [!] Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            if attempt < retries - 1:
                wait_time = delay * (attempt + 1)
                print(f"  [!] Error: {e}, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  [!] Groq API error: {e}")
                return None
    return None


def parse_questions(text):
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


def get_prompt(chapter, grade_name):
    return f"""Generate exactly 20 MCQ quiz questions for the chapter "{chapter.name}" from {chapter.subject.name} (Grade: {grade_name}).

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


def seed_chapter(chapter, force=False, delay=2):
    existing = MCQQuestion.objects.filter(chapter=chapter).count()
    if existing > 0 and not force:
        return None

    grade_name = chapter.subject.grade.name
    print(f"\n[{chapter.subject.grade.name}] {chapter.subject.name}: {chapter.name}")
    print(f"  -> Generating {20 if existing == 0 else existing} MCQs...")

    prompt = get_prompt(chapter, grade_name)
    text = generate_with_groq(prompt)

    if not text:
        print(f"  [!] Failed to get response")
        return None

    data = parse_questions(text)
    if not data or 'questions' not in data:
        print(f"  [!] Could not parse questions")
        return None

    questions = data['questions']
    if not questions:
        print(f"  [!] No questions in response")
        return None

    MCQQuestion.objects.filter(chapter=chapter).delete()
    created = 0

    for i, q in enumerate(questions[:20]):
        try:
            MCQQuestion.objects.create(
                chapter=chapter,
                question_text=q.get('question', ''),
                option_a=q.get('option_a', ''),
                option_b=q.get('option_b', ''),
                option_c=q.get('option_c', ''),
                option_d=q.get('option_d', ''),
                correct_option=q.get('correct_option', 'A'),
                explanation=q.get('explanation', ''),
                order=i
            )
            created += 1
        except Exception as e:
            print(f"  [!] Error creating Q{i+1}: {e}")

    print(f"  ✓ Created {created} questions")
    time.sleep(delay)
    return created


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Regenerate even if questions exist')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of chapters')
    parser.add_argument('--grade', type=str, default='', help='Filter by grade')
    parser.add_argument('--delay', type=int, default=2, help='Delay between API calls')
    args = parser.parse_args()

    chapters = Chapter.objects.all().order_by('subject__grade__order', 'subject__name', 'order')

    if args.grade:
        chapters = chapters.filter(subject__grade__name__icontains=args.grade)

    total = chapters.count()
    print(f"\nTotal chapters: {total}")

    to_process = []
    for ch in chapters:
        count = ch.mcqs.count()
        if args.force or count == 0:
            to_process.append(ch)

    print(f"Chapters needing MCQs: {len(to_process)}")

    if args.limit > 0:
        to_process = to_process[:args.limit]
        print(f"Processing first {args.limit} chapters...")

    if not to_process:
        print("All chapters already have MCQs!")
        return

    print(f"\nStarting generation... (delay: {args.delay}s)")
    success = 0

    for i, ch in enumerate(to_process, 1):
        print(f"\n[{i}/{len(to_process)}]", end=" ")
        result = seed_chapter(ch, force=args.force, delay=args.delay)
        if result:
            success += 1

    print("\n" + "=" * 60)
    print(f"Done! Generated MCQs for {success} chapters")
    print("=" * 60)


if __name__ == '__main__':
    main()