"""OpenCV DNN + MobileNet-SSD aniqlash strategiyasi (21 sinf)."""

from pathlib import Path
from typing import List

import cv2
import numpy as np

from loyiha.modellar.obyekt import Obyekt
from loyiha.modellar.ramka import Ramka
from loyiha.modellar.xatolar import ModelTopilmadiXatosi, AniqlashXatosi
from loyiha.vositalar.rang_vositalari import sinf_rangi
from .asosiy_strategiya import AniqlashStrategiyasi

# MobileNet-SSD COCO-21 sinflari (fon 0-indeks)
DNN_SINFLAR: List[str] = [
    "fon",
    "samolyot",
    "velosiped",
    "qush",
    "qayiq",
    "shisha",
    "avtobus",
    "mashina",
    "mushuk",
    "stul",
    "sigir",
    "stol",
    "it",
    "ot",
    "mototsikl",
    "shaxs",
    "kochati",
    "qoy",
    "divan",
    "poyezd",
    "monitor",
]

# Model fayl nomlari
PROTOTXT_FAYL = "MobileNetSSD_deploy.prototxt"
CAFFEMODEL_FAYL = "MobileNetSSD_deploy.caffemodel"


class DnnAniqlovchi(AniqlashStrategiyasi):
    """OpenCV DNN moduli va MobileNet-SSD modeli orqali obyekt aniqlash.

    21 ta sinf: odamlar, hayvonlar, transport vositalari, mebel va boshqalar.
    CPU da ham tez ishlaydi. Model fayllarini alohida yuklab olish kerak.
    """

    def __init__(self, modellar_papka: str) -> None:
        """DNN aniqlovchini sozlaydi.

        Parametrlar:
            modellar_papka: Prototxt va caffemodel fayllari joylashgan papka.
        """
        self._papka = Path(modellar_papka)
        self._prototxt = self._papka / PROTOTXT_FAYL
        self._caffemodel = self._papka / CAFFEMODEL_FAYL
        self._tarmoq: cv2.dnn.Net | None = None

    @property
    def nomi(self) -> str:
        """Strategiya nomi."""
        return "dnn"

    @property
    def sinflar(self) -> List[str]:
        """DNN aniqlay oladigan sinflar (fon olib tashlangan)."""
        return DNN_SINFLAR[1:]  # fon ni olib tashlaymiz

    def model_fayllar_mavjud(self) -> bool:
        """Model fayllarining diskda mavjudligini tekshiradi (xato chiqarmaydi)."""
        return self._prototxt.exists() and self._caffemodel.exists()

    def model_yuklash(self) -> None:
        """MobileNet-SSD modelini yuklaydi.

        Istisno:
            ModelTopilmadiXatosi: Fayl topilmasa.
            AniqlashXatosi: Tarmoq yuklanmasa.
        """
        if not self._prototxt.exists():
            raise ModelTopilmadiXatosi(
                f"DNN model fayli topilmadi:\n  {self._prototxt}\n\n"
                f"Quyidagi fayllarni '{self._papka}' papkasiga joylashtiring:\n"
                f"  • {PROTOTXT_FAYL}\n"
                f"  • {CAFFEMODEL_FAYL}\n\n"
                f"Yuklab olish:\n"
                f"  https://github.com/chuanqi305/MobileNet-SSD"
            )
        if not self._caffemodel.exists():
            raise ModelTopilmadiXatosi(
                f"DNN model fayli topilmadi:\n  {self._caffemodel}\n\n"
                f"Quyidagi fayllarni '{self._papka}' papkasiga joylashtiring:\n"
                f"  • {PROTOTXT_FAYL}\n"
                f"  • {CAFFEMODEL_FAYL}\n\n"
                f"Yuklab olish:\n"
                f"  https://github.com/chuanqi305/MobileNet-SSD"
            )

        try:
            self._tarmoq = cv2.dnn.readNetFromCaffe(
                str(self._prototxt), str(self._caffemodel)
            )
        except cv2.error as xato:
            raise AniqlashXatosi(f"DNN model yuklanmadi: {xato}") from xato

    def tayyor_mi(self) -> bool:
        """Model yuklanganligini tekshiradi."""
        return self._tarmoq is not None

    def aniqlash(self, rasm: np.ndarray, min_aniqlik: float = 0.50) -> List[Obyekt]:
        """Rasmdan 21 ta sinfdagi obyektlarni aniqlaydi.

        Parametrlar:
            rasm:        BGR numpy massivi.
            min_aniqlik: Minimal aniqlik chegarasi (0.0–1.0).

        Natija:
            Aniqlangan obyektlar ro'yxati.

        Istisno:
            AniqlashXatosi: Model yuklanmagan bo'lsa.
        """
        if not self.tayyor_mi():
            raise AniqlashXatosi(
                "DNN model yuklanmagan. Avval model_yuklash() chaqiring."
            )

        balandlik, kenglik = rasm.shape[:2]

        # Rasmni DNN uchun tayyorlash (blob)
        blob = cv2.dnn.blobFromImage(
            cv2.resize(rasm, (300, 300)),
            scalefactor=0.007843,
            size=(300, 300),
            mean=(127.5, 127.5, 127.5),
        )

        self._tarmoq.setInput(blob)  # type: ignore[union-attr]
        chiqish = self._tarmoq.forward()  # type: ignore[union-attr]

        natijalar: List[Obyekt] = []

        # Natijalarni tahlil qilish: [1, 1, N, 7] shaklida
        for i in range(chiqish.shape[2]):
            aniqlik = float(chiqish[0, 0, i, 2])
            if aniqlik < min_aniqlik:
                continue

            sinf_indeksi = int(chiqish[0, 0, i, 1])
            if sinf_indeksi >= len(DNN_SINFLAR):
                continue

            # Koordinatalarni haqiqiy o'lchamga qaytarish
            x1 = int(chiqish[0, 0, i, 3] * kenglik)
            y1 = int(chiqish[0, 0, i, 4] * balandlik)
            x2 = int(chiqish[0, 0, i, 5] * kenglik)
            y2 = int(chiqish[0, 0, i, 6] * balandlik)

            # Rasm chegarasidan chiqmasin
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(kenglik - 1, x2)
            y2 = min(balandlik - 1, y2)

            obyekt = Obyekt(
                sinf_nomi=DNN_SINFLAR[sinf_indeksi],
                aniqlik=aniqlik,
                ramka=Ramka(x1, y1, x2, y2),
                sinf_indeksi=sinf_indeksi,
                rang=sinf_rangi(sinf_indeksi),
                strategiya=self.nomi,
            )
            natijalar.append(obyekt)

        return natijalar
