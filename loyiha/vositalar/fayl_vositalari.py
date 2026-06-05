"""Fayl va papka bilan ishlash uchun yordamchi funksiyalar."""

from pathlib import Path


def papka_yaratish(manzil: str | Path) -> Path:
    """Ko'rsatilgan manzilda papkani yaratadi (mavjud bo'lsa o'tkazib yuboradi).

    Parametrlar:
        manzil: Papka manzili.

    Natija:
        Path obyekti.
    """
    yol = Path(manzil)
    yol.mkdir(parents=True, exist_ok=True)
    return yol


def fayl_mavjudmi(manzil: str | Path) -> bool:
    """Fayl mavjudligini tekshiradi.

    Parametrlar:
        manzil: Fayl manzili.

    Natija:
        True — mavjud bo'lsa, False — bo'lmasa.
    """
    return Path(manzil).is_file()


def fayl_kengaytmasi(manzil: str | Path) -> str:
    """Fayl kengaytmasini kichik harfda qaytaradi, masalan '.jpg'.

    Parametrlar:
        manzil: Fayl manzili.

    Natija:
        Kengaytma, masalan: '.jpg', '.png'.
    """
    return Path(manzil).suffix.lower()


def kerakli_papkalarni_yaratish(papkalar: list[str]) -> None:
    """Bir nechta papkalarni bir vaqtda yaratadi.

    Parametrlar:
        papkalar: Papka manzillari ro'yxati.
    """
    for manzil in papkalar:
        papka_yaratish(manzil)
