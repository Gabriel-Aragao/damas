"""
Settings manager to handle game settings.
"""
import sys
import importlib
from src.config import settings

def get_setting(setting_name):
    """Get a setting value by name."""
    return getattr(settings, setting_name, None)

def set_setting(setting_name, value):
    """Set a setting value by name."""
    setattr(settings, setting_name, value)
    return True

def get_ai_difficulty():
    """Get the current AI difficulty."""
    return get_setting('AI_DIFFICULTY')

def set_ai_difficulty(difficulty):
    """Set the AI difficulty (1-5)."""
    if 1 <= difficulty <= 5:
        set_setting('AI_DIFFICULTY', difficulty)
        return True
    return False