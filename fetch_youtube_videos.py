import os
import sys
import django
import urllib.request
import urllib.parse
import re
import json
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, Video

def search_youtube_video_id(query):
    """Search YouTube and extract the first video ID from search results."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(req, timeout=15)
        html = response.read().decode('utf-8')
        
        # YouTube embeds video data in a JSON object within the page
        # Look for videoId in the initial data
        matches = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
        if matches:
            # Return the first unique video ID (skip duplicates/ads)
            seen = set()
            for vid_id in matches:
                if vid_id not in seen:
                    seen.add(vid_id)
                    return vid_id
    except Exception as e:
        print(f"\n      [!] Search Error for '{query}': {e}")
    return None

def update_all_class_videos(class_name):
    """Update all chapters for a given class with real YouTube video IDs."""
    print(f"\n{'='*60}")
    print(f"  Processing {class_name}")
    print(f"{'='*60}")
    
    try:
        grade = Grade.objects.get(name=class_name)
    except Grade.DoesNotExist:
        print(f"ERROR: {class_name} not found in database!")
        return
    
    subjects = Subject.objects.filter(grade=grade)
    total_updated = 0
    total_failed = 0
    
    for subject in subjects:
        chapters = Chapter.objects.filter(subject=subject).order_by('order')
        print(f"\n  Subject: {subject.name} ({chapters.count()} chapters)")
        print(f"  {'-'*40}")
        
        for chap in chapters:
            # Customizing query based on grade type
            if class_name in ['JEE', 'NEET', 'NDA']:
                query = f"{class_name} {subject.name} {chap.name} one shot lecture Hindi"
            else:
                query = f"NCERT {class_name} {subject.name} {chap.name} full chapter explanation Hindi"
            
            vid_id = search_youtube_video_id(query)
            
            if vid_id:
                video = chap.videos.first()
                if video:
                    video.youtube_id = vid_id
                    video.title = f"{chap.name} - {subject.name} ({class_name})"
                    video.save()
                else:
                    Video.objects.create(
                        chapter=chap,
                        title=f"{chap.name} - {subject.name} ({class_name})",
                        youtube_id=vid_id,
                        description=f"CBSE {class_name} {subject.name}: {chap.name}",
                        order=1
                    )
                print(f"    [OK] {chap.name[:35]:35s} -> {vid_id}")
                total_updated += 1
            else:
                print(f"    [!!] {chap.name[:35]:35s} -> FAILED")
                total_failed += 1
            
            # Don't hammer YouTube - 2 seconds is usually safe
            time.sleep(1.5)
    
    print(f"\n  Results for {class_name}: {total_updated} updated, {total_failed} failed")
    return total_updated, total_failed

if __name__ == '__main__':
    # All supported grades
    classes_to_process = [
        'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5',
        'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10',
        'Class 11', 'Class 12', 'JEE', 'NEET', 'NDA'
    ]
    
    # If a specific class is passed as argument, only process that
    if len(sys.argv) > 1:
        class_arg = ' '.join(sys.argv[1:])
        classes_to_process = [class_arg]
    
    grand_total_ok = 0
    grand_total_fail = 0
    
    for cls in classes_to_process:
        ok, fail = update_all_class_videos(cls)
        grand_total_ok += ok
        grand_total_fail += fail
    
    print(f"\n{'='*60}")
    print(f"  GRAND TOTAL: {grand_total_ok} videos updated, {grand_total_fail} failed")
    print(f"{'='*60}")
