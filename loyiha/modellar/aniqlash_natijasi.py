"""Bitta aniqlash sessiyasining to'liq natijasi."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .obyekt import Obyekt


@dataclass
class AniqlashNatijasi:
    """Bitta aniqlash jarayonining natijasi — barcha meta-ma'lumotlar bilan.

    Parametrlar:
        rasm_manzili:    Manba rasm fayli manzili.
        aniqlash_vaqti:  Aniqlash boshlangan vaqt.
        obyektlar:       Aniqlangan obyektlar ro'yxati.
        ishlash_vaqti_ms: Aniqlash davom etgan vaqt (millisekundda).
        rasm_olchami:    Rasm o'lchami (balandlik, kenglik).
        strategiya_nomi: Ishlatilgan strategiya nomi.
    """

    rasm_manzili: str
    aniqlash_vaqti: datetime
    obyektlar: List[Obyekt]
    ishlash_vaqti_ms: float
    rasm_olchami: tuple[int, int]
    strategiya_nomi: str
    chizilgan_rasm: object = field(default=None, repr=False)

    @property
    def obyektlar_soni(self) -> int:
        """Aniqlangan obyektlar soni."""
        return len(self.obyektlar)

    @property
    def ortacha_aniqlik(self) -> float:
        """O'rtacha aniqlik darajasi. Obyekt yo'q bo'lsa 0.0."""
        if not self.obyektlar:
            return 0.0
        return sum(o.aniqlik for o in self.obyektlar) / len(self.obyektlar)

    @property
    def sinf_statistikasi(self) -> dict[str, int]:
        """Har bir sinf nechta aniqlangan — lug'at ko'rinishida."""
        stat: dict[str, int] = {}
        for ob in self.obyektlar:
            stat[ob.sinf_nomi] = stat.get(ob.sinf_nomi, 0) + 1
        return stat

    def json_ga(self) -> dict:
        """Natijani JSON uchun lug'at ko'rinishiga o'tkazadi."""
        return {
            "rasm_manzili": self.rasm_manzili,
            "aniqlash_vaqti": self.aniqlash_vaqti.isoformat(),
            "strategiya": self.strategiya_nomi,
            "ishlash_vaqti_ms": round(self.ishlash_vaqti_ms, 2),
            "rasm_olchami": {
                "balandlik": self.rasm_olchami[0],
                "kenglik": self.rasm_olchami[1],
            },
            "jami_obyektlar": self.obyektlar_soni,
            "ortacha_aniqlik": round(self.ortacha_aniqlik, 4),
            "sinf_statistikasi": self.sinf_statistikasi,
            "obyektlar": [o.json_ga() for o in self.obyektlar],
        }
