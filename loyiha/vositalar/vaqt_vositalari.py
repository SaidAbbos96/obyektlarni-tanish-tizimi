"""Sana va vaqt bilan ishlash uchun yordamchi funksiyalar."""

from datetime import datetime


def hozir_formatlangan() -> str:
    """Joriy sana va vaqtni fayl nomi uchun qulay formatda qaytaradi.

    Natija:
        Masalan: '2026-06-05_143022'
    """
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def hozir_iso() -> str:
    """Joriy sana va vaqtni ISO 8601 formatida qaytaradi.

    Natija:
        Masalan: '2026-06-05T14:30:22.123456'
    """
    return datetime.now().isoformat()


def ms_dan_soniyaga(ms: float) -> str:
    """Millisekundni 'X.XX s' formatida qaytaradi.

    Parametrlar:
        ms: Millisekund qiymati.

    Natija:
        Masalan: '1.24 s'
    """
    return f"{ms / 1000:.2f} s"
