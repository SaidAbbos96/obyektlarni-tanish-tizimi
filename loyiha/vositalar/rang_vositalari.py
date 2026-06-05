"""Sinf indeksiga qarab bounding box uchun rang generatsiyasi."""

# Oldindan tayyorlangan 20 ta aniq ajraladigan BGR rang
_RANGLAR: list[tuple[int, int, int]] = [
    (255, 56, 56),  # qizil
    (56, 255, 56),  # yashil
    (56, 56, 255),  # ko'k
    (255, 157, 56),  # to'q sariq
    (157, 56, 255),  # binafsha
    (56, 255, 157),  # moviy-yashil
    (255, 255, 56),  # sariq
    (56, 255, 255),  # moviy
    (255, 56, 255),  # qo'ng'ir-qizil
    (180, 180, 56),  # zaytun
    (56, 180, 180),  # moviy-ko'k
    (180, 56, 180),  # to'q binafsha
    (255, 120, 0),  # apelsin
    (0, 120, 255),  # ko'k-moviy
    (120, 255, 0),  # limon
    (0, 255, 120),  # o't-yashil
    (255, 0, 120),  # pushti
    (120, 0, 255),  # to'q ko'k
    (0, 180, 255),  # osmon ko'k
    (180, 255, 0),  # yashil-sariq
]


def sinf_rangi(sinf_indeksi: int) -> tuple[int, int, int]:
    """Sinf indeksiga mos BGR rangni qaytaradi.

    Parametrlar:
        sinf_indeksi: Model sinf raqami (istalgan musbat son).

    Natija:
        (B, G, R) formatdagi rang to'plami.
    """
    return _RANGLAR[sinf_indeksi % len(_RANGLAR)]
