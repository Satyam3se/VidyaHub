import redis
import json
from django.conf import settings
from .models import SubjectScore, Subject, Achievement, UserBadge
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

# Initialize Redis client
try:
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    r.ping()
    REDIS_AVAILABLE = True
except Exception as e:
    print(f"Redis not available: {e}")
    REDIS_AVAILABLE = False

def update_user_score(user, subject_id, score_delta):
    """Update user's score for a subject in both DB and Redis."""
    subject = Subject.objects.get(id=subject_id)
    
    # DB Update
    score_obj, created = SubjectScore.objects.get_or_create(user=user, subject=subject)
    score_obj.score = F('score') + score_delta
    score_obj.save()
    
    # Reload from DB to get the new actual score
    score_obj.refresh_from_db()
    actual_score = score_obj.score

    # Redis Update
    if REDIS_AVAILABLE:
        leaderboard_key = f"leaderboard:{subject_id}"
        r.zadd(leaderboard_key, {user.username: actual_score})
    
    return actual_score

def get_subject_leaderboard(subject_id, limit=10):
    """Retrieve the top users for a subject."""
    if REDIS_AVAILABLE:
        leaderboard_key = f"leaderboard:{subject_id}"
        raw_data = r.zrevrange(leaderboard_key, 0, limit - 1, withscores=True)
        # Format: [('username', 100.0), ...]
        return [{'username': user, 'score': int(score)} for user, score in raw_data]
    else:
        # DB Fallback
        scores = SubjectScore.objects.filter(subject_id=subject_id).select_related('user').order_by('-score')[:limit]
        return [{'username': s.user.username, 'score': s.score} for s in scores]

def get_global_leaderboard(limit=10):
    """Retrieve global rankings across all subjects."""
    from django.db.models import Sum
    from django.contrib.auth.models import User
    
    top_users = User.objects.annotate(total_score=Sum('subject_scores__score')).order_by('-total_score')[:limit]
    return [{'username': u.username, 'score': u.total_score or 0} for u in top_users]

# ============ GAMIFICATION FUNCTIONS ============

def add_xp(user, amount, activity_type='general', description=''):
    """Add XP to user, handle level ups and badge checks."""
    from .models import XPTransaction, SeasonalEvent
    from django.utils import timezone
    
    profile = user.profile
    
    # Check for active events
    multiplier = 1.0
    active_event = SeasonalEvent.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()
    
    if active_event:
        multiplier = active_event.xp_multiplier
    
    # Apply multiplier
    actual_amount = int(amount * multiplier)
    profile.xp += actual_amount
    
    # Log transaction
    XPTransaction.objects.create(
        user=user,
        amount=actual_amount,
        transaction_type=activity_type,
        description=description or f"{activity_type} - {amount} XP"
    )
    
    # Check for level up
    xp_needed = profile.level * 500
    new_badges = []
    leveled_up = 0
    
    while profile.xp >= profile.level * 500:
        profile.level += 1
        leveled_up = profile.level
        profile.save()
        new_badges.extend(check_level_badges(profile))
    
    profile.save()
    
    # Check streak
    update_streak(profile)
    
    # Check achievements
    new_badges.extend(check_achievements(profile, activity_type))
    
    return {
        'new_xp': profile.xp,
        'new_level': profile.level,
        'leveled_up': leveled_up,
        'new_badges': new_badges,
        'xp_earned': actual_amount,
        'event_bonus': multiplier > 1,
        'event_name': active_event.name if active_event else None
    }

def update_streak(profile):
    """Update user's daily streak."""
    today = timezone.now().date()
    
    if profile.last_quiz_date:
        days_diff = (today - profile.last_quiz_date).days
        
        if days_diff == 1:
            # Consecutive day - increase streak
            profile.streak += 1
        elif days_diff > 1:
            # Streak broken
            profile.streak = 1
        # If days_diff == 0, same day, don't change streak
    else:
        # First activity
        profile.streak = 1
    
    profile.last_quiz_date = today
    profile.save()

def check_achievements(profile, activity_type='general'):
    """Check and award achievements based on profile stats."""
    earned_badges = []
    user = profile.user
    
    # Map activity type to requirement type
    type_map = {
        'quiz': 'quizzes_completed',
        'perfect': 'perfect_scores',
        'game': 'games_played',
        'streak': 'streak_days',
        'battle': 'battles_won',
        'battle_win': 'battles_won',
    }
    
    requirement_type = type_map.get(activity_type, 'total_xp')
    
    # Get all achievements the user doesn't have yet
    user_badges = UserBadge.objects.filter(user=user).values_list('achievement_id', flat=True)
    achievements = Achievement.objects.exclude(id__in=user_badges)
    
    for achievement in achievements:
        # Check if this achievement matches current activity or is XP-based
        if achievement.requirement_type in [requirement_type, 'total_xp', 'level']:
            current_value = 0
            
            if achievement.requirement_type == 'quizzes_completed':
                current_value = profile.total_quizzes
            elif achievement.requirement_type == 'perfect_scores':
                current_value = profile.perfect_scores
            elif achievement.requirement_type == 'games_played':
                current_value = profile.games_played
            elif achievement.requirement_type == 'streak_days':
                current_value = profile.streak
            elif achievement.requirement_type == 'total_xp':
                current_value = profile.xp
            elif achievement.requirement_type == 'level':
                current_value = profile.level
            elif achievement.requirement_type == 'battles_won':
                current_value = profile.battles_won
            elif achievement.requirement_type == 'battle_streak':
                current_value = profile.battle_streak
            
            if current_value >= achievement.requirement_value:
                # Award achievement
                UserBadge.objects.create(user=user, achievement=achievement)
                profile.xp += achievement.xp_reward
                profile.save()
                earned_badges.append(achievement)
    
    return earned_badges

def check_level_badges(profile):
    """Check level-based achievements."""
    return check_achievements(profile, 'level')

def get_user_badges(user):
    """Get all badges for a user."""
    return UserBadge.objects.filter(user=user).select_related('achievement').order_by('-earned_at')

def get_daily_reward(streak_days):
    """Get daily reward based on streak (1-7 day cycle)."""
    from .models import DailyReward
    day = ((streak_days - 1) % 7) + 1
    try:
        return DailyReward.objects.get(day=day)
    except DailyReward.DoesNotExist:
        return None

def get_achievement_progress(profile):
    """Get progress toward next achievements."""
    achievements = Achievement.objects.all()[:10]
    progress = []
    
    for achievement in achievements:
        current_value = 0
        
        if achievement.requirement_type == 'quizzes_completed':
            current_value = profile.total_quizzes
        elif achievement.requirement_type == 'perfect_scores':
            current_value = profile.perfect_scores
        elif achievement.requirement_type == 'games_played':
            current_value = profile.games_played
        elif achievement.requirement_type == 'streak_days':
            current_value = profile.streak
        elif achievement.requirement_type == 'total_xp':
            current_value = profile.xp
        elif achievement.requirement_type == 'level':
            current_value = profile.level
        
        progress_percent = min(100, (current_value / achievement.requirement_value) * 100)
        
        # Check if already earned
        earned = UserBadge.objects.filter(user=profile.user, achievement=achievement).exists()
        
        progress.append({
            'name': achievement.name,
            'description': achievement.description,
            'icon': achievement.icon,
            'rarity': achievement.rarity,
            'current': current_value,
            'required': achievement.requirement_value,
            'progress': progress_percent,
            'earned': earned,
            'xp_reward': achievement.xp_reward
        })
    
    return progress
