"""
Gerenciador de configurações para lidar com as configurações do jogo.
"""
import sys
import importlib
from src.config import settings

def get_setting(setting_name):
    """Obtém um valor de configuração pelo nome."""
    return getattr(settings, setting_name, None)

def set_setting(setting_name, value):
    """Define um valor de configuração pelo nome."""
    setattr(settings, setting_name, value)
    return True

def get_ai_difficulty():
    """Obtém a dificuldade atual da IA."""
    return get_setting('AI_DIFFICULTY')

def set_ai_difficulty(difficulty):
    """Define a dificuldade da IA (1-5)."""
    if 1 <= difficulty <= 5:
        set_setting('AI_DIFFICULTY', difficulty)
        return True
    return False