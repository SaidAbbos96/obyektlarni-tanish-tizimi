"""
media/kiruvchi papkasiga MobileNet-SSD 21 sinfi uchun
namunaviy rasmlarni yuklab oluvchi skript.

Ishga tushirish:
    python yuklovchi_skript.py
"""

import time
import urllib.request
from pathlib import Path

PAPKA = Path("media/kiruvchi")
PAPKA.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# O'zbek nomi → Wikimedia Commons original fayl URL (thumbnail emas)
RASMLAR: dict[str, str] = {
    "shaxs": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
    "mashina": "https://upload.wikimedia.org/wikipedia/commons/1/1b/2019_Honda_Civic_sedan_%28facelift%2C_red%29%2C_front_8.21.19.jpg",
    "avtobus": "https://upload.wikimedia.org/wikipedia/commons/a/a0/2004_Daf_rear_engined_bus.jpg",
    "mototsikl": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Yamaha_YZF_R1.jpg",
    "velosiped": "https://upload.wikimedia.org/wikipedia/commons/4/41/Bicycle_with_a_medium-length_wheelbase.jpg",
    "it": "https://upload.wikimedia.org/wikipedia/commons/2/26/YellowLabradorLooking_new.jpg",
    "mushuk": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_November_2010-1a.jpg",
    "ot": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Collage_of_Nine_Horses.jpg",
    "sigir": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Cow_female_black_white.jpg",
    "qoy": "https://upload.wikimedia.org/wikipedia/commons/2/27/Ovis_aries_Tibetan_sheep.jpg",
    "qush": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Selasphorus-sasin-001.jpg",
    "qayiq": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Big_Duck_small_boat.jpg",
    "samolyot": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png",
    "poyezd": "https://upload.wikimedia.org/wikipedia/commons/e/e6/ICE_3_Cologne_Bonn_Airport.jpg",
    "stul": "https://upload.wikimedia.org/wikipedia/commons/8/80/Windsor_chair%2C_1765-1780_-_Springfield_Museum_of_Art_-_DSC00921.JPG",
    "stol": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Breakfast_table.jpg",
    "divan": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Sofa_noci.jpg",
    "monitor": "https://upload.wikimedia.org/wikipedia/commons/7/72/Computer_monitor.jpg",
    "shisha": "https://upload.wikimedia.org/wikipedia/commons/9/91/Glass_of_wine_top.jpg",
    "kochati": "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg",
}


def rasmni_yukla(url: str, fayl_yoli: Path) -> bool:
    """Rasmni yuklab saqlaydi."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as javob:
            fayl_yoli.write_bytes(javob.read())
        return True
    except Exception as e:
        print(f"  Yuklash xatosi: {e}")
        return False


def main() -> None:
    print(f"Rasmlar papkasi: {PAPKA.resolve()}\n")
    muvaffaqiyat = 0
    xato = 0

    for nom, url in RASMLAR.items():
        # Kengaytmani URL dan aniqlash
        kengaytma = ".jpg"
        if ".png" in url.lower():
            kengaytma = ".png"
        fayl = PAPKA / f"{nom}{kengaytma}"

        if fayl.exists() and fayl.stat().st_size > 5000:
            print(f"  [mavjud]  {fayl.name}")
            muvaffaqiyat += 1
            continue

        print(f"  Yuklanmoqda: {nom}...", end=" ", flush=True)

        if rasmni_yukla(url, fayl):
            kb = fayl.stat().st_size // 1024
            print(f"OK  ({kb} KB)")
            muvaffaqiyat += 1
        else:
            xato += 1

        time.sleep(0.2)

    print(f"\nTayyor: {muvaffaqiyat} ta yuklandi, {xato} ta xato.")


if __name__ == "__main__":
    main()
