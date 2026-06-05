"""Loyihaning kirish nuqtasi.

Ishga tushirish:
    python asosiy.py
"""

import sys
from pathlib import Path

# Loyiha ildizini Python yo'liga qo'shamiz
sys.path.insert(0, str(Path(__file__).parent))

from loyiha.sozlamalar.sozlamalar import Sozlamalar
from loyiha.xizmatlar.jurnal_xizmati import jurnal_sozlash
from loyiha.vositalar.fayl_vositalari import kerakli_papkalarni_yaratish
from loyiha.interfeys.asosiy_oyna import AsosiyOyna


def asosiy() -> None:
    """Ilovani ishga tushiradi.

    1. Sozlamalarni yuklaydi (sozlamalar.json).
    2. Zaruriy papkalarni yaratadi.
    3. Jurnal tizimini sozlaydi.
    4. Tkinter asosiy oynani ochadi.
    """
    # Sozlamalar
    sozlamalar_yol = Path(__file__).parent / "sozlamalar.json"
    if sozlamalar_yol.is_file():
        sozlamalar = Sozlamalar.yuklash(str(sozlamalar_yol))
    else:
        sozlamalar = Sozlamalar.standart()

    # Papkalar
    kerakli_papkalarni_yaratish(
        [
            sozlamalar.chiquvchi_papka,
            sozlamalar.kiruvchi_papka,
            sozlamalar.modellar_papka,
            str(Path(sozlamalar.jurnal_fayl).parent),
        ]
    )

    # Jurnal
    jurnal_sozlash(sozlamalar)

    # GUI
    oyna = AsosiyOyna(sozlamalar)
    oyna.ishga_tushirish()


if __name__ == "__main__":
    asosiy()
