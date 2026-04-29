import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()
from main.models import Chapter, Video

print("=== Class 1 Video IDs currently in DB ===")
chapters = Chapter.objects.filter(subject__grade__name='Class 1').order_by('subject__name', 'order')
for c in chapters:
    v = c.videos.first()
    vid_id = v.youtube_id if v else 'NO VIDEO'
    print(f"{c.subject.name:10s} | {c.name[:35]:35s} | {vid_id}")
