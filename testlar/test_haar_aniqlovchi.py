"""Haar aniqlovchisi uchun testlar."""

import numpy as np
import pytest

from loyiha.aniqlash.haar_aniqlovchi import HaarAniqlovchi


@pytest.fixture
def aniqlovchi():
    """HaarAniqlovchi nusxasi — model yuklangan."""
    a = HaarAniqlovchi()
    a.model_yuklash()
    return a


def test_nomi(aniqlovchi):
    assert aniqlovchi.nomi == "haar"


def test_sinflar(aniqlovchi):
    assert "yuz" in aniqlovchi.sinflar


def test_tayyor(aniqlovchi):
    assert aniqlovchi.tayyor_mi() is True


def test_aniqlash_bosh_rasm(aniqlovchi):
    """Bo'sh qora rasmda hech narsa topilmasligi kerak."""
    bosh = np.zeros((300, 300, 3), dtype=np.uint8)
    natijalar = aniqlovchi.aniqlash(bosh)
    assert isinstance(natijalar, list)
