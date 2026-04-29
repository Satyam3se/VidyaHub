import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'vidyahub.settings'

import django
django.setup()

from main.models import Chapter, MCQQuestion
from django.conf import settings
import google.generativeai as genai
import json

print("GEMINI_API_KEY:", bool(settings.GEMINI_API_KEY))
print("OPENAI_API_KEY:", bool(settings.OPENAI_API_KEY))

# Test Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content("Say hello in 5 words")
    print("GEMINI Response:", response.text[:100] if response.text else "No text")
except Exception as e:
    print("GEMINI Error:", e)

# Test OpenAI
if settings.OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in 5 words"}]
        )
        print("OPENAI Response:", response.choices[0].message.content)
    except Exception as e:
        print("OPENAI Error:", e)