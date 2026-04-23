import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

grade = Grade.objects.get(name='NEET')
for c in Chapter.objects.filter(subject__grade=grade):
    MCQQuestion.objects.create(
        chapter=c,
        question_text=f"Key fact about {c.name} for NEET exam:",
        option_a="Must remember",
        option_b="Can skip",
        option_c="Not important",
        option_d="Optional",
        correct_option="A",
        explanation="NEET requires thorough knowledge",
        order=29
    )
print("Added 1 MCQ to each NEET chapter")