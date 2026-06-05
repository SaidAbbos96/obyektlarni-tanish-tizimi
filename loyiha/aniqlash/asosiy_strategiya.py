"""Barcha aniqlash strategiyalari uchun abstrakt asosiy sinf."""

from abc import ABC, abstractmethod
from typing import List

import numpy as np

from loyiha.modellar.obyekt import Obyekt


class AniqlashStrategiyasi(ABC):
    """Barcha aniqlovchilar implement qilishi kerak bo'lgan shartnoma.

    Yangi strategiya qo'shish uchun bu sinfdan meros oling va
    barcha abstractmethod larni implement qiling.
    """

    @abstractmethod
    def model_yuklash(self) -> None:
        """Modelni fayldan xotiraga yuklaydi."""

    @abstractmethod
    def aniqlash(self, rasm: np.ndarray, min_aniqlik: float = 0.5) -> List[Obyekt]:
        """Rasmdan obyektlarni aniqlaydi va ro'yxat qaytaradi.

        Parametrlar:
            rasm:         BGR formatdagi numpy massivi.
            min_aniqlik:  Minimal aniqlik chegarasi (0.0–1.0).

        Natija:
            Aniqlangan obyektlar ro'yxati.
        """

    @abstractmethod
    def tayyor_mi(self) -> bool:
        """Model yuklangan va aniqlashga tayyor ekanligini tekshiradi."""

    @property
    @abstractmethod
    def nomi(self) -> str:
        """Strategiya identifikatori: 'haar', 'dnn', 'yolo'."""

    @property
    @abstractmethod
    def sinflar(self) -> List[str]:
        """Bu strategiya aniqlay oladigan obyekt sinflari."""
