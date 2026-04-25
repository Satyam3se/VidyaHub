from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    TARGET_EXAM_CHOICES = (
        ('none', 'None'),
        ('jee', 'JEE (Engineering)'),
        ('neet', 'NEET (Medical)'),
        ('nda', 'NDA (Defence)'),
    )
    
    LEVEL_TITLES = {
        1: 'Newcomer',
        2: 'Learner',
        3: 'Explorer',
        4: 'Scholar',
        5: 'Achiever',
        6: 'Expert',
        7: 'Master',
        8: 'Champion',
        9: 'Hero',
        10: 'Legend',
        11: 'Mythic',
        12: 'Divine',
        13: 'Ultimate',
        14: 'Immortal',
        15: 'God Mode',
    }
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    # Role-specific fields
    grade = models.CharField(max_length=50, blank=True, null=True, help_text="For Students")
    target_exam = models.CharField(max_length=20, choices=TARGET_EXAM_CHOICES, default='none', help_text="For JEE/NEET students")
    subject = models.CharField(max_length=100, blank=True, null=True, help_text="For Teachers")
    
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Gamification Fields
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    streak = models.IntegerField(default=0)
    last_quiz_date = models.DateField(null=True, blank=True)
    
    # Additional gamification
    total_quizzes = models.IntegerField(default=0)
    perfect_scores = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    
    # Avatar customization
    AVATAR_CHOICES = [
        ('default', 'Default'),
        ('wizard', 'Wizard'),
        ('scientist', 'Scientist'),
        ('explorer', 'Explorer'),
        ('champion', 'Champion'),
        ('ninja', 'Ninja'),
        ('astronaut', 'Astronaut'),
        ('artist', 'Artist'),
    ]
    avatar = models.CharField(max_length=20, choices=AVATAR_CHOICES, default='default')
    
    # Battle stats
    battles_played = models.IntegerField(default=0)
    battles_won = models.IntegerField(default=0)
    battle_streak = models.IntegerField(default=0)
    highest_battle_streak = models.IntegerField(default=0)
    
    def get_level_title(self):
        return self.LEVEL_TITLES.get(self.level, 'Legend')
    
    def get_xp_for_next_level(self):
        return self.level * 500
    
    def get_xp_progress(self):
        xp_needed = self.get_xp_for_next_level()
        return min(100, (self.xp % 500) / xp_needed * 100)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Subject(models.Model):
    grade = models.ForeignKey(Grade, related_name='subjects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide icon name")

    def __str__(self):
        return f"{self.name} ({self.grade.name})"

    class Meta:
        unique_together = ('grade', 'slug')

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, related_name='chapters', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"

    class Meta:
        ordering = ['order']
        unique_together = ('subject', 'slug')

class Video(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=50, help_text="Just the ID (e.g. dQw4w9WgXcQ)")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class ChapterNote(models.Model):
    chapter = models.OneToOneField(Chapter, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField(help_text="Markdown or HTML content for the chapter notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notes for {self.chapter.name}"

class MCQQuestion(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='mcqs', on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    
    CORRECT_CHOICES = (
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    )
    correct_option = models.CharField(max_length=1, choices=CORRECT_CHOICES)
    explanation = models.TextField(blank=True, help_text="Explanation shown after answering")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"MCQ for {self.chapter.name}: {self.question_text[:30]}..."

class UserProgress(models.Model):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    chapter_note = models.ForeignKey(ChapterNote, related_name='completions', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'chapter_note')

    def __str__(self):
        return f"{self.user.username} completed {self.chapter_note.chapter.name}"

class ChapterMastery(models.Model):
    """Tracks student mastery percentage and AI recommendations per chapter."""
    user = models.ForeignKey(User, related_name='chapter_mastery', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    
    mastery_percentage = models.IntegerField(default=0)  # 0 to 100
    questions_attempted = models.IntegerField(default=0)
    questions_correct = models.IntegerField(default=0)
    
    # AI Analysis
    ai_recommendation = models.TextField(blank=True, help_text="Gemini's advice for this chapter")
    last_analyzed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username} - {self.chapter.name} ({self.mastery_percentage}%)"

class SubjectScore(models.Model):
    user = models.ForeignKey(User, related_name='subject_scores', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='leaderboard', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'subject')
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}: {self.score}"

class Achievement(models.Model):
    CATEGORY_CHOICES = (
        ('streak', 'Streak'),
        ('quiz', 'Quiz'),
        ('game', 'Game'),
        ('social', 'Social'),
        ('special', 'Special'),
    )
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Lucide icon name")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    xp_reward = models.IntegerField(default=50)
    
    # Requirement
    requirement_type = models.CharField(max_length=50)  # streak_days, quizzes_completed, etc.
    requirement_value = models.IntegerField()
    
    # Rarity
    rarity = models.CharField(max_length=20, default='common')  # common, rare, epic, legendary
    
    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, related_name='badges', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, related_name='users', on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
    
    def __str__(self):
        return f"{self.user.username} earned {self.achievement.name}"

class DailyReward(models.Model):
    day = models.PositiveIntegerField(unique=True)  # 1-7 for weekly cycle
    xp_reward = models.IntegerField(default=50)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Day {self.day}: {self.xp_reward} XP"

class XPTransaction(models.Model):
    """Track all XP gains/losses for analytics."""
    TYPE_CHOICES = (
        ('quiz', 'Quiz'),
        ('game', 'Game'),
        ('video', 'Video'),
        ('achievement', 'Achievement'),
        ('streak', 'Streak Bonus'),
        ('daily', 'Daily Reward'),
        ('penalty', 'Penalty'),
    )
    
    user = models.ForeignKey(User, related_name='xp_transactions', on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.amount} XP ({self.transaction_type})"

class UserStreak(models.Model):
    """Track detailed streak history."""
    user = models.ForeignKey(User, related_name='streak_history', on_delete=models.CASCADE)
    streak_count = models.IntegerField()
    longest_streak = models.IntegerField(default=0)
    last_activity = models.DateField()
    
    def __str__(self):
        return f"{self.user.username}: {self.streak_count} day streak"

class SeasonalEvent(models.Model):
    """Time-limited events with bonus XP."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    xp_multiplier = models.FloatField(default=1.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class UserEventReward(models.Model):
    """Track which rewards user has claimed from events."""
    user = models.ForeignKey(User, related_name='event_rewards', on_delete=models.CASCADE)
    event = models.ForeignKey(SeasonalEvent, related_name='claimants', on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')

class Friend(models.Model):
    """Friend connections between users."""
    from_user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

class FriendRequest(models.Model):
    """Pending friend requests."""
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

class UserChallenge(models.Model):
    """Challenge friends to quizzes/games."""
    challenger = models.ForeignKey(User, related_name='challenges_sent', on_delete=models.CASCADE)
    challenged = models.ForeignKey(User, related_name='challenges_received', on_delete=models.CASCADE)
    challenge_type = models.CharField(max_length=20)  # quiz, game, duel
    subject_id = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, accepted, completed, declined
    challenger_score = models.PositiveIntegerField(default=0)
    challenged_score = models.PositiveIntegerField(default=0)
    xp_reward = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.challenger.username} vs {self.challenged.username}"

class TeacherNoteUpload(models.Model):
    """Stores PDF uploads from teachers and AI-generated game insights."""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_notes')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='teacher_uploads')
    pdf_file = models.FileField(upload_to='teacher_notes/')
    
    # AI Generated Content (Stored as JSON or Text)
    game_levels_json = models.JSONField(null=True, blank=True, help_text="5 Game Levels summary")
    blindspots_json = models.JSONField(null=True, blank=True, help_text="Student difficult spots")
    quiz_questions_json = models.JSONField(null=True, blank=True, help_text="10 Generated Quiz Questions")
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Note: {self.chapter.name} by {self.teacher.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
