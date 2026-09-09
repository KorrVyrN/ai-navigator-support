"""
AI-Штурман - AI-powered platform for predictive incident detection
MVP модуль предиктивного обнаружения массовых инцидентов и аварий провайдеров
на базе GigaChat API, RAG и защиты персональных данных (ФЗ-152)
"""

__version__ = "0.1.0"
__author__ = "KorrVyrN"
__description__ = "AI Navigator - Predictive Incident Detection Platform"

from app.services.anonymizer import PIIAnonymizer

__all__ = [
    "PIIAnonymizer",
    "__version__",
    "__author__",
    "__description__",
]
