"""Pastki karusel — media/kiruvchi papkasidagi rasmlar thumbnaillari."""

import os
from pathlib import Path
from typing import Callable, List, Optional

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Thumbnail o'lchami (px)
THUMB_K = 110
THUMB_B = 82
THUMB_PAD = 3

# Qo'llab-quvvatlanadigan kengaytmalar
RASM_KENGAYTMALAR = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}

# Ranglar
_FONI = "#1e1e2e"
_TANLANGAN = "#89b4fa"
_HOVER_CHEGARA = "#6272a4"


class RasmKarusel:
    """Papkadagi rasmlarni gorizontal skrollable karusel sifatida ko'rsatadi.

    Foydalanish:
        karusel = RasmKarusel(ota, tanlash_cb)
        karusel.yangilash("media/kiruvchi")
    """

    def __init__(
        self,
        ota: tk.Widget,
        rasm_tanlash_cb: Callable[[str], None],
    ) -> None:
        """Karuselni yaratadi.

        Parametrlar:
            ota:             Ota widget.
            rasm_tanlash_cb: Rasm tanlanganda chaqiriladigan callback.
        """
        self._tanlash_cb = rasm_tanlash_cb
        self._thumb_refs: List[ImageTk.PhotoImage] = []
        self._joriy_papka: str = ""

        # Tashqi LabelFrame
        self._asosiy = ttk.LabelFrame(ota, text="Rasmlar — media/kiruvchi")
        self._asosiy.pack(side=tk.BOTTOM, fill=tk.X, padx=4, pady=(0, 4))

        # Canvas + gorizontal scrollbar
        self._canvas = tk.Canvas(
            self._asosiy,
            height=THUMB_B + 20,
            bg=_FONI,
            highlightthickness=0,
        )
        self._skroll = ttk.Scrollbar(
            self._asosiy, orient=tk.HORIZONTAL, command=self._canvas.xview
        )
        self._canvas.configure(xscrollcommand=self._skroll.set)

        self._skroll.pack(side=tk.BOTTOM, fill=tk.X)
        self._canvas.pack(side=tk.TOP, fill=tk.X)

        # Thumbnaillar joylashadigan ichki frame
        self._ichki = tk.Frame(self._canvas, bg=_FONI)
        self._canvas.create_window((0, 0), window=self._ichki, anchor=tk.NW)
        self._ichki.bind("<Configure>", self._ichki_olcham_ozgardi)

        # Mousewheel scroll
        self._canvas.bind("<MouseWheel>", self._aylantirish)

        # Bo'sh holat matni
        self._bosh_label = tk.Label(
            self._ichki,
            text="Papkada rasm topilmadi  (media/kiruvchi)",
            bg=_FONI,
            fg="#585b70",
            font=("Segoe UI", 9),
        )
        self._bosh_label.pack(padx=10, pady=12)

    # ------------------------------------------------------------------ #
    # Ochiq API
    # ------------------------------------------------------------------ #

    def yangilash(self, papka_manzili: str) -> None:
        """Papkadagi rasmlarni qayta yuklaydi.

        Parametrlar:
            papka_manzili: Rasm fayllari joylashgan papka.
        """
        self._joriy_papka = papka_manzili

        # Eski widgetlarni tozalash
        for widget in self._ichki.winfo_children():
            widget.destroy()
        self._thumb_refs.clear()

        papka = Path(papka_manzili)
        if not papka.is_dir():
            self._bosh_label = tk.Label(
                self._ichki,
                text=f"Papka topilmadi: {papka_manzili}",
                bg=_FONI,
                fg="#585b70",
                font=("Segoe UI", 9),
            )
            self._bosh_label.pack(padx=10, pady=12)
            return

        fayllar = sorted(
            [f for f in papka.iterdir() if f.suffix.lower() in RASM_KENGAYTMALAR]
        )

        if not fayllar:
            self._bosh_label = tk.Label(
                self._ichki,
                text="Papkada rasm topilmadi",
                bg=_FONI,
                fg="#585b70",
                font=("Segoe UI", 9),
            )
            self._bosh_label.pack(padx=10, pady=12)
            return

        for fayl in fayllar:
            self._thumbnail_qoshish(fayl)

    # ------------------------------------------------------------------ #
    # Ichki metodlar
    # ------------------------------------------------------------------ #

    def _thumbnail_qoshish(self, fayl_yol: Path) -> None:
        """Bitta thumbnail widget yaratib ichki framega qo'shadi."""
        try:
            img = Image.open(fayl_yol)
            img.thumbnail((THUMB_K, THUMB_B), Image.LANCZOS)

            # Bir xil o'lchamdagi qora fon — barcha thumbnaillar bir hil
            fon = Image.new("RGB", (THUMB_K, THUMB_B), (30, 30, 46))
            x_offs = (THUMB_K - img.width) // 2
            y_offs = (THUMB_B - img.height) // 2
            fon.paste(img, (x_offs, y_offs))

            tk_img = ImageTk.PhotoImage(fon)
            self._thumb_refs.append(tk_img)

            # Konteyner frame (chegara effekti uchun)
            konteyner = tk.Frame(self._ichki, bg=_FONI, padx=1, pady=1)
            konteyner.pack(side=tk.LEFT, padx=THUMB_PAD, pady=6)

            # Rasm label
            label = tk.Label(
                konteyner,
                image=tk_img,
                bg=_FONI,
                cursor="hand2",
                relief=tk.FLAT,
            )
            label.pack()

            # Fayl nomi (qisqartirilgan)
            nom = fayl_yol.name
            if len(nom) > 14:
                nom = nom[:11] + "…"
            tk.Label(
                konteyner,
                text=nom,
                bg=_FONI,
                fg="#585b70",
                font=("Segoe UI", 7),
            ).pack()

            # Hover va click
            def _enter(e, k=konteyner, lb=label):
                k.config(bg=_HOVER_CHEGARA)
                lb.config(bg=_HOVER_CHEGARA)

            def _leave(e, k=konteyner, lb=label):
                k.config(bg=_FONI)
                lb.config(bg=_FONI)

            manzil = str(fayl_yol)
            label.bind("<Button-1>", lambda e, m=manzil: self._tanlash_cb(m))
            label.bind("<Enter>", _enter)
            label.bind("<Leave>", _leave)
            konteyner.bind("<Enter>", _enter)
            konteyner.bind("<Leave>", _leave)
            konteyner.bind("<Button-1>", lambda e, m=manzil: self._tanlash_cb(m))

        except Exception:
            pass  # Buzilgan fayl — o'tkazib yuboriladi

    def _ichki_olcham_ozgardi(self, _e: tk.Event) -> None:  # type: ignore[type-arg]
        """Ichki frame o'lchami o'zgarganda scroll regionini yangilaydi."""
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _aylantirish(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        """Mouse wheel bilan gorizontal aylantirishni ta'minlaydi."""
        self._canvas.xview_scroll(-1 * (event.delta // 120), "units")
