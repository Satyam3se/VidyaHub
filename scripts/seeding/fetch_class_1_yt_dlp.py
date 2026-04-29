import os
import django
import time
import yt_dlp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, Video

def fetch_class_1_videos():
    print("Starting YouTube fetch for Class 1 chapters using yt-dlp...")
    chapters = Chapter.objects.filter(subject__grade__name='Class 1')
    total = chapters.count()
    
    ydl_opts = {
        'extract_flat': True,
        'force_ipv4': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    success_count = 0
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, chap in enumerate(chapters, 1):
            # Formulating the search query
            # Adding 'cbse class 1' for specificity
            query = f"ytsearch1:cbse class 1 {chap.subject.name} {chap.name} in hindi"
            print(f"[{i:02d}/{total}] {chap.subject.name} - {chap.name[:25]}...", end=" ")
            
            try:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    entry = info['entries'][0]
                    video_id = entry.get('id')
                    video_title = entry.get('title')
                    
                    if video_id:
                        vid = chap.videos.first()
                        if vid:
                            vid.youtube_id = video_id
                            vid.title = video_title or vid.title
                            vid.save()
                            print(f"-> Updated (ID: {video_id})")
                            success_count += 1
                        else:
                            Video.objects.create(
                               chapter=chap,
                               title=video_title or f"{chap.name} Video",
                               youtube_id=video_id,
                               order=1
                            )
                            print(f"-> Created (ID: {video_id})")
                            success_count += 1
                    else:
                        print("-> No video ID found")
                else:
                    print("-> No results")
            except Exception as e:
                print(f"-> Error finding video")
            
            # Rate limiting delay
            time.sleep(1)
            
    print(f"\nComplete! Successfully fetched and updated {success_count} out of {total} chapters.")

if __name__ == '__main__':
    fetch_class_1_videos()
