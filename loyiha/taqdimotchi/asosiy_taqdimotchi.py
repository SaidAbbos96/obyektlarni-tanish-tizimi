"""Asosiy taqdimotchi — GUI va xizmatlar o'rtasidagi ko'prik."""

import logging
import queue
from typing import Callable

import numpy as np

from loyiha.aniqlash import aniqlovchi_yaratish
from loyiha.aniqlash.dnn_aniqlovchi import DnnAniqlovchi
from loyiha.modellar.aniqlash_natijasi import AniqlashNatijasi
from loyiha.sozlamalar.sozlamalar import Sozlamalar
from loyiha.xizmatlar import (
    RasmYuklashXizmati,
    ObyektAniqlovchiXizmat,
    NatijaSaqlashXizmati,
)
from .hodisalar import Hodisa, HodisaTuri

log = logging.getLogger("loyiha.taqdimotchi")


class AsosiyTaqdimotchi:
    """Barcha GUI komponentlari bilan ishlovchi taqdimotchi.

    GUI hech qanday biznes mantiqni bilmasligi kerak —
    faqat taqdimotchiga hodisalar jo'natadi va javob kutadi.

    Foydalanish:
        taqdimotchi = AsosiyTaqdimotchi(sozlamalar, hodisa_chaqiruvchi)
        taqdimotchi.boshlash()
    """

    def __init__(
        self,
        sozlamalar: Sozlamalar,
        hodisa_chaqiruv: Callable[[Hodisa], None],
    ) -> None:
        """Taqdimotchini sozlaydi.

        Parametrlar:
            sozlamalar:     Ilova sozlamalari.
            hodisa_chaqiruv: GUI dan keladigan hodisalar qabul qiluvchi.
        """
        self._sozlamalar = sozlamalar
        self._hodisa_chaqiruv = hodisa_chaqiruv

        # Xizmatlar
        self._rasm_yuklash = RasmYuklashXizmati(sozlamalar)
        self._saqlash = NatijaSaqlashXizmati(sozlamalar)

        # Aniqlovchi
        aniqlovchi = aniqlovchi_yaratish(sozlamalar.faol_strategiya, sozlamalar)
        self._aniqlovchi_xizmat = ObyektAniqlovchiXizmat(aniqlovchi, sozlamalar)

        # Navbatlar
        self._natija_navbat: "queue.Queue[AniqlashNatijasi]" = queue.Queue()
        self._xato_navbat: "queue.Queue[Exception]" = queue.Queue()

        # Joriy holat
        self._joriy_rasm: np.ndarray | None = None
        self._joriy_manzil: str = ""

    def boshlash(self) -> None:
        """Strategiya modelini yuklaydi (ilovani ishga tushirishda)."""
        try:
            self._aniqlovchi_xizmat.strategiyani_yuklash()
        except Exception as xato:
            log.error("Model yuklanmadi: %s", xato)
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.XATO_YUZAGA_KELDI, str(xato)))

    # ------------------------------------------------------------------ #
    # Rasm ishlash
    # ------------------------------------------------------------------ #

    def rasm_tanlash(self, manzil: str) -> None:
        """Tanlangan faylni yuklaydi va GUI ga xabar beradi.

        Parametrlar:
            manzil: Rasm fayli manzili.
        """
        self._hodisa_chaqiruv(Hodisa(HodisaTuri.RASM_TANLANDI, manzil))
        try:
            rasm = self._rasm_yuklash.yuklash(manzil)
            self._joriy_rasm = rasm
            self._joriy_manzil = manzil
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.RASM_YUKLANDI, rasm))
        except Exception as xato:
            log.error("Rasm yuklanmadi: %s", xato)
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.RASM_YUKLANMADI, str(xato)))

    def aniqlashni_boshlash(self) -> None:
        """Asinxron aniqlashni ishga tushiradi.

        Aniqlash tugagach `navbatni_tekshirish()` natijani topadi.
        """
        if self._joriy_rasm is None:
            self._hodisa_chaqiruv(
                Hodisa(
                    HodisaTuri.XATO_YUZAGA_KELDI,
                    "Avval rasm yuklang.",
                )
            )
            return

        self._hodisa_chaqiruv(Hodisa(HodisaTuri.ANIQLASH_BOSHLANDI))
        self._aniqlovchi_xizmat.asinxron_aniqlash(
            self._joriy_rasm,
            self._joriy_manzil,
            self._natija_navbat,
            self._xato_navbat,
        )

    def navbatni_tekshirish(self) -> None:
        """Natija navbatini tekshirib, GUI ga hodisa yuboradi.

        GUI dagi `after()` tsikli bu metodini chaqiradi.
        """
        # Natija kelganmi?
        try:
            natija = self._natija_navbat.get_nowait()
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.ANIQLASH_TUGADI, natija))
        except queue.Empty:
            pass

        # Xato kelganmi?
        try:
            xato = self._xato_navbat.get_nowait()
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.ANIQLASH_XATOSI, str(xato)))
        except queue.Empty:
            pass

    # ------------------------------------------------------------------ #
    # Strategiya almashtirish
    # ------------------------------------------------------------------ #

    def strategiyani_almashtirish(self, strategiya_nomi: str) -> None:
        """Faol strategiyani almashtiradi.

        DNN tanlansa va model fayllari yo'q bo'lsa, xato chiqarmaydi —
        ogohlantirish xabari ko'rsatiladi. Model aniqlash boshlanganda yuklanadi.

        Parametrlar:
            strategiya_nomi: Yangi strategiya nomi ('haar' yoki 'dnn').
        """
        try:
            yangi = aniqlovchi_yaratish(strategiya_nomi, self._sozlamalar)
            self._aniqlovchi_xizmat.strategiyani_almashtirish(yangi)
            self._sozlamalar.faol_strategiya = strategiya_nomi
            self._hodisa_chaqiruv(
                Hodisa(HodisaTuri.STRATEGIYA_ALMASHDI, strategiya_nomi)
            )

            # DNN uchun model fayllari tekshiruvi (ogohlantiruv)
            if isinstance(yangi, DnnAniqlovchi) and not yangi.model_fayllar_mavjud():
                ogohlantirish = (
                    "DNN model fayllari topilmadi.\n"
                    f"'{self._sozlamalar.modellar_papka}' papkasiga qo'ying:\n"
                    "  • MobileNetSSD_deploy.prototxt\n"
                    "  • MobileNetSSD_deploy.caffemodel\n\n"
                    "Yuklab olish: https://github.com/chuanqi305/MobileNet-SSD"
                )
                self._hodisa_chaqiruv(
                    Hodisa(HodisaTuri.HOLAT_YANGILANDI, ogohlantirish)
                )
        except Exception as xato:
            log.error("Strategiya almashtirilmadi: %s", xato)
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.XATO_YUZAGA_KELDI, str(xato)))

    # ------------------------------------------------------------------ #
    # Natija saqlash
    # ------------------------------------------------------------------ #

    def natijani_saqlash(
        self,
        asl_rasm: np.ndarray,
        natija: AniqlashNatijasi,
    ) -> None:
        """Aniqlash natijasini PNG va JSON sifatida saqlaydi.

        Parametrlar:
            asl_rasm: Manba BGR rasm.
            natija:   AniqlashNatijasi.
        """
        try:
            png_yol, _ = self._saqlash.saqlash(asl_rasm, natija)
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.NATIJA_SAQLANDI, png_yol))
        except Exception as xato:
            log.error("Natija saqlanmadi: %s", xato)
            self._hodisa_chaqiruv(Hodisa(HodisaTuri.XATO_YUZAGA_KELDI, str(xato)))
