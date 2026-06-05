"""Natijalar ro'yxati paneli — Treeview asosida."""

import tkinter as tk
from tkinter import ttk
from typing import List

from loyiha.modellar.aniqlash_natijasi import AniqlashNatijasi


class NatijaPanel:
    """Aniqlash natijalarini jadval ko'rinishida ko'rsatuvchi komponent.

    Ustunlar: #, Sinf, Aniqlik, (x1,y1)-(x2,y2), Strategiya

    Foydalanish:
        panel = NatijaPanel(ota)
        panel.natijani_korsatish(aniqlash_natijasi)
        panel.tozalash()
    """

    def __init__(self, ota: tk.Widget) -> None:
        """Natija panelini yaratadi.

        Parametrlar:
            ota: Ota widget.
        """
        self._asosiy = ttk.LabelFrame(ota, text="Natijalar")
        self._asosiy.pack(side=tk.RIGHT, fill=tk.BOTH, padx=4, pady=4, ipadx=2)

        # Ustunlar
        ustunlar = ("#", "Sinf", "Aniqlik", "Koordinat", "Strategiya")
        self._jadval = ttk.Treeview(
            self._asosiy,
            columns=ustunlar,
            show="headings",
            height=20,
        )

        # Ustun sarlavhalari va enlari
        enlari = (30, 110, 72, 170, 80)
        for nom, en in zip(ustunlar, enlari):
            self._jadval.heading(nom, text=nom)
            self._jadval.column(nom, width=en, anchor=tk.CENTER, minwidth=en)

        # Yashil rang — yuqori aniqlik uchun
        self._jadval.tag_configure("yuqori", foreground="#27ae60")
        self._jadval.tag_configure("orta", foreground="#e67e22")
        self._jadval.tag_configure("past", foreground="#e74c3c")

        # Scroll bar
        skroll = ttk.Scrollbar(
            self._asosiy, orient=tk.VERTICAL, command=self._jadval.yview
        )
        self._jadval.configure(yscrollcommand=skroll.set)

        self._jadval.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        skroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Statistika label (jadval ostida, to'liq kenglikda)
        self._statistika_oz = tk.StringVar(value="")
        tk.Label(
            ota,
            textvariable=self._statistika_oz,
            anchor=tk.W,
            font=("Segoe UI", 9),
            pady=3,
        ).pack(side=tk.BOTTOM, fill=tk.X, padx=6)

    def natijani_korsatish(self, natija: AniqlashNatijasi) -> None:
        """Aniqlash natijasini jadvalga to'ldiradi.

        Parametrlar:
            natija: AniqlashNatijasi nusxasi.
        """
        self.tozalash()

        for i, ob in enumerate(natija.obyektlar, start=1):
            r = ob.ramka
            koord = f"({r.x1},{r.y1})-({r.x2},{r.y2})"
            # Aniqlikka qarab rang belgilash
            if ob.aniqlik >= 0.8:
                teg = ("yuqori",)
            elif ob.aniqlik >= 0.5:
                teg = ("orta",)
            else:
                teg = ("past",)
            self._jadval.insert(
                "",
                tk.END,
                values=(i, ob.sinf_nomi, ob.aniqlik_foiz, koord, ob.strategiya),
                tags=teg,
            )

        stat = (
            f"Jami: {natija.obyektlar_soni} ta   "
            f"O'rt: {natija.ortacha_aniqlik:.0%}   "
            f"{natija.ishlash_vaqti_ms:.0f} ms   "
            f"{natija.strategiya_nomi}"
        )
        self._statistika_oz.set(stat)

    def tozalash(self) -> None:
        """Jadvalni bo'shatadi."""
        for satir in self._jadval.get_children():
            self._jadval.delete(satir)
        self._statistika_oz.set("")
