import os
import django
import time
import yt_dlp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, Video

def fetch_all_class_videos():
    grades = Grade.objects.filter(name__in=[f'Class {i}' for i in range(2, 11)])
    
    ydl_opts = {
        'extract_flat': True,
        'force_ipv4': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for grade in grades:
            print(f"=== Starting YouTube fetch for {grade.name} ===")
            chapters = Chapter.objects.filter(subject__grade=grade)
            total = chapters.count()
            success_count = 0
            
            for i, chap in enumerate(chapters, 1):
                query = f"ytsearch1:cbse {grade.name.lower()} {chap.subject.name} {chap.name} in hindi"
                print(f"[{grade.name}] [{i:02d}/{total}] {chap.subject.name} - {chap.name[:25]}...", end=" ")
                
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
                
            print(f"Complete for {grade.name}! Successfully fetched {success_count}/{total} chapters.\n")

if __name__ == '__main__':
    fetch_all_class_videos()
