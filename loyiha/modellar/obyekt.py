"""Aniqlangan bitta obyekt ma'lumot modeli."""

from dataclasses import dataclass
from .ramka import Ramka


@dataclass(frozen=True)
class Obyekt:
    """Rasmda aniqlangan bitta obyekt.

    Parametrlar:
        sinf_nomi:     Obyekt sinfi nomi (masalan: "yuz", "shaxs").
        aniqlik:       Aniqlik darajasi 0.0 dan 1.0 gacha.
        ramka:         Bounding box koordinatalari.
        sinf_indeksi:  Model sinf raqami.
        rang:          Vizualizatsiya uchun BGR rang (B, G, R).
        strategiya:    Qaysi strategiya aniqladi ("haar", "dnn", "yolo").
    """

    sinf_nomi: str
    aniqlik: float
    ramka: Ramka
    sinf_indeksi: int
    rang: tuple[int, int, int]
    strategiya: str

    @property
    def aniqlik_foiz(self) -> str:
        """Aniqlikni foiz ko'rinishida qaytaradi, masalan: '94.5%'."""
        return f"{self.aniqlik * 100:.1f}%"

    def json_ga(self) -> dict:
        """Obyektni JSON uchun lug'at ko'rinishiga o'tkazadi."""
        return {
            "sinf": self.sinf_nomi,
            "aniqlik": round(self.aniqlik, 4),
            "strategiya": self.strategiya,
            "ramka": {
                "x1": self.ramka.x1,
                "y1": self.ramka.y1,
                "x2": self.ramka.x2,
                "y2": self.ramka.y2,
            },
        }
