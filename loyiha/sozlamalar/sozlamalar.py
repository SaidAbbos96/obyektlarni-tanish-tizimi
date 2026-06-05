"""Sozlamalar — sozlamalar.json faylini o'qish va yozish."""

from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

from loyiha.modellar.xatolar import SozlamalarXatosi
from . import standart


@dataclass
class HaarSozlamalari:
    """Haar Cascade aniqlash sozlamalari."""

    min_qoshni: int = standart.HAAR_MIN_QOSHNI
    olcham_koeffitsienti: float = standart.HAAR_OLCHAM_KOEF
    minimal_olcham: List[int] = field(
        default_factory=lambda: list(standart.HAAR_MINIMAL_OLCHAM)
    )


@dataclass
class DnnSozlamalari:
    """OpenCV DNN aniqlash sozlamalari."""

    minimal_aniqlik: float = standart.DNN_MIN_ANIQLIK
    olcham: List[int] = field(default_factory=lambda: list(standart.DNN_OLCHAM))
    orta_qiymat: List[float] = field(
        default_factory=lambda: list(standart.DNN_ORTA_QIYMAT)
    )
    koeffitsient: float = standart.DNN_KOEFFITSIENT


@dataclass
class AniqlashSozlamalari:
    """Aniqlash tizimi uchun sozlamalar."""

    faol_strategiya: str = standart.STANDART_STRATEGIYA
    haar: HaarSozlamalari = field(default_factory=HaarSozlamalari)
    dnn: DnnSozlamalari = field(default_factory=DnnSozlamalari)


@dataclass
class Sozlamalar:
    """Ilovaning barcha sozlamalari bir joyda.

    Foydalanish:
        soz = Sozlamalar.yuklash()
        soz = Sozlamalar.standart()
    """

    versiya: str = "1.0.0"
    faol_strategiya: str = standart.STANDART_STRATEGIYA
    maks_kenglik: int = standart.MAKS_KENGLIK
    maks_balandlik: int = standart.MAKS_BALANDLIK
    ramka_qalinlik: int = standart.RAMKA_QALINLIK
    shrift_olchami: float = standart.SHRIFT_OLCHAMI
    jurnal_daraja: str = standart.JURNAL_DARAJA
    jurnal_fayl: str = "jurnal/loyiha.log"
    chiquvchi_papka: str = "media/chiquvchi"
    kiruvchi_papka: str = "media/kiruvchi"
    modellar_papka: str = "loyiha/model_boshqaruv/modellar"
    haar: HaarSozlamalari = field(default_factory=HaarSozlamalari)
    dnn: DnnSozlamalari = field(default_factory=DnnSozlamalari)

    @classmethod
    def standart(cls) -> "Sozlamalar":
        """Standart sozlamalar bilan yangi nusxa qaytaradi."""
        return cls()

    @classmethod
    def yuklash(cls, manzil: str = "sozlamalar.json") -> "Sozlamalar":
        """sozlamalar.json faylidan sozlamalarni o'qiydi.

        Parametrlar:
            manzil: JSON fayl manzili.

        Natija:
            Sozlamalar nusxasi.

        Istisno:
            SozlamalarXatosi: Fayl o'qib bo'lmasa yoki noto'g'ri format.
        """
        yol = Path(manzil)
        if not yol.exists():
            # Fayl yo'q — standart qaytaramiz
            return cls.standart()
        try:
            matn = yol.read_text(encoding="utf-8")
            ma_lumot = json.loads(matn)
        except (OSError, json.JSONDecodeError) as xato:
            raise SozlamalarXatosi(f"sozlamalar.json o'qilmadi: {xato}") from xato

        # JSON dan qiymatlarni olamiz, yo'q bo'lsa standart qoladi
        soz = cls.standart()
        soz.versiya = ma_lumot.get("versiya", soz.versiya)

        aniqlash = ma_lumot.get("aniqlash", {})
        soz.faol_strategiya = aniqlash.get("faol_strategiya", soz.faol_strategiya)

        haar_data = aniqlash.get("haar", {})
        soz.haar.min_qoshni = haar_data.get("min_qoshni", soz.haar.min_qoshni)

        dnn_data = aniqlash.get("dnn", {})
        soz.dnn.minimal_aniqlik = dnn_data.get(
            "minimal_aniqlik", soz.dnn.minimal_aniqlik
        )

        rasm = ma_lumot.get("rasm", {})
        soz.maks_kenglik = rasm.get("maksimal_kenglik", soz.maks_kenglik)
        soz.maks_balandlik = rasm.get("maksimal_balandlik", soz.maks_balandlik)

        jurnal = ma_lumot.get("jurnal", {})
        soz.jurnal_daraja = jurnal.get("daraja", soz.jurnal_daraja)
        soz.jurnal_fayl = jurnal.get("fayl", soz.jurnal_fayl)

        papkalar = ma_lumot.get("papkalar", {})
        soz.chiquvchi_papka = papkalar.get("chiquvchi", soz.chiquvchi_papka)
        soz.kiruvchi_papka = papkalar.get("kiruvchi", soz.kiruvchi_papka)
        soz.modellar_papka = papkalar.get("modellar", soz.modellar_papka)

        return soz

    def saqlash(self, manzil: str = "sozlamalar.json") -> None:
        """Joriy sozlamalarni JSON fayliga yozadi.

        Parametrlar:
            manzil: Saqlash uchun JSON fayl manzili.
        """
        ma_lumot = {
            "versiya": self.versiya,
            "aniqlash": {
                "faol_strategiya": self.faol_strategiya,
                "haar": {
                    "min_qoshni": self.haar.min_qoshni,
                    "olcham_koeffitsienti": self.haar.olcham_koeffitsienti,
                },
                "dnn": {
                    "minimal_aniqlik": self.dnn.minimal_aniqlik,
                },
            },
            "rasm": {
                "maksimal_kenglik": self.maks_kenglik,
                "maksimal_balandlik": self.maks_balandlik,
            },
            "jurnal": {
                "daraja": self.jurnal_daraja,
                "fayl": self.jurnal_fayl,
            },
            "papkalar": {
                "kiruvchi": self.kiruvchi_papka,
                "chiquvchi": self.chiquvchi_papka,
                "modellar": self.modellar_papka,
            },
        }
        try:
            Path(manzil).write_text(
                json.dumps(ma_lumot, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as xato:
            raise SozlamalarXatosi(f"sozlamalar.json saqlanmadi: {xato}") from xato
