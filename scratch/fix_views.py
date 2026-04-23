import os

file_path = r'c:\VidyaHub\main\views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if "'level_up': level_up," in line and i + 1 < len(lines) and "subject = get_object_or_404" in lines[i+1]:
        new_lines.append(line)
        new_lines.append("        })\n")
        new_lines.append("    return JsonResponse({'error': 'Invalid request'}, status=400)\n\n")
        new_lines.append("@login_required\n")
        new_lines.append("def boss_battle_init(request, subject_id):\n")
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed views.py successfully.")
