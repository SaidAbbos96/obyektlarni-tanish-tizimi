"""Asosiy oyna — barcha komponentlarni birlashtiruvchi."""

import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES

    _DND_MAVJUD = True
except ImportError:
    _DND_MAVJUD = False

from loyiha.modellar.aniqlash_natijasi import AniqlashNatijasi
from loyiha.sozlamalar.sozlamalar import Sozlamalar
from loyiha.taqdimotchi.asosiy_taqdimotchi import AsosiyTaqdimotchi
from loyiha.taqdimotchi.hodisalar import Hodisa, HodisaTuri
from .menyu import MenyuSatri
from .holat_satri import HolatSatri
from .rasm_paneli import RasmPaneli
from .natija_paneli import NatijaPanel
from .karusel import RasmKarusel

# Navbat tekshirish oralig'i (ms)
NAVBAT_INTERVAL = 150


class AsosiyOyna:
    """Tkinter asosiy oyna.

    Barcha GUI komponentlarini yaratadi, taqdimotchi bilan bog'laydi.

    Foydalanish:
        oyna = AsosiyOyna(sozlamalar)
        oyna.ishga_tushirish()
    """

    def __init__(self, sozlamalar: Sozlamalar) -> None:
        """Asosiy oynani yaratadi.

        Parametrlar:
            sozlamalar: Ilova sozlamalari.
        """
        self._sozlamalar = sozlamalar
        self._joriy_rasm: np.ndarray | None = None
        self._joriy_natija: AniqlashNatijasi | None = None

        # Tkinter oyna — DnD mavjud bo'lsa TkinterDnD.Tk ishlatamiz
        if _DND_MAVJUD:
            self._ildiz = TkinterDnD.Tk()
        else:
            self._ildiz = tk.Tk()
        self._ildiz.title("Obyektlarni Tanish Tizimi — v3.0")
        self._ildiz.geometry("1100x720")
        self._ildiz.minsize(800, 560)

        # Taqdimotchi (hodisa callback bilan)
        self._taqdimotchi = AsosiyTaqdimotchi(sozlamalar, self._hodisani_qabul_qilish)

        # Komponentlar
        self._menyu = MenyuSatri(
            self._ildiz,
            rasm_och=self._rasm_ochish,
            natija_saqlash=self._natijani_saqlash,
            aniqlash_boshlash=self._aniqlashni_boshlash,
            haar_tanlash=lambda: self._strategiya_almashtirish("haar"),
            dnn_tanlash=lambda: self._strategiya_almashtirish("dnn"),
            haqida_ochish=self._haqida_oynasi,
        )
        self._holat = HolatSatri(self._ildiz)

        # Asosiy panel (rasm + natija)
        markaziy = tk.Frame(self._ildiz)
        markaziy.pack(fill=tk.BOTH, expand=True)

        self._rasm_panel = RasmPaneli(
            markaziy,
            rasm_tanlash_cb=self._taqdimotchi.rasm_tanlash,
            aniqlash_cb=self._aniqlashni_boshlash,
            saqlash_cb=self._natijani_saqlash,
            tozalash_cb=self._tozalash,
        )
        self._natija_panel = NatijaPanel(markaziy)

        # Drag & Drop ulash (tkinterdnd2 mavjud bo'lsa)
        if _DND_MAVJUD:
            self._rasm_panel._canvas.drop_target_register(DND_FILES)  # type: ignore[attr-defined]
            self._rasm_panel._canvas.dnd_bind(  # type: ignore[attr-defined]
                "<<Drop>>",
                lambda e: self._rasm_panel.drop_qabul_qilish(e.data),
            )

        # Pastki karusel
        self._karusel = RasmKarusel(
            self._ildiz,
            rasm_tanlash_cb=self._taqdimotchi.rasm_tanlash,
        )
        self._karusel.yangilash(sozlamalar.kiruvchi_papka)

        # Klaviatura qisqa yo'llari
        self._ildiz.bind("<Control-o>", lambda _e: self._rasm_ochish())
        self._ildiz.bind("<Control-s>", lambda _e: self._natijani_saqlash())
        self._ildiz.bind("<F5>", lambda _e: self._aniqlashni_boshlash())

    # ------------------------------------------------------------------ #
    # Ishga tushirish
    # ------------------------------------------------------------------ #

    def ishga_tushirish(self) -> None:
        """Oynani ko'rsatadi va hodisa tsiklini boshlaydi."""
        self._taqdimotchi.boshlash()
        self._navbatni_tekshirish()
        self._ildiz.mainloop()

    # ------------------------------------------------------------------ #
    # Hodisa callback
    # ------------------------------------------------------------------ #

    def _hodisani_qabul_qilish(self, hodisa: Hodisa) -> None:
        """Taqdimotchidan kelgan hodisalarni qayta ishlaydi.

        Bu metod GUI threadida chaqirilishi kafolatlanmagan —
        Tkinter `after()` orqali chaqiriladi.

        Parametrlar:
            hodisa: Taqdimotchidan kelgan Hodisa.
        """
        self._ildiz.after(0, lambda: self._hodisani_bajarish(hodisa))

    def _hodisani_bajarish(self, hodisa: Hodisa) -> None:
        """Hodisaga mos UI yangilashni amalga oshiradi."""
        tur = hodisa.tur

        if tur == HodisaTuri.RASM_YUKLANDI:
            rasm: np.ndarray = hodisa.data
            self._joriy_rasm = rasm
            self._rasm_panel.rasm_korsatish(rasm)
            self._holat.oddiy_rang()
            self._holat.xabar_korsatish("Rasm yuklandi. F5 bilan aniqlashni boshlang.")
            self._karusel.yangilash(self._sozlamalar.kiruvchi_papka)

        elif tur == HodisaTuri.RASM_YUKLANMADI:
            self._holat.xato_korsatish(str(hodisa.data))

        elif tur == HodisaTuri.ANIQLASH_BOSHLANDI:
            self._holat.yuklanish_korsatish(True)
            self._holat.oddiy_rang()
            self._holat.xabar_korsatish("Aniqlash amalga oshirilmoqda…")
            self._rasm_panel.aniqlash_holatini_belgilash(True)

        elif tur == HodisaTuri.ANIQLASH_TUGADI:
            natija: AniqlashNatijasi = hodisa.data
            self._joriy_natija = natija
            self._holat.yuklanish_korsatish(False)
            self._holat.oddiy_rang()
            self._holat.xabar_korsatish(
                f"{natija.obyektlar_soni} ta obyekt aniqlandi "
                f"({natija.ishlash_vaqti_ms:.0f} ms)"
            )
            self._rasm_panel.aniqlash_holatini_belgilash(False)
            if natija.chizilgan_rasm is not None:
                self._rasm_panel.rasm_korsatish(natija.chizilgan_rasm)
            self._natija_panel.natijani_korsatish(natija)

        elif tur == HodisaTuri.ANIQLASH_XATOSI:
            self._holat.yuklanish_korsatish(False)
            self._holat.xato_korsatish(str(hodisa.data))
            self._rasm_panel.aniqlash_holatini_belgilash(False)
            messagebox.showerror("Aniqlash xatosi", str(hodisa.data))

        elif tur == HodisaTuri.STRATEGIYA_ALMASHDI:
            nom: str = hodisa.data
            self._holat.oddiy_rang()
            self._holat.xabar_korsatish(f"Strategiya: {nom}")
            self._menyu.strategiyani_belgilash(nom)
            self._rasm_panel.strategiya_nomi_yangilash(nom)

        elif tur == HodisaTuri.HOLAT_YANGILANDI:
            # Ogohlantirish — faqat dialog, strategiya o'zgargan holda ishlaydi
            messagebox.showwarning("Diqqat", str(hodisa.data))

        elif tur == HodisaTuri.NATIJA_SAQLANDI:
            self._holat.oddiy_rang()
            self._holat.xabar_korsatish(f"Saqlandi: {hodisa.data}")

        elif tur == HodisaTuri.XATO_YUZAGA_KELDI:
            self._holat.yuklanish_korsatish(False)
            self._holat.xato_korsatish(str(hodisa.data))
            messagebox.showerror("Xato", str(hodisa.data))

    # ------------------------------------------------------------------ #
    # GUI buyruqlari
    # ------------------------------------------------------------------ #

    def _rasm_ochish(self) -> None:
        """Fayl tanlash dialogi va rasmni yuklash."""
        manzil = filedialog.askopenfilename(
            title="Rasm tanlang",
            filetypes=[
                ("Rasm fayllar", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif"),
                ("Barcha fayllar", "*.*"),
            ],
        )
        if manzil:
            self._taqdimotchi.rasm_tanlash(manzil)

    def _aniqlashni_boshlash(self) -> None:
        """Aniqlashni ishga tushiradi."""
        self._taqdimotchi.aniqlashni_boshlash()

    def _tozalash(self) -> None:
        """Joriy rasmni va natijani tozalaydi."""
        self._joriy_rasm = None
        self._joriy_natija = None
        self._natija_panel.tozalash()
        self._holat.oddiy_rang()
        self._holat.xabar_korsatish("Tayyor.")

    def _natijani_saqlash(self) -> None:
        """Joriy natijani saqlaydi."""
        if self._joriy_natija is None or self._joriy_rasm is None:
            messagebox.showinfo("Ma'lumot", "Saqlash uchun avval aniqlash bajaring.")
            return
        self._taqdimotchi.natijani_saqlash(self._joriy_rasm, self._joriy_natija)

    def _strategiya_almashtirish(self, nom: str) -> None:
        """Ko'rsatilgan strategiyani faollashtiradi."""
        self._taqdimotchi.strategiyani_almashtirish(nom)

    def _haqida_oynasi(self) -> None:
        """Ilova haqida dialog ko'rsatadi."""
        matn = (
            "Obyektlarni Tanish Tizimi v3.0\n\n"
            "Talaba: Xudoyqulov SaidAbbos Salim o'g'li\n"
            "Guruh: KI-032-01 | Masofaviy ta'lim\n"
            "TATU Samarqand filiali\n\n"
            "Ishlatilgan texnologiyalar:\n"
            "  Python 3.12 | OpenCV | Tkinter | Pillow"
        )
        messagebox.showinfo("Ilova haqida", matn)

    # ------------------------------------------------------------------ #
    # Navbat kuzatuv tsikli
    # ------------------------------------------------------------------ #

    def _navbatni_tekshirish(self) -> None:
        """Asinxron natijalar uchun navbatni tekshiradi.

        Har NAVBAT_INTERVAL millisekund chaqiriladi.
        """
        self._taqdimotchi.navbatni_tekshirish()
        self._ildiz.after(NAVBAT_INTERVAL, self._navbatni_tekshirish)
