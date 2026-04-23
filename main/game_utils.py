"""
VidyaHub Game Utilities
Functions for quiz generation, XP calculation, and clan progression.
"""
import random
from .models import MCQQuestion


def generate_30_questions(subject, grade_slug):
    """
    Fetch 30 MCQ questions for a given subject.
    Priority: DB questions -> empty list (caller handles fallback).
    Questions are randomly shuffled.
    """
    # Get all MCQ questions for this subject across all chapters
    qs_queryset = MCQQuestion.objects.filter(chapter__subject=subject)
    
    if qs_queryset.count() == 0:
        return []
    
    # Shuffle and take up to 30
    question_list = list(qs_queryset)
    random.shuffle(question_list)
    return question_list[:30]


def calculate_xp_award(score, time_taken=None):
    """
    Calculate XP earned from a quiz attempt.
    - score: number of correct answers (out of 30)
    - time_taken: seconds taken (optional, for bonus)
    """
    base_xp = score * 10  # 10 XP per correct answer

    # Speed bonus: if completed in under 5 minutes
    if time_taken and time_taken < 300:
        speed_bonus = max(0, int((300 - time_taken) / 10))
        base_xp += speed_bonus

    # Perfect score bonus
    if score == 30:
        base_xp += 50

    return base_xp


def get_clan_info(progress_percent):
    """
    Return clan name, slug, and next milestone based on progress.
    """
    if progress_percent >= 75:
        return "Boss Clan", "boss", 100
    elif progress_percent >= 50:
        return "Challenge Clan", "challenge", 75
    elif progress_percent >= 25:
        return "Practice Clan", "practice", 50
    else:
        return "Basics Clan", "basics", 25


def calculate_level(xp):
    """Calculate level from XP. Each level needs 500 XP."""
    return max(1, (xp // 500) + 1)


def get_rank_label(level):
    """Return a rank title based on level."""
    if level >= 20:
        return "Legend"
    elif level >= 15:
        return "Master"
    elif level >= 10:
        return "Expert"
    elif level >= 5:
        return "Apprentice"
    else:
        return "Novice"
