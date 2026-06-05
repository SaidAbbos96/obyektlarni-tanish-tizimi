"""Menyu satri komponenti."""

import tkinter as tk
from typing import Callable


class MenyuSatri:
    """Asosiy oyna menyusi.

    Tugmalar: Fayl → Ochish, Saqlash, Chiqish
              Aniqlash → Boshlash, Strategiya tanlash
              Yordam → Haqida
    """

    def __init__(
        self,
        ota: tk.Tk,
        rasm_och: Callable[[], None],
        natija_saqlash: Callable[[], None],
        aniqlash_boshlash: Callable[[], None],
        haar_tanlash: Callable[[], None],
        dnn_tanlash: Callable[[], None],
        haqida_ochish: Callable[[], None],
    ) -> None:
        """Menyuni yaratadi va oynaga ulaydi.

        Parametrlar:
            ota:              Asosiy tk.Tk oyna.
            rasm_och:         'Rasm ochish' callback.
            natija_saqlash:   'Natijani saqlash' callback.
            aniqlash_boshlash:'Aniqlashni boshlash' callback.
            haar_tanlash:     'Haar strategiyasi' callback.
            dnn_tanlash:      'DNN strategiyasi' callback.
            haqida_ochish:    'Haqida' callback.
        """
        self._menyu = tk.Menu(ota)
        ota.config(menu=self._menyu)

        # Fayl menyusi
        fayl = tk.Menu(self._menyu, tearoff=False)
        self._menyu.add_cascade(label="Fayl", menu=fayl)
        fayl.add_command(label="Rasm ochish…  Ctrl+O", command=rasm_och)
        fayl.add_command(label="Natijani saqlash  Ctrl+S", command=natija_saqlash)
        fayl.add_separator()
        fayl.add_command(label="Chiqish  Alt+F4", command=ota.destroy)

        # Aniqlash menyusi
        aniqlash = tk.Menu(self._menyu, tearoff=False)
        self._menyu.add_cascade(label="Aniqlash", menu=aniqlash)
        aniqlash.add_command(label="Aniqlashni boshlash  F5", command=aniqlash_boshlash)
        aniqlash.add_separator()

        self._faol_strategiya = tk.StringVar(value="haar")
        aniqlash.add_radiobutton(
            label="Haar (Yuz)",
            variable=self._faol_strategiya,
            value="haar",
            command=haar_tanlash,
        )
        aniqlash.add_radiobutton(
            label="DNN MobileNet",
            variable=self._faol_strategiya,
            value="dnn",
            command=dnn_tanlash,
        )

        # Yordam
        yordam = tk.Menu(self._menyu, tearoff=False)
        self._menyu.add_cascade(label="Yordam", menu=yordam)
        yordam.add_command(label="Ilova haqida", command=haqida_ochish)

    def strategiyani_belgilash(self, nom: str) -> None:
        """Menyu da faol strategiyani yangilaydi.

        Parametrlar:
            nom: Strategiya nomi ('haar' yoki 'dnn').
        """
        self._faol_strategiya.set(nom)
