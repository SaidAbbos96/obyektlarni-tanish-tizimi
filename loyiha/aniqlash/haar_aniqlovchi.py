"""Haar Cascade aniqlash strategiyasi — OpenCV klassik usuli."""

from pathlib import Path
from typing import List

import cv2
import numpy as np

from loyiha.modellar.obyekt import Obyekt
from loyiha.modellar.ramka import Ramka
from loyiha.modellar.xatolar import ModelTopilmadiXatosi, AniqlashXatosi
from loyiha.vositalar.rang_vositalari import sinf_rangi
from .asosiy_strategiya import AniqlashStrategiyasi

# Haar modeli fayl nomi
HAAR_FAYL_NOMI = "haarcascade_frontalface_default.xml"

# OpenCV ning ichida o'rnatilgan Haar modeli manzili
OPENCV_HAAR_ICHKI = str(Path(cv2.__file__).parent / "data" / HAAR_FAYL_NOMI)


class HaarAniqlovchi(AniqlashStrategiyasi):
    """OpenCV Haar Cascade Classifier yordamida yuz aniqlash.

    Oddiy va tez. Kamera va fotosuratdagi yuzlarni aniqlaydi.
    Alohida model fayli kerak emas — OpenCV bilan birga keladi.
    """

    def __init__(self, model_manzili: str | None = None) -> None:
        """Haar aniqlovchini sozlaydi.

        Parametrlar:
            model_manzili: XML fayl manzili. None bo'lsa OpenCV
                           ichki modelidan foydalaniladi.
        """
        # Model manzilini aniqlash
        self._model_manzili = model_manzili or OPENCV_HAAR_ICHKI
        self._aniqlovchi: cv2.CascadeClassifier | None = None

    @property
    def nomi(self) -> str:
        """Strategiya nomi."""
        return "haar"

    @property
    def sinflar(self) -> List[str]:
        """Haar faqat yuz aniqlaydi."""
        return ["yuz"]

    def model_yuklash(self) -> None:
        """Haar modelini fayldan yuklaydi.

        Istisno:
            ModelTopilmadiXatosi: Fayl topilmasa.
            AniqlashXatosi: Model yuklanmasa.
        """
        if not Path(self._model_manzili).exists():
            raise ModelTopilmadiXatosi(
                f"Haar model fayli topilmadi: {self._model_manzili}"
            )

        aniqlovchi = cv2.CascadeClassifier(self._model_manzili)
        if aniqlovchi.empty():
            raise AniqlashXatosi(f"Haar model yuklanmadi: {self._model_manzili}")

        self._aniqlovchi = aniqlovchi

    def tayyor_mi(self) -> bool:
        """Model yuklanganligini tekshiradi."""
        return self._aniqlovchi is not None

    def aniqlash(self, rasm: np.ndarray, min_aniqlik: float = 0.5) -> List[Obyekt]:
        """Rasmdan yuzlarni aniqlaydi.

        Parametrlar:
            rasm:        BGR numpy massivi.
            min_aniqlik: Haar uchun ishlatilmaydi (compatibility uchun).

        Natija:
            Aniqlangan yuzlar ro'yxati.

        Istisno:
            AniqlashXatosi: Model yuklanmagan bo'lsa.
        """
        if not self.tayyor_mi():
            raise AniqlashXatosi(
                "Haar model yuklanmagan. Avval model_yuklash() chaqiring."
            )

        # Kulrang formatga o'tkazish (Haar kulrang tasvir bilan ishlaydi)
        kulrang = cv2.cvtColor(rasm, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(kulrang, kulrang)

        # Yuzlarni aniqlash
        yuzlar = self._aniqlovchi.detectMultiScale(  # type: ignore[union-attr]
            kulrang,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        natijalar: List[Obyekt] = []
        if len(yuzlar) == 0:
            return natijalar

        rang = sinf_rangi(0)
        for x, y, w, h in yuzlar:
            obyekt = Obyekt(
                sinf_nomi="yuz",
                aniqlik=1.0,  # Haar aniqlikni bermaydi — 1.0 qo'yamiz
                ramka=Ramka(int(x), int(y), int(x + w), int(y + h)),
                sinf_indeksi=0,
                rang=rang,
                strategiya=self.nomi,
            )
            natijalar.append(obyekt)

        return natijalar
