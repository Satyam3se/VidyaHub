with open('c:/VidyaHub/templates/main/video_player.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\r\n', '\n')

old_broken = """            </script>

                </div>
            </aside>
        </div>
    </div>
</section>"""

new_fixed = """            </script>

            <!-- Sidebar Navigation -->
            <aside class="player-sidebar glass">
                <div class="sidebar-header">
                    <h3>Course Content</h3>
                    <span>{{ all_chapters.count }} Chapters</span>
                </div>
                <div class="sidebar-list">
                    {% for chap in all_chapters %}
                    <div class="sidebar-chapter-group">
                        <div class="chapter-header">
                            <i data-lucide="book-open" class="me-2"></i>
                            Chapter {{ forloop.counter }}: {{ chap.name }}
                        </div>
                        {% for vid in chap.videos.all %}
                        <a href="{% url 'chapter_detail' grade.slug subject.slug chap.slug %}?v={{ vid.id }}"
                           class="sidebar-item animate-scale {% if vid.id == current_video.id %}active{% endif %}">
                            <div class="item-icon">
                                {% if vid.id == current_video.id %}
                                <i data-lucide="play-circle" class="playing-icon"></i>
                                {% else %}
                                <i data-lucide="play" class="opacity-50"></i>
                                {% endif %}
                            </div>
                            <div class="item-text">
                                <span class="item-name">{{ vid.title }}</span>
                                <span class="item-meta">Video Lesson</span>
                            </div>
                        </a>
                        {% empty %}
                        <div class="sidebar-item disabled opacity-50">
                            <div class="item-icon"><i data-lucide="circle"></i></div>
                            <div class="item-text">
                                <span class="item-name">No videos yet</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% endfor %}
                </div>
            </aside>
        </div>
    </div>
</section>"""

if old_broken in content:
    content = content.replace(old_broken, new_fixed)
    print("SUCCESS: Sidebar restored!")
else:
    print("ERROR: Pattern not found. Current content around line 230:")
    lines = content.split('\n')
    for i, line in enumerate(lines[228:240], start=229):
        print(f"{i}: {repr(line)}")

with open('c:/VidyaHub/templates/main/video_player.html', 'w', encoding='utf-8') as f:
    f.write(content)
