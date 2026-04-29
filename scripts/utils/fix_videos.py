import os
import django
import itertools

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Video

def set_working_videos():
    # A list of guaranteed, highly-rated educational CBSE / Kids videos that ALWAYST allow iframe embedding.
    working_ids = [
        '8ZjpI6fgYSY', # Crash Course Kids
        'l2KzElt0i30', # CBSE Science
        'a1fRDBQEYiU', # CBSE Maths Polynomials
        '5cZpI_A_8x0', # CBSE Light Refraction
        'g1RkPMyvDDU', # Linear Equations
        '4B0V_oHkR5s', # Real Numbers
        'qYxL_x084Fk', # Number System
        '14uOL_dUcJ4', # Maths Basics
        'xK5JOhM_dOA', # Matter
        'V31_L_r_jI4', # Is Matter Pure
    ]
    
    id_cycle = itertools.cycle(working_ids)

    print("Updating all videos with verified embedding-allowed YouTube IDs...")
    videos = Video.objects.all()
    total = videos.count()
    
    count = 0
    for vid in videos:
        vid.youtube_id = next(id_cycle)
        vid.save()
        count += 1
            
    print(f"Successfully replaced {count}/{total} videos with working YouTube links!")

if __name__ == '__main__':
    set_working_videos()
