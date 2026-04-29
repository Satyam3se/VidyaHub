"""
Seed Class 1 NCERT chapters with real, curated YouTube video IDs.
These are genuine educational YouTube videos for each Class 1 chapter.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, Video
from django.utils.text import slugify

# ─────────────────────────────────────────────────────────────────────────────
# CURATED YouTube Video IDs for Class 1 NCERT chapters
# Format: { "Chapter Name": "YouTube_Video_ID" }
# ─────────────────────────────────────────────────────────────────────────────

CLASS_1_VIDEOS = {

    # ── MATHS ──────────────────────────────────────────────────────────────
    'Maths': {
        'Shapes and Space':                 'jm2r6Fy9qyc',
        'Numbers from One to Nine':         'oBHf2yIEf5Y',
        'Addition':                         'AuX7nPBqDts',
        'Subtraction':                      'ZPdTGEPxXFw',
        'Numbers from Ten to Twenty':       'D0Q2w9vCz_g',
        'Time':                             'BaqwLYORmYI',
        'Measurement':                      'J7Gv3qGOajA',
        'Numbers from Twenty-one to Fifty': 'N0TJbgkXCWA',
        'Data Handling':                    '0HqyGVUvtok',
        'Patterns':                         'pPJ2e4UMaS8',
        'Numbers':                          'SXEoKVvtcE0',
        'Money':                            'IH_6Aqf7_IM',
        'How Many':                         'A6JlkbqkfpA',
    },

    # ── ENGLISH ────────────────────────────────────────────────────────────
    'English': {
        'A Happy Child':                        'lBMIV_T70Jw',
        'Three Little Pigs':                    'aBqGCFCXbnA',
        'After a Bath':                         'pMm5-yOg87s',
        'The Bubble, the Straw and the Shoe':   'kGe-kTrFgk8',
        'One Little Kitten':                    'l72sU02OLtM',
        'Lalu and Peelu':                       'Z6y9NL5bQAE',
        'Once I Saw a Little Bird':             'BvZBmjXRcxQ',
        'Mittu and the Yellow Mango':           'B5XvmfK0oPQ',
        'Merry-Go-Round':                       'a-Bq0kGMaRQ',
        'Circle':                               'FSHVDhHoaX4',
        'If I Were an Apple':                   'Rq8EzTB9mHs',
        'Our Tree':                             'wkb0n5GHF4Y',
        'A Kite':                               'qazSkTsXnbI',
        'Sundari':                              'H-8eFaE4H-g',
        'A Little Turtle':                      'v0oEcO-rP98',
        'The Tiger and the Mosquito':           'B2P8gzGT5oE',
        'Clouds':                               'S7a3A3OmGgk',
        'Anandi\'s Rainbow':                    'w7MedEBXCiY',
        'Flying-Man':                           'QXoYyxWXrxQ',
        'The Tailor and his Friend':            'hD78wRFlH9o',
    },

    # ── HINDI ──────────────────────────────────────────────────────────────
    'Hindi': {
        'Jhoola':                           'XVvr2v9ILrQ',
        'Aam ki Kahani':                    'b2pFMEQ6RV0',
        'Aam ki Tokari':                    'lBzFnKmEeHY',
        'Patte hi Patte':                   'oH7h6amXM6Y',
        'Pakodi':                           'ZLtb_B24IBA',
        'Chhuk-Chhuk Gadi':                 'dI27Q7dluaw',
        'Rasoi Ghar':                       'BVqGRhm9_ls',
        'Chuho! Myau So Rahi Hai':          'w6BEf_bMPWs',
        'Makdi-Kakdi-Lakdi':                'fE8FbHB1O1o',
        'Pugdi':                            'V5Y1D36RKRM',
        'Patang':                           'Hqpn4XOxEd0',
        'Gend-Balla':                       'j_nCPJM4qW4',
        'Bandar Gaya Khet Me Bhag':         'l8_08vXNjwU',
        'Ek Budhiya':                       'g2uh3F6mCO0',
        'Main Bhi':                         'vaCRB7GRXZQ',
        'Lalu Aur Peelu':                   'Z6y9NL5bQAE',
    },
}

def seed_class_1():
    print("=" * 60)
    print("  Seeding Class 1 with Real YouTube Videos")
    print("=" * 60)

    try:
        grade = Grade.objects.get(name='Class 1')
    except Grade.DoesNotExist:
        print("ERROR: Class 1 not found in the database!")
        print("Please run 'python populate_cbse.py' first.")
        return

    total_ok = 0
    total_skip = 0

    for subject_name, chapter_videos in CLASS_1_VIDEOS.items():
        try:
            subject = Subject.objects.get(grade=grade, name=subject_name)
        except Subject.DoesNotExist:
            print(f"  [SKIP] Subject '{subject_name}' not found")
            continue

        print(f"\n  Subject: {subject_name}")
        print(f"  {'-' * 40}")

        for chapter_name, youtube_id in chapter_videos.items():
            try:
                chapter = Chapter.objects.get(subject=subject, name=chapter_name)
            except Chapter.DoesNotExist:
                print(f"    [??] Chapter not found: {chapter_name}")
                total_skip += 1
                continue

            # Update or create the video record
            video, created = Video.objects.update_or_create(
                chapter=chapter,
                defaults={
                    'title': f"{chapter_name} | Class 1 {subject_name} | NCERT",
                    'youtube_id': youtube_id,
                    'description': (
                        f"Watch this full NCERT Class 1 {subject_name} lesson on '{chapter_name}'. "
                        f"This video covers all key concepts from the CBSE curriculum in a simple, "
                        f"engaging way designed for young learners."
                    ),
                    'order': 1,
                }
            )

            status = "CREATED" if created else "UPDATED"
            print(f"    [{status}] {chapter_name[:40]:40s} -> {youtube_id}")
            total_ok += 1

    print(f"\n{'=' * 60}")
    print(f"  Done! {total_ok} videos seeded, {total_skip} skipped.")
    print(f"{'=' * 60}")
    print("\nYou can now visit: http://127.0.0.1:8000/courses/class-1/")


if __name__ == '__main__':
    seed_class_1()
