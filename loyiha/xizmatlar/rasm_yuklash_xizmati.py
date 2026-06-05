"""Rasm yuklash xizmati — validatsiya va OpenCV ga o'tkazish."""

import logging
from pathlib import Path

import cv2
import numpy as np

from loyiha.modellar.xatolar import (
    RasmTopilmadiXatosi,
    NotogriFaqlFormatXatosi,
)
from loyiha.sozlamalar.sozlamalar import Sozlamalar
from loyiha.vositalar.rasm_vositalari import olchamga_keltirish

# Qo'llab-quvvatlanadigan rasm kengaytmalari
RUXSAT_FORMATLAR = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}

log = logging.getLogger("loyiha.rasm_yuklash")


class RasmYuklashXizmati:
    """Rasmni fayldan yuklash, validatsiya qilish va o'lchamini moslashtirish.

    Foydalanish:
        xizmat = RasmYuklashXizmati(sozlamalar)
        rasm = xizmat.yuklash('/rasmlar/test.jpg')
    """

    def __init__(self, sozlamalar: Sozlamalar) -> None:
        """Xizmatni sozlaydi.

        Parametrlar:
            sozlamalar: Ilova sozlamalari (o'lcham chegaralari uchun).
        """
        self._sozlamalar = sozlamalar

    def yuklash(self, manzil: str) -> np.ndarray:
        """Ko'rsatilgan manzildan rasmni yuklaydi.

        Parametrlar:
            manzil: Rasm fayli manzili (mutlaq yoki nisbiy).

        Natija:
            BGR formatdagi numpy massivi.

        Istisno:
            RasmTopilmadiXatosi:     Fayl mavjud emas.
            NotogriFaqlFormatXatosi: Format qo'llanilmaydi.
        """
        yol = Path(manzil)

        # Fayl mavjudligini tekshirish
        if not yol.is_file():
            raise RasmTopilmadiXatosi(f"Rasm fayli topilmadi: {manzil}")

        # Format tekshirish
        if yol.suffix.lower() not in RUXSAT_FORMATLAR:
            raise NotogriFaqlFormatXatosi(
                f"Qo'llanilmaydigan format: '{yol.suffix}'. "
                f"Ruxsat etilganlar: {', '.join(sorted(RUXSAT_FORMATLAR))}"
            )

        # Rasmni yuklash
        rasm = cv2.imread(str(yol))
        if rasm is None:
            raise NotogriFaqlFormatXatosi(
                f"Rasm o'qilmadi (buzilgan fayl bo'lishi mumkin): {manzil}"
            )

        # O'lchamni cheklash
        rasm = olchamga_keltirish(
            rasm,
            self._sozlamalar.maks_kenglik,
            self._sozlamalar.maks_balandlik,
        )

        log.info(
            "Rasm yuklandi: %s | O'lcham: %dx%d",
            yol.name,
            rasm.shape[1],
            rasm.shape[0],
        )
        return rasm
