"""Natijalarni faylga saqlash xizmati."""

import json
import logging
from pathlib import Path

import cv2
import numpy as np

from loyiha.modellar.aniqlash_natijasi import AniqlashNatijasi
from loyiha.modellar.xatolar import SaqlashXatosi
from loyiha.sozlamalar.sozlamalar import Sozlamalar
from loyiha.vositalar.vaqt_vositalari import hozir_formatlangan
from loyiha.vositalar.fayl_vositalari import papka_yaratish

log = logging.getLogger("loyiha.saqlash")


class NatijaSaqlashXizmati:
    """Aniqlash natijasini PNG va JSON formatda saqlash.

    Foydalanish:
        xizmat = NatijaSaqlashXizmati(sozlamalar)
        png_yol, json_yol = xizmat.saqlash(rasm, natija)
    """

    def __init__(self, sozlamalar: Sozlamalar) -> None:
        """Xizmatni sozlaydi.

        Parametrlar:
            sozlamalar: Ilova sozlamalari (chiquvchi papka uchun).
        """
        self._sozlamalar = sozlamalar

    def saqlash(
        self, asl_rasm: np.ndarray, natija: AniqlashNatijasi
    ) -> tuple[str, str]:
        """Chizilgan rasmni PNG va hisobotni JSON sifatida saqlaydi.

        Parametrlar:
            asl_rasm: Manba BGR rasm (zaruriy emas, chizilgan ishlatiladi).
            natija:   AniqlashNatijasi (chizilgan_rasm ni o'z ichiga oladi).

        Natija:
            (png_manzil, json_manzil) to'plami.

        Istisno:
            SaqlashXatosi: Yozib bo'lmasa.
        """
        # Chiquvchi papkani yaratish
        papka = papka_yaratish(self._sozlamalar.chiquvchi_papka)
        vaqt = hozir_formatlangan()

        # PNG saqlash
        chizilgan = natija.chizilgan_rasm
        if chizilgan is None:
            chizilgan = asl_rasm

        png_manzil = str(papka / f"{vaqt}_natija.png")
        try:
            muvaffaqiyat = cv2.imwrite(png_manzil, chizilgan)
            if not muvaffaqiyat:
                raise SaqlashXatosi(f"PNG saqlanmadi: {png_manzil}")
        except cv2.error as xato:
            raise SaqlashXatosi(f"PNG yozish xatosi: {xato}") from xato

        # JSON hisobot saqlash
        json_manzil = str(papka / f"{vaqt}_hisobot.json")
        try:
            Path(json_manzil).write_text(
                json.dumps(natija.json_ga(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as xato:
            raise SaqlashXatosi(f"JSON saqlanmadi: {xato}") from xato

        log.info("Natija saqlandi: %s", png_manzil)
        return png_manzil, json_manzil

    def skrinshot_saqlash(self, rasm: np.ndarray, papka: str | None = None) -> str:
        """GUI skrinshotini saqlaydi.

        Parametrlar:
            rasm:  BGR numpy massivi.
            papka: Saqlash papkasi. None bo'lsa chiquvchi papkadan foydalanadi.

        Natija:
            Saqlangan fayl manzili.
        """
        manzil = papka or "media/skrinshotlar"
        yol = papka_yaratish(manzil)
        vaqt = hozir_formatlangan()
        fayl = str(yol / f"{vaqt}_skrinshot.png")
        cv2.imwrite(fayl, rasm)
        log.info("Skrinshot saqlandi: %s", fayl)
        return fayl
