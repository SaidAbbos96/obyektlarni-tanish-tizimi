"""Loyiha uchun barcha maxsus xato sinflari."""


class TizimXatosi(Exception):
    """Barcha loyiha xatolarining asosi."""


class RasmTopilmadiXatosi(TizimXatosi):
    """Rasm fayli ko'rsatilgan manzilda mavjud emas."""


class NotogriFaqlFormatXatosi(TizimXatosi):
    """Fayl rasm formatida emas yoki qo'llanilmaydi."""


class ModelTopilmadiXatosi(TizimXatosi):
    """Model fayli yuklanmagan yoki manzilda mavjud emas."""


class ModelYuklashXatosi(TizimXatosi):
    """Modelni yuklashda xatolik yuz berdi."""


class AniqlashXatosi(TizimXatosi):
    """Aniqlash jarayonida xatolik yuz berdi."""


class SozlamalarXatosi(TizimXatosi):
    """Sozlamalar faylini o'qish yoki yozishda xatolik."""


class SaqlashXatosi(TizimXatosi):
    """Natijani faylga saqlashda xatolik yuz berdi."""


class QollanilmaganStrategiyaXatosi(TizimXatosi):
    """Ko'rsatilgan strategiya nomi mavjud emas."""
