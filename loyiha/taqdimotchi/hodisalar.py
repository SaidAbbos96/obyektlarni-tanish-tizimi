"""Hodisalar tizimi — MVP arxitekturasi uchun."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class HodisaTuri(Enum):
    """Ilovada chiqariladigan hodisa turlari."""

    # Rasm bilan bog'liq
    RASM_TANLANDI = auto()
    RASM_YUKLANDI = auto()
    RASM_YUKLANMADI = auto()

    # Aniqlash bilan bog'liq
    ANIQLASH_BOSHLANDI = auto()
    ANIQLASH_TUGADI = auto()
    ANIQLASH_XATOSI = auto()

    # Strategiya bilan bog'liq
    STRATEGIYA_ALMASHDI = auto()

    # Saqlash bilan bog'liq
    NATIJA_SAQLANDI = auto()

    # Holat
    HOLAT_YANGILANDI = auto()
    XATO_YUZAGA_KELDI = auto()


@dataclass
class Hodisa:
    """Bir hodisani ifodalovchi ma'lumotlar konteyner.

    Maydonlar:
        tur:  Hodisa turi (HodisaTuri).
        data: Ixtiyoriy qo'shimcha ma'lumot.
    """

    tur: HodisaTuri
    data: Any = field(default=None)
