"""Bounding box ma'lumot modeli."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Ramka:
    """Aniqlangan obyektning to'rtburchak chegarasi.

    Parametrlar:
        x1: Chap yuqori burchak X koordinatasi.
        y1: Chap yuqori burchak Y koordinatasi.
        x2: O'ng quyi burchak X koordinatasi.
        y2: O'ng quyi burchak Y koordinatasi.
    """

    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def kenglik(self) -> int:
        """Ramka kengligi (piksel)."""
        return self.x2 - self.x1

    @property
    def balandlik(self) -> int:
        """Ramka balandligi (piksel)."""
        return self.y2 - self.y1

    @property
    def yuza(self) -> int:
        """Ramka yuzasi (piksel kvadrat)."""
        return self.kenglik * self.balandlik

    @property
    def markaz(self) -> tuple[int, int]:
        """Ramka markaziy nuqtasi (x, y)."""
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    def to_tuple(self) -> tuple[int, int, int, int]:
        """Ramkani to'plam sifatida qaytaradi (x1, y1, x2, y2)."""
        return (self.x1, self.y1, self.x2, self.y2)
