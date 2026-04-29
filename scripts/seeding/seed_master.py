import os
import sys
import django
import subprocess

# Set up path to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

def run_script(script_path):
    print(f"\n--- Running {script_path} ---")
    try:
        # Run using current python interpreter
        # We use subprocess to avoid issues with django.setup() being called multiple times in same process
        subprocess.run([sys.executable, os.path.join(BASE_DIR, script_path)], check=True)
    except Exception as e:
        print(f"Error running {script_path}: {e}")

scripts = [
    'scripts/seeding/populate_cbse.py', # Important: Create Grades and Chapters first
    'scripts/seeding/seed_all_class1.py',
    'scripts/seeding/seed_all_class2.py',
    'scripts/seeding/generate_unique_class3_mcqs.py',
    'scripts/seeding/generate_unique_class4_mcqs.py',
    'scripts/seeding/generate_unique_class5_mcqs.py',
    'scripts/seeding/generate_unique_class6_mcqs.py',
    'scripts/seeding/generate_unique_class7_mcqs.py',
    'scripts/seeding/generate_unique_class8_mcqs.py',
    'scripts/seeding/generate_unique_class9_mcqs.py',
    'scripts/seeding/generate_unique_class10_mcqs.py',
    'scripts/seeding/add_jee_mcqs.py',
    'scripts/seeding/add_neet_mcqs.py',
    'scripts/seeding/add_nda_pyqs.py',
    'scripts/seeding/fetch_youtube_videos.py', # ADDED: Get real videos for all chapters
    'scripts/seeding/seed_chapter_notes.py',   # ADDED: Get notes for all chapters
    'scripts/seeding/seed_achievements.py',
]


if __name__ == "__main__":
    print("Starting Master Seeding Process...")
    for script in scripts:
        run_script(script)
    print("\nAll seeding complete!")
