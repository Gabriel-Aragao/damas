from src.config import settings

def get_ai_difficulty():
    return getattr(settings, 'AI_DIFFICULTY', None)

def set_ai_difficulty(difficulty):
    if 1 <= difficulty <= 5:
        setattr(settings, 'AI_DIFFICULTY', difficulty)
        return True
    return False