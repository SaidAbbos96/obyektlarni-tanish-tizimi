# Obyektlarni Tanish Tizimi — v3.0

**Talaba:** Xudoyqulov SaidAbbos Salim o'g'li  
**Guruh:** KI-032-01 | Masofaviy ta'lim  
**Universitet:** Muhammad al-Xorazmiy nomidagi TATU Samarqand filiali  
**GitHub:** https://github.com/SaidAbbos96/obyektlarni-tanish-tizimi

---

## Loyiha haqida

Python va OpenCV yordamida rasmlardan yuzlarni va 20 ta toifadagi obyektlarni
aniqlash tizimi. Tkinter yordamida qurilgan zamonaviy grafik interfeys.

**Arxitektura:** Clean Architecture + Strategy Pattern (MVP)  
**Barcha nomlar va sharhlar:** O'zbek tilida

---

## Imkoniyatlar

- **Haar Cascade** — yuzlarni aniqlash (model yuklab olish shart emas)
- **DNN MobileNet-SSD** — 20 ta obyekt sinfi: shaxs, mashina, it, mushuk va boshqalar
- Drag & Drop orqali rasm yuklash
- Canvas ga bosish orqali fayl dialog
- Pastki karusel — `media/kiruvchi` papkasidagi rasmlar
- Boshqaruv paneli (rasm ochish, aniqlash, saqlash, tozalash)
- Natija PNG + JSON sifatida saqlanadi
- Asinxron aniqlash — GUI bloklanmaydi

---

## Talablar

- Python 3.12+
- `requirements.txt` paketlar:
  - `opencv-python >= 4.8`
  - `numpy >= 1.26`
  - `Pillow >= 10.0`
  - `requests >= 2.31`
  - `tkinterdnd2` _(Drag & Drop uchun)_

---

## Ishga tushirish

```bash
# 1. Virtual muhit yaratish va faollashtirish
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS

# 2. Paketlarni o'rnatish
pip install -r requirements.txt

# 3. Ilovani ishga tushirish
python asosiy.py
```

---

## DNN model fayllarini o'rnatish

`.caffemodel` fayli katta (22 MB) — GitHub da saqlanmaydi, alohida yuklab olinadi.

```
loyiha/model_boshqaruv/modellar/
  ├── MobileNetSSD_deploy.prototxt    ← GitHub da mavjud (loyiha bilan birga)
  └── MobileNetSSD_deploy.caffemodel  ← Quyidagi havoladan yuklab qo'ying
```

**To'g'ridan-to'g'ri yuklab olish havolasi:**  
https://drive.google.com/open?id=0B3gersZ2cHIxRm5BMmZnQ3drOTA

**Yoki GitHub dan:**  
https://github.com/chuanqi305/MobileNet-SSD

Yuklab olgach, faylni `loyiha/model_boshqaruv/modellar/` papkasiga joylashtiring.

---

## Papka tuzilmasi

```
loyiha_max/
├── asosiy.py                        # Kirish nuqtasi
├── sozlamalar.json                  # Konfiguratsiya
├── requirements.txt
├── .gitignore
├── loyiha/
│   ├── modellar/                    # Ma'lumot modellari
│   │   ├── ramka.py                 # Bounding box
│   │   ├── obyekt.py                # Aniqlangan obyekt
│   │   ├── aniqlash_natijasi.py
│   │   └── xatolar.py               # Maxsus istisnolar
│   ├── sozlamalar/                  # Konfiguratsiya tizimi
│   ├── vositalar/                   # Yordamchi funksiyalar
│   ├── aniqlash/                    # Strategy Pattern
│   │   ├── asosiy_strategiya.py     # Abstract Base Class
│   │   ├── haar_aniqlovchi.py       # Yuz aniqlash
│   │   ├── dnn_aniqlovchi.py        # MobileNet-SSD
│   │   └── zavod.py                 # Factory funksiya
│   ├── xizmatlar/                   # Biznes logika
│   ├── taqdimotchi/                 # MVP Presenter + Hodisalar
│   ├── interfeys/                   # Tkinter GUI komponentlari
│   └── model_boshqaruv/modellar/   # Model fayllar
├── media/
│   ├── kiruvchi/                    # Namuna rasmlar (23 ta)
│   └── chiquvchi/                   # Aniqlash natijalari
└── testlar/                         # Pytest testlar (11 ta)
```

---

## Aniqlash strategiyalari

| Strategiya | Tavsif                     | Model                     |
| ---------- | -------------------------- | ------------------------- |
| `haar`     | Yuzni aniqlaydi            | Avtomatik (OpenCV ichida) |
| `dnn`      | 20 ta sinf (MobileNet-SSD) | Alohida yuklab olinadi    |

### DNN sinflari (20 ta)

`shaxs` · `mashina` · `avtobus` · `mototsikl` · `velosiped`  
`it` · `mushuk` · `ot` · `sigir` · `qoy` · `qush`  
`qayiq` · `samolyot` · `poyezd`  
`stul` · `stol` · `divan` · `monitor` · `shisha` · `kochati`

---

## Klaviatura yorliqlari

| Tugma    | Amal                |
| -------- | ------------------- |
| `Ctrl+O` | Rasm ochish         |
| `F5`     | Aniqlashni boshlash |
| `Ctrl+S` | Natijani saqlash    |

---

## Testlarni ishga tushirish

```bash
pytest testlar/ -v
```

---

## Litsenziya

MIT
