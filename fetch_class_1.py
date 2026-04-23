import os
import django
import urllib.request
import urllib.parse
import re
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter

def get_best_video_id(query):
    query_encoded = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q=site:youtube.com+{query_encoded}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Find the first valid YouTube video ID from duckduckgo results
        match = re.search(r'v=([a-zA-Z0-9_-]{11})', html)
        if match:
            return match.group(1)
        
        # Sometime DDG formats links differently
        match2 = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', html)
        if match2:
            return match2.group(1)
            
    except Exception as e:
        pass
    return None

def fetch_class_1_videos():
    print("Starting exact YouTube fetch for Class 1 chapters using DDG...")
    chapters = Chapter.objects.filter(subject__grade__name='Class 1')
    total = chapters.count()
    
    success_count = 0
    for i, chap in enumerate(chapters, 1):
        query = f"cbse ncert class 1 {chap.subject.name} {chap.name} explanation"
        print(f"[{i:02d}/{total}] {chap.subject.name} - {chap.name[:20]}...", end=" ")
        
        video_id = get_best_video_id(query)
        if video_id:
            vid = chap.videos.first()
            if vid:
                vid.youtube_id = video_id
                vid.save()
                print(f"-> {video_id}")
                success_count += 1
            else:
                print("-> Error: No video object")
        else:
            print("-> Failed")
        
        # Be polite to duckduckgo
        time.sleep(1.5)
        
    print(f"\nComplete! Successfully fetched and updated {success_count} out of {total} videos.")
            
if __name__ == '__main__':
    fetch_class_1_videos()
