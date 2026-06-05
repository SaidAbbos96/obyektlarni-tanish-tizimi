"""Markaziy jurnal xizmati — barcha modullar uchun."""

import logging
import logging.handlers
from pathlib import Path

from loyiha.sozlamalar.sozlamalar import Sozlamalar


def jurnal_sozlash(sozlamalar: Sozlamalar) -> logging.Logger:
    """Ilovaning markaziy jurnal tizimini sozlaydi va qaytaradi.

    Fayl jurnal (rotatsiyali) va konsol jurnal bir vaqtda ishlaydi.

    Parametrlar:
        sozlamalar: Ilova sozlamalari.

    Natija:
        Sozlangan Logger.
    """
    # Jurnal papkasini yaratish
    jurnal_yol = Path(sozlamalar.jurnal_fayl)
    jurnal_yol.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("loyiha")
    logger.setLevel(getattr(logging, sozlamalar.jurnal_daraja, logging.INFO))

    # Takror sozlashni oldini olish
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Aylanuvchi fayl handler (5 MB, 3 ta zaxira)
    fayl_handler = logging.handlers.RotatingFileHandler(
        sozlamalar.jurnal_fayl,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    fayl_handler.setFormatter(fmt)
    logger.addHandler(fayl_handler)

    # Konsol handler
    konsol_handler = logging.StreamHandler()
    konsol_handler.setFormatter(fmt)
    logger.addHandler(konsol_handler)

    return logger
