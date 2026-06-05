"""Rasm konversiyasi va o'lchamini boshqarish uchun vositalar."""

import cv2
import numpy as np
from PIL import Image, ImageTk


def opencv_dan_pil(rasm: np.ndarray) -> Image.Image:
    """OpenCV (BGR numpy) rasmni PIL Image ga o'tkazadi.

    Parametrlar:
        rasm: BGR formatdagi numpy massivi.

    Natija:
        PIL Image (RGB formatda).
    """
    rgb = cv2.cvtColor(rasm, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def pil_dan_tkinter(pil_rasm: Image.Image) -> ImageTk.PhotoImage:
    """PIL Image ni Tkinter da ko'rsatish uchun PhotoImage ga o'tkazadi.

    Parametrlar:
        pil_rasm: PIL Image obyekti.

    Natija:
        Tkinter PhotoImage.
    """
    return ImageTk.PhotoImage(pil_rasm)


def olchamga_keltirish(
    rasm: np.ndarray, maks_kenglik: int, maks_balandlik: int
) -> np.ndarray:
    """Rasmni berilgan o'lchamdan oshmaydigan qilib kichraytiradi.
    Nisbat saqlanadi.

    Parametrlar:
        rasm:          BGR numpy massivi.
        maks_kenglik:  Maksimal ruxsat etilgan kenglik.
        maks_balandlik: Maksimal ruxsat etilgan balandlik.

    Natija:
        Kichraytirilgan yoki asl rasm (agar o'lcham chegaradan oshsa).
    """
    balandlik, kenglik = rasm.shape[:2]
    if kenglik <= maks_kenglik and balandlik <= maks_balandlik:
        return rasm

    # Nisbatni saqlab o'lchamni hisoblash
    nisbat_k = maks_kenglik / kenglik
    nisbat_b = maks_balandlik / balandlik
    nisbat = min(nisbat_k, nisbat_b)

    yangi_kenglik = int(kenglik * nisbat)
    yangi_balandlik = int(balandlik * nisbat)

    return cv2.resize(
        rasm, (yangi_kenglik, yangi_balandlik), interpolation=cv2.INTER_AREA
    )


def panelga_moslash(
    rasm: np.ndarray, panel_kenglik: int, panel_balandlik: int
) -> np.ndarray:
    """Rasmni panel o'lchamiga sig'diradi (kattalashtirish va kichraytirish).

    Parametrlar:
        rasm:            BGR numpy massivi.
        panel_kenglik:   Panel kengligi.
        panel_balandlik: Panel balandligi.

    Natija:
        Moslashtirilgan rasm.
    """
    balandlik, kenglik = rasm.shape[:2]
    if kenglik == 0 or balandlik == 0:
        return rasm

    nisbat_k = panel_kenglik / kenglik
    nisbat_b = panel_balandlik / balandlik
    nisbat = min(nisbat_k, nisbat_b)

    yangi_k = max(1, int(kenglik * nisbat))
    yangi_b = max(1, int(balandlik * nisbat))

    return cv2.resize(rasm, (yangi_k, yangi_b), interpolation=cv2.INTER_AREA)
