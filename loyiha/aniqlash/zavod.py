"""Aniqlovchi strategiyasini yaratuvchi factory."""

from loyiha.sozlamalar.sozlamalar import Sozlamalar
from loyiha.modellar.xatolar import QollanilmaganStrategiyaXatosi
from .asosiy_strategiya import AniqlashStrategiyasi
from .haar_aniqlovchi import HaarAniqlovchi
from .dnn_aniqlovchi import DnnAniqlovchi


def aniqlovchi_yaratish(
    strategiya: str, sozlamalar: Sozlamalar
) -> AniqlashStrategiyasi:
    """Ko'rsatilgan strategiya nomiga mos aniqlovchi yaratadi.

    Parametrlar:
        strategiya:  Strategiya nomi: 'haar' yoki 'dnn'.
        sozlamalar:  Ilova sozlamalari.

    Natija:
        AniqlashStrategiyasi nusxasi.

    Istisno:
        QollanilmaganStrategiyaXatosi: Noma'lum strategiya nomi.
    """
    if strategiya == "haar":
        return HaarAniqlovchi()

    if strategiya == "dnn":
        return DnnAniqlovchi(sozlamalar.modellar_papka)

    raise QollanilmaganStrategiyaXatosi(
        f"Noma'lum strategiya: '{strategiya}'. " f"Mavjudlari: 'haar', 'dnn'."
    )
