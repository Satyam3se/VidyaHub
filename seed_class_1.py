import os
import django
import sys

# Set up Django environment
sys.path.append('c:/VidyaHub')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

def seed_class_1_basics():
    print("🌱 Seeding Class 1 Fundamentals...")
    
    # 1. Create Grade
    grade, _ = Grade.objects.get_or_create(name='Class 1', slug='class-1', defaults={'order': 1})
    
    # 2. Create Subjects
    subjects_data = [
        {'name': 'Maths', 'slug': 'maths', 'icon': 'plus-circle'},
        {'name': 'English', 'slug': 'english', 'icon': 'languages'},
        {'name': 'Hindi', 'slug': 'hindi', 'icon': 'book-open'},
        {'name': 'EVS', 'slug': 'evs', 'icon': 'leaf'},
    ]
    
    subjects = {}
    for s_data in subjects_data:
        s, _ = Subject.objects.get_or_create(
            grade=grade, 
            slug=s_data['slug'], 
            defaults={'name': s_data['name'], 'icon': s_data['icon']}
        )
        subjects[s_data['name']] = s
        print(f"✅ Subject Created: {s_data['name']}")

    # 3. Create a "Basics" chapter for each to hold the first 30 questions
    for name, s_obj in subjects.items():
        Chapter.objects.get_or_create(
            subject=s_obj,
            slug='basics',
            defaults={'name': 'The Basics', 'order': 1}
        )
        print(f"✅ Chapter 'The Basics' created for {name}")

if __name__ == '__main__':
    seed_class_1_basics()
