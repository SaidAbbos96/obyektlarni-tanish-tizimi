"""Obyekt aniqlash xizmati — strategiya orqali, asinxron versiyasi bilan."""

import logging
import queue
import threading
import time
from datetime import datetime
from typing import Callable

import numpy as np

from loyiha.aniqlash.asosiy_strategiya import AniqlashStrategiyasi
from loyiha.modellar.aniqlash_natijasi import AniqlashNatijasi
from loyiha.modellar.xatolar import AniqlashXatosi
from loyiha.vositalar.rasm_vositalari import opencv_dan_pil
from loyiha.sozlamalar.sozlamalar import Sozlamalar
import cv2

log = logging.getLogger("loyiha.aniqlash")


def _ramkalar_chizish(
    rasm: np.ndarray, natija: AniqlashNatijasi, qalinlik: int, shrift: float
) -> np.ndarray:
    """Aniqlangan obyektlarning ramkalarini rasmga chizadi.

    Parametrlar:
        rasm:     BGR asl rasm.
        natija:   AniqlashNatijasi.
        qalinlik: Ramka chiziq qalinligi.
        shrift:   Label shrift o'lchami.

    Natija:
        Ramkalar chizilgan yangi rasm nusxasi.
    """
    chizilgan = rasm.copy()
    for ob in natija.obyektlar:
        r = ob.ramka
        rang = ob.rang

        # Bounding box
        cv2.rectangle(chizilgan, (r.x1, r.y1), (r.x2, r.y2), rang, qalinlik)

        # Label matni
        matn = f"{ob.sinf_nomi} {ob.aniqlik_foiz}"
        (m_k, m_b), _ = cv2.getTextSize(matn, cv2.FONT_HERSHEY_SIMPLEX, shrift, 1)

        # Label fon
        fon_y1 = max(0, r.y1 - m_b - 6)
        cv2.rectangle(chizilgan, (r.x1, fon_y1), (r.x1 + m_k + 4, r.y1), rang, -1)

        # Matn
        cv2.putText(
            chizilgan,
            matn,
            (r.x1 + 2, r.y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            shrift,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return chizilgan


class ObyektAniqlovchiXizmat:
    """Strategiya orqali rasmdan obyektlarni aniqlovchi xizmat.

    Foydalanish:
        xizmat = ObyektAniqlovchiXizmat(aniqlovchi, sozlamalar)
        xizmat.strategiyani_yuklash()
        natija = xizmat.aniqlash(rasm, manzil)
    """

    def __init__(
        self, aniqlovchi: AniqlashStrategiyasi, sozlamalar: Sozlamalar
    ) -> None:
        """Xizmatni sozlaydi.

        Parametrlar:
            aniqlovchi: Faol strategiya nusxasi.
            sozlamalar: Ilova sozlamalari.
        """
        self._aniqlovchi = aniqlovchi
        self._sozlamalar = sozlamalar

    @property
    def strategiya_nomi(self) -> str:
        """Faol strategiya nomi."""
        return self._aniqlovchi.nomi

    def strategiyani_almashtirish(self, yangi_aniqlovchi: AniqlashStrategiyasi) -> None:
        """Ishlayotgan strategiyani almashtiradi (model keyinroq yuklanadi).

        Parametrlar:
            yangi_aniqlovchi: Yangi strategiya nusxasi.
        """
        self._aniqlovchi = yangi_aniqlovchi

    def strategiyani_yuklash(self) -> None:
        """Faol strategiya modelini yuklaydi (hali yuklanmagan bo'lsa)."""
        if not self._aniqlovchi.tayyor_mi():
            log.info("Model yuklanmoqda: %s", self.strategiya_nomi)
            self._aniqlovchi.model_yuklash()
            log.info("Model tayyor: %s", self.strategiya_nomi)

    def aniqlash(self, rasm: np.ndarray, rasm_manzili: str = "") -> AniqlashNatijasi:
        """Sinxron aniqlash — to'g'ridan-to'g'ri natija qaytaradi.

        Parametrlar:
            rasm:         BGR numpy massivi.
            rasm_manzili: Manba fayl manzili (log uchun).

        Natija:
            AniqlashNatijasi (chizilgan_rasm bilan).
        """
        # Hali yuklanmagan bo'lsa, shu yerda lazy yuklash
        if not self._aniqlovchi.tayyor_mi():
            log.info("Model lazy yuklanmoqda: %s", self.strategiya_nomi)
            self._aniqlovchi.model_yuklash()

        balandlik, kenglik = rasm.shape[:2]
        boshlanish = time.perf_counter()

        obyektlar = self._aniqlovchi.aniqlash(
            rasm,
            min_aniqlik=self._sozlamalar.dnn.minimal_aniqlik,
        )

        ishlash_ms = (time.perf_counter() - boshlanish) * 1000

        natija = AniqlashNatijasi(
            rasm_manzili=rasm_manzili,
            aniqlash_vaqti=datetime.now(),
            obyektlar=obyektlar,
            ishlash_vaqti_ms=ishlash_ms,
            rasm_olchami=(balandlik, kenglik),
            strategiya_nomi=self.strategiya_nomi,
        )

        # Ramkalar chizish
        natija.chizilgan_rasm = _ramkalar_chizish(
            rasm,
            natija,
            self._sozlamalar.ramka_qalinlik,
            self._sozlamalar.shrift_olchami,
        )

        log.info(
            "Aniqlash tugadi: %d ta obyekt | %.0f ms | %s",
            natija.obyektlar_soni,
            natija.ishlash_vaqti_ms,
            self.strategiya_nomi,
        )
        return natija

    def asinxron_aniqlash(
        self,
        rasm: np.ndarray,
        rasm_manzili: str,
        natija_navbati: "queue.Queue[AniqlashNatijasi]",
        xato_navbati: "queue.Queue[Exception]",
        tugallandi_qaytarish: Callable | None = None,
    ) -> None:
        """Aniqlashni alohida threadda asinxron bajaradi.

        GUI bloklanmasin deb ishlatiladi.

        Parametrlar:
            rasm:               BGR numpy massivi.
            rasm_manzili:       Manba fayl manzili.
            natija_navbati:     Natija kelganda shu navbatga qo'yiladi.
            xato_navbati:       Xato bo'lsa shu navbatga qo'yiladi.
            tugallandi_qaytarish: Tugagach chaqiriladigan callback (ixtiyoriy).
        """

        def _ish() -> None:
            try:
                natija = self.aniqlash(rasm, rasm_manzili)
                natija_navbati.put(natija)
            except Exception as xato:
                xato_navbati.put(xato)
            finally:
                if tugallandi_qaytarish:
                    tugallandi_qaytarish()

        threading.Thread(target=_ish, daemon=True).start()
