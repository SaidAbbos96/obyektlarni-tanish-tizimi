"""Rasm ko'rsatish paneli — Canvas asosida.

Xususiyatlar:
  • Bo'sh holatda chiroyli placeholder (rasm ikonkasi + matn)
  • Canvasga bosish → fayl ochish dialogi
  • Drag & drop — tashqi fayllar qabul qilinadi (TkinterDnD2)
  • Rasm ostida boshqaruv tugmalari paneli
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional

from PIL import ImageTk
import numpy as np

from loyiha.vositalar.rasm_vositalari import (
    opencv_dan_pil,
    pil_dan_tkinter,
    panelga_moslash,
)

# Placeholder ranglar
_FONI = "#1e1e2e"
_CHEGARA = "#44475a"
_ASOSIY_RANG = "#6272a4"
_MATN_RANG = "#cdd6f4"
_IKKILAMCHI = "#585b70"

# Toolbar ranglar
_TB_FONI = "#313244"
_TB_BTN = "#45475a"
_TB_BTN_HOVER = "#585b70"
_TB_YASHIL = "#a6e3a1"
_TB_KOK = "#89b4fa"
_TB_SARIQ = "#f9e2af"
_TB_QIZIL = "#f38ba8"


def _tugma_yaratish(
    ota: tk.Widget,
    matn: str,
    buyruq: Callable,
    rang: str = _TB_KOK,
    eni: int = 12,
) -> tk.Button:
    """Toolbar uchun zamonaviy flat tugma yaratadi."""
    btn = tk.Button(
        ota,
        text=matn,
        command=buyruq,
        bg=_TB_BTN,
        fg=rang,
        activebackground=_TB_BTN_HOVER,
        activeforeground=rang,
        relief=tk.FLAT,
        bd=0,
        padx=10,
        pady=6,
        width=eni,
        font=("Segoe UI", 9, "bold"),
        cursor="hand2",
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=_TB_BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=_TB_BTN))
    return btn


class RasmPaneli:
    """Rasmni Canvas da ko'rsatuvchi komponent.

    Foydalanish:
        panel = RasmPaneli(ota, rasm_tanlash_cb, aniqlash_cb, saqlash_cb, tozalash_cb)
        panel.rasm_korsatish(bgr_massiv)
        panel.tozalash()
        panel.aniqlash_holatini_belgilash(True/False)
    """

    def __init__(
        self,
        ota: tk.Widget,
        rasm_tanlash_cb: Optional[Callable[[str], None]] = None,
        aniqlash_cb: Optional[Callable] = None,
        saqlash_cb: Optional[Callable] = None,
        tozalash_cb: Optional[Callable] = None,
    ) -> None:
        """Rasm panelini yaratadi.

        Parametrlar:
            ota:             Ota widget.
            rasm_tanlash_cb: Rasm manzili tanlanganda callback.
            aniqlash_cb:     Aniqlashni boshlash callback.
            saqlash_cb:      Natijani saqlash callback.
            tozalash_cb:     Rasmni tozalash callback.
        """
        self._tanlash_cb = rasm_tanlash_cb
        self._aniqlash_cb = aniqlash_cb
        self._saqlash_cb = saqlash_cb
        self._tozalash_cb = tozalash_cb

        self._asosiy = ttk.LabelFrame(ota, text="Rasm")
        self._asosiy.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Canvas (asosiy rasm maydoni)
        self._canvas = tk.Canvas(
            self._asosiy, bg=_FONI, cursor="hand2", highlightthickness=0
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

        # Boshqaruv tugmalari paneli (canvas ostida)
        self._toolbar = tk.Frame(self._asosiy, bg=_TB_FONI, pady=4)
        self._toolbar.pack(fill=tk.X, side=tk.BOTTOM)

        self._btn_ochish = _tugma_yaratish(
            self._toolbar,
            "📂  Rasm ochish",
            self._rasm_ochish_dialog,
            rang=_TB_KOK,
            eni=14,
        )
        self._btn_ochish.pack(side=tk.LEFT, padx=(8, 3))

        self._btn_aniqlash = _tugma_yaratish(
            self._toolbar,
            "▶  Aniqlashni boshlash",
            lambda: self._aniqlash_cb() if self._aniqlash_cb else None,
            rang=_TB_YASHIL,
            eni=18,
        )
        self._btn_aniqlash.pack(side=tk.LEFT, padx=3)

        self._btn_saqlash = _tugma_yaratish(
            self._toolbar,
            "💾  Saqlash",
            lambda: self._saqlash_cb() if self._saqlash_cb else None,
            rang=_TB_SARIQ,
            eni=10,
        )
        self._btn_saqlash.pack(side=tk.LEFT, padx=3)

        self._btn_tozalash = _tugma_yaratish(
            self._toolbar,
            "🗑  Tozalash",
            self._tozalash_ichki,
            rang=_TB_QIZIL,
            eni=10,
        )
        self._btn_tozalash.pack(side=tk.LEFT, padx=3)

        # Strategiya ko'rsatkichi (o'ng tomonda)
        self._strategiya_oz = tk.StringVar(value="haar")
        tk.Label(
            self._toolbar,
            textvariable=self._strategiya_oz,
            bg=_TB_FONI,
            fg=_IKKILAMCHI,
            font=("Segoe UI", 8),
        ).pack(side=tk.RIGHT, padx=(0, 10))
        tk.Label(
            self._toolbar,
            text="Strategiya:",
            bg=_TB_FONI,
            fg=_IKKILAMCHI,
            font=("Segoe UI", 8),
        ).pack(side=tk.RIGHT)

        # GC dan himoya
        self._tk_rasm: Optional[ImageTk.PhotoImage] = None
        self._joriy_bgr: Optional[np.ndarray] = None

        # Hodisalar
        self._canvas.bind("<Configure>", self._olcham_ozgardi)
        self._canvas.bind("<Button-1>", self._bosildi)

    # ------------------------------------------------------------------ #
    # Ochiq API
    # ------------------------------------------------------------------ #

    def rasm_korsatish(self, bgr_rasm: np.ndarray) -> None:
        """BGR numpy massivini canvasda ko'rsatadi."""
        self._joriy_bgr = bgr_rasm
        self._canvas.config(cursor="crosshair")
        self._chizish(bgr_rasm)

    def tozalash(self) -> None:
        """Rasmni o'chirib placeholder ko'rsatadi."""
        self._canvas.delete("all")
        self._tk_rasm = None
        self._joriy_bgr = None
        self._canvas.config(cursor="hand2")
        self._placeholder_chizish()

    def aniqlash_holatini_belgilash(self, jarayonda: bool) -> None:
        """Aniqlash tugmasi holatini yangilaydi.

        Parametrlar:
            jarayonda: True → tugma o'chiriladi (loading), False → yoqiladi.
        """
        holat = tk.DISABLED if jarayonda else tk.NORMAL
        matn = "⏳  Aniqlanmoqda…" if jarayonda else "▶  Aniqlashni boshlash"
        self._btn_aniqlash.config(state=holat, text=matn)

    def strategiya_nomi_yangilash(self, nom: str) -> None:
        """Toolbar da strategiya nomini yangilaydi.

        Parametrlar:
            nom: Strategiya nomi ('haar' yoki 'dnn').
        """
        self._strategiya_oz.set(nom)

    def drop_qabul_qilish(self, xom_manzil: str) -> None:
        """Drag&drop yoki tashqi manbadan kelgan fayl manzilini qayta ishlaydi."""
        manzil = xom_manzil.strip().strip("{}")
        if manzil and self._tanlash_cb:
            self._tanlash_cb(manzil)

    # ------------------------------------------------------------------ #
    # Ichki metodlar
    # ------------------------------------------------------------------ #

    def _rasm_ochish_dialog(self) -> None:
        """Fayl tanlash dialogini ochadi."""
        manzil = filedialog.askopenfilename(
            title="Rasm tanlang",
            filetypes=[
                ("Rasm fayllar", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif"),
                ("Barcha fayllar", "*.*"),
            ],
        )
        if manzil and self._tanlash_cb:
            self._tanlash_cb(manzil)

    def _tozalash_ichki(self) -> None:
        """Rasmni tozalab tashqi callback ni ham chaqiradi."""
        self.tozalash()
        if self._tozalash_cb:
            self._tozalash_cb()

    def _bosildi(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        """Canvas bosilganda fayl ochish dialogi (faqat bo'sh holatda)."""
        if self._joriy_bgr is not None:
            return  # Rasm bor — bosish kerak emas
        self._rasm_ochish_dialog()

    def _chizish(self, bgr_rasm: np.ndarray) -> None:
        """Rasmni canvasga joylashtiradi."""
        k = self._canvas.winfo_width() or 640
        b = self._canvas.winfo_height() or 480

        moslangan = panelga_moslash(bgr_rasm, k, b)
        pil_rasm = opencv_dan_pil(moslangan)
        self._tk_rasm = pil_dan_tkinter(pil_rasm)

        self._canvas.delete("all")
        self._canvas.create_image(k // 2, b // 2, image=self._tk_rasm, anchor=tk.CENTER)

    def _placeholder_chizish(self) -> None:
        """Bo'sh holat uchun chiroyli placeholder chizadi."""
        k = self._canvas.winfo_width() or 640
        b = self._canvas.winfo_height() or 480
        cx, cy = k // 2, b // 2

        # Markaziy ikonka bloki
        ikon_k, ikon_b = 120, 90
        ix1, iy1 = cx - ikon_k // 2, cy - ikon_b // 2 - 30
        ix2, iy2 = cx + ikon_k // 2, cy + ikon_b // 2 - 30

        # --- Rasm ikonkasi (canvas shapes) ---
        # Tashqi ramka
        self._canvas.create_rectangle(
            ix1,
            iy1,
            ix2,
            iy2,
            outline=_ASOSIY_RANG,
            width=3,
            fill=_CHEGARA,
        )
        # To'lqin chiziq (gorizontal) — ufq
        ufq_y = iy1 + int((iy2 - iy1) * 0.65)
        self._canvas.create_line(ix1, ufq_y, ix2, ufq_y, fill=_ASOSIY_RANG, width=1)
        # Tog' silueti (uchburchaklar)
        tog_mx = cx - 20
        tog_y_top = iy1 + 14
        self._canvas.create_polygon(
            tog_mx - 28,
            ufq_y,
            tog_mx,
            tog_y_top,
            tog_mx + 28,
            ufq_y,
            fill=_ASOSIY_RANG,
            outline="",
        )
        tog2_mx = cx + 22
        tog2_top = iy1 + 26
        self._canvas.create_polygon(
            tog2_mx - 20,
            ufq_y,
            tog2_mx,
            tog2_top,
            tog2_mx + 20,
            ufq_y,
            fill=_IKKILAMCHI,
            outline="",
        )
        # Quyosh
        qx, qy, qr = ix1 + 20, iy1 + 20, 10
        self._canvas.create_oval(
            qx - qr,
            qy - qr,
            qx + qr,
            qy + qr,
            fill="#f1fa8c",
            outline="",
        )
        # Kamera linzasi (pastki o'ng)
        lx, ly, lr = ix2 - 18, iy2 - 16, 8
        self._canvas.create_oval(
            lx - lr,
            ly - lr,
            lx + lr,
            ly + lr,
            fill="",
            outline=_MATN_RANG,
            width=2,
        )

        # --- Matnlar ---
        self._canvas.create_text(
            cx,
            iy2 + 18,
            text="Rasm yuklash",
            fill=_MATN_RANG,
            font=("Segoe UI", 16, "bold"),
        )
        self._canvas.create_text(
            cx,
            iy2 + 42,
            text="Bosing yoki faylni bu yerga tashlang",
            fill=_IKKILAMCHI,
            font=("Segoe UI", 10),
        )
        self._canvas.create_text(
            cx,
            iy2 + 60,
            text="PNG · JPG · BMP · TIFF",
            fill=_IKKILAMCHI,
            font=("Segoe UI", 9),
        )

    def _olcham_ozgardi(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        """Panel o'lchami o'zgarganda qayta chizadi."""
        if self._joriy_bgr is not None:
            self._chizish(self._joriy_bgr)
        else:
            self._canvas.delete("all")
            self._placeholder_chizish()
