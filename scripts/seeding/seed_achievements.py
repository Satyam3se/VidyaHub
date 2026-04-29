import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Achievement, DailyReward

# Clear existing
Achievement.objects.all().delete()
DailyReward.objects.all().delete()

achievements_data = [
    # Streak Achievements
    {"name": "First Step", "slug": "first-step", "description": "Complete your first daily streak", "icon": "flame", "category": "streak", "xp_reward": 25, "requirement_type": "streak_days", "requirement_value": 1, "rarity": "common"},
    {"name": "On Fire", "slug": "on-fire", "description": "Maintain a 3-day streak", "icon": "flame", "category": "streak", "xp_reward": 50, "requirement_type": "streak_days", "requirement_value": 3, "rarity": "common"},
    {"name": "Week Warrior", "slug": "week-warrior", "description": "Maintain a 7-day streak", "icon": "flame", "category": "streak", "xp_reward": 100, "requirement_type": "streak_days", "requirement_value": 7, "rarity": "rare"},
    {"name": "Fortnight Fighter", "slug": "fortnight-fighter", "description": "Maintain a 14-day streak", "icon": "flame", "category": "streak", "xp_reward": 200, "requirement_type": "streak_days", "requirement_value": 14, "rarity": "epic"},
    {"name": "Monthly Master", "slug": "monthly-master", "description": "Maintain a 30-day streak", "icon": "crown", "category": "streak", "xp_reward": 500, "requirement_type": "streak_days", "requirement_value": 30, "rarity": "legendary"},
    
    # Quiz Achievements
    {"name": "Quiz Starter", "slug": "quiz-starter", "description": "Complete your first quiz", "icon": "pen-line", "category": "quiz", "xp_reward": 25, "requirement_type": "quizzes_completed", "requirement_value": 1, "rarity": "common"},
    {"name": "Quiz Enthusiast", "slug": "quiz-enthusiast", "description": "Complete 10 quizzes", "icon": "pen-line", "category": "quiz", "xp_reward": 75, "requirement_type": "quizzes_completed", "requirement_value": 10, "rarity": "common"},
    {"name": "Quiz Champion", "slug": "quiz-champion", "description": "Complete 50 quizzes", "icon": "trophy", "category": "quiz", "xp_reward": 200, "requirement_type": "quizzes_completed", "requirement_value": 50, "rarity": "rare"},
    {"name": "Quiz Legend", "slug": "quiz-legend", "description": "Complete 100 quizzes", "icon": "award", "category": "quiz", "xp_reward": 500, "requirement_type": "quizzes_completed", "requirement_value": 100, "rarity": "epic"},
    
    # Perfect Score Achievements
    {"name": "Perfectionist", "slug": "perfectionist", "description": "Get your first perfect score", "icon": "star", "category": "quiz", "xp_reward": 50, "requirement_type": "perfect_scores", "requirement_value": 1, "rarity": "common"},
    {"name": "Perfection Master", "slug": "perfection-master", "description": "Get 10 perfect scores", "icon": "sparkles", "category": "quiz", "xp_reward": 200, "requirement_type": "perfect_scores", "requirement_value": 10, "rarity": "rare"},
    {"name": "Flawless", "slug": "flawless", "description": "Get 25 perfect scores", "icon": "crown", "category": "quiz", "xp_reward": 500, "requirement_type": "perfect_scores", "requirement_value": 25, "rarity": "legendary"},
    
    # Game Achievements
    {"name": "Game On", "slug": "game-on", "description": "Play your first game", "icon": "gamepad-2", "category": "game", "xp_reward": 25, "requirement_type": "games_played", "requirement_value": 1, "rarity": "common"},
    {"name": "Gamer", "slug": "gamer", "description": "Play 10 games", "icon": "gamepad-2", "category": "game", "xp_reward": 75, "requirement_type": "games_played", "requirement_value": 10, "rarity": "common"},
    {"name": "Game Master", "slug": "game-master", "description": "Play 50 games", "icon": "trophy", "category": "game", "xp_reward": 250, "requirement_type": "games_played", "requirement_value": 50, "rarity": "rare"},
    
    # XP Achievements
    {"name": "XP Hunter", "slug": "xp-hunter", "description": "Earn 100 XP", "icon": "zap", "category": "special", "xp_reward": 25, "requirement_type": "total_xp", "requirement_value": 100, "rarity": "common"},
    {"name": "XP Collector", "slug": "xp-collector", "description": "Earn 500 XP", "icon": "zap", "category": "special", "xp_reward": 50, "requirement_type": "total_xp", "requirement_value": 500, "rarity": "common"},
    {"name": "XP Legend", "slug": "xp-legend", "description": "Earn 2000 XP", "icon": "zap", "category": "special", "xp_reward": 150, "requirement_type": "total_xp", "requirement_value": 2000, "rarity": "rare"},
    {"name": "XP God", "slug": "xp-god", "description": "Earn 5000 XP", "icon": "crown", "category": "special", "xp_reward": 500, "requirement_type": "total_xp", "requirement_value": 5000, "rarity": "legendary"},
    
    # Level Achievements
    {"name": "Level 5", "slug": "level-5", "description": "Reach level 5", "icon": "trending-up", "category": "special", "xp_reward": 100, "requirement_type": "level", "requirement_value": 5, "rarity": "common"},
    {"name": "Level 10", "slug": "level-10", "description": "Reach level 10", "icon": "trending-up", "category": "special", "xp_reward": 250, "requirement_type": "level", "requirement_value": 10, "rarity": "rare"},
    {"name": "Level 20", "slug": "level-20", "description": "Reach level 20", "icon": "crown", "category": "special", "xp_reward": 750, "requirement_type": "level", "requirement_value": 20, "rarity": "epic"},
]

for data in achievements_data:
    Achievement.objects.create(**data)

print(f"Created {len(achievements_data)} achievements")

# Daily Rewards
daily_rewards = [
    {"day": 1, "xp_reward": 25, "description": "Starter Pack"},
    {"day": 2, "xp_reward": 35, "description": "Day 2 Bonus"},
    {"day": 3, "xp_reward": 50, "description": "Keep Going!"},
    {"day": 4, "xp_reward": 60, "description": "Almost there!"},
    {"day": 5, "xp_reward": 75, "description": "Week in sight!"},
    {"day": 6, "xp_reward": 100, "description": "So close!"},
    {"day": 7, "xp_reward": 200, "description": "Weekly Champion!"},
]

for data in daily_rewards:
    DailyReward.objects.create(**data)

print(f"Created {len(daily_rewards)} daily rewards")
print("Done!")