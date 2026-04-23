from django.contrib import admin
from .models import Profile, Grade, Subject, Chapter, Video, ChapterNote, MCQQuestion, UserProgress

admin.site.register(Profile)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Video)
admin.site.register(ChapterNote)
admin.site.register(MCQQuestion)
admin.site.register(UserProgress)
