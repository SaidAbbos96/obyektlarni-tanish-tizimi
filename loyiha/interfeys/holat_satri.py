"""Holat satri — pastki qismdagi xabarlar."""

import tkinter as tk


class HolatSatri:
    """Oyna pastida joylashgan holat xabar satri.

    Foydalanish:
        holat = HolatSatri(ota)
        holat.xabar_korsatish("Tayyor")
        holat.yuklanish_korsatish(True)
    """

    def __init__(self, ota: tk.Widget) -> None:
        """Holat satrini yaratadi.

        Parametrlar:
            ota: Ota tk.Widget.
        """
        self._asosiy = tk.Frame(ota, bd=1, relief=tk.SUNKEN)
        self._asosiy.pack(side=tk.BOTTOM, fill=tk.X)

        # Xabar matni
        self._xabar_oz = tk.StringVar(value="Tayyor.")
        self._xabar_label = tk.Label(
            self._asosiy,
            textvariable=self._xabar_oz,
            anchor=tk.W,
            padx=6,
        )
        self._xabar_label.pack(side=tk.LEFT)

        # Yuklanish indikatori
        self._yuklash_oz = tk.StringVar(value="")
        self._yuklash_label = tk.Label(
            self._asosiy,
            textvariable=self._yuklash_oz,
            fg="blue",
            padx=6,
        )
        self._yuklash_label.pack(side=tk.RIGHT)

    def xabar_korsatish(self, matn: str) -> None:
        """Holat xabarini yangilaydi.

        Parametrlar:
            matn: Ko'rsatiladigan xabar matni.
        """
        self._xabar_oz.set(matn)

    def xato_korsatish(self, matn: str) -> None:
        """Xato xabarini qizil rangda ko'rsatadi.

        Parametrlar:
            matn: Xato matni.
        """
        self._xabar_oz.set(f"Xato: {matn}")
        self._xabar_label.config(fg="red")

    def oddiy_rang(self) -> None:
        """Xabar rangini oddiy (qora) ga qaytaradi."""
        self._xabar_label.config(fg="black")

    def yuklanish_korsatish(self, faol: bool) -> None:
        """Yuklanish indikatorini yoqadi yoki o'chiradi.

        Parametrlar:
            faol: True bo'lsa indikator ko'rinadi.
        """
        if faol:
            self._yuklash_oz.set("Ishlamoqda…")
        else:
            self._yuklash_oz.set("")
