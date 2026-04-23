import os
import django
import time
from youtubesearchpython import VideosSearch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, Video

def fetch_class_1_videos():
    print("Starting YouTube fetch for Class 1 chapters using youtube-search-python...")
    chapters = Chapter.objects.filter(subject__grade__name='Class 1')
    total = chapters.count()
    
    success_count = 0
    for i, chap in enumerate(chapters, 1):
        query = f"cbse ncert class 1 {chap.subject.name} {chap.name} explanation"
        print(f"[{i:02d}/{total}] {chap.subject.name} - {chap.name[:20]}...", end=" ")
        
        try:
            videos_search = VideosSearch(query, limit = 1)
            results = videos_search.result()
            
            if results and 'result' in results and len(results['result']) > 0:
                video_id = results['result'][0]['id']
                
                vid = chap.videos.first()
                if vid:
                    vid.youtube_id = video_id
                    vid.title = results['result'][0].get('title', vid.title)
                    vid.save()
                    print(f"-> Updated existing Video (ID: {video_id})")
                    success_count += 1
                else:
                    # Create a new video if it doesn't exist
                    Video.objects.create(
                       chapter=chap,
                       title=results['result'][0].get('title', f"{chap.name} Video"),
                       youtube_id=video_id,
                       order=1
                    )
                    print(f"-> Created new Video (ID: {video_id})")
                    success_count += 1
            else:
                print("-> No results found")
        except Exception as e:
            print(f"-> Error: {e}")
        
        time.sleep(1) # Be polite
        
    print(f"\nComplete! Successfully fetched and updated {success_count} out of {total} chapters.")

if __name__ == '__main__':
    fetch_class_1_videos()
