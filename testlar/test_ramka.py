"""Ramka modeli uchun testlar."""

import pytest
from loyiha.modellar.ramka import Ramka


def test_ramka_kenglik_balandlik():
    r = Ramka(10, 20, 110, 70)
    assert r.kenglik == 100
    assert r.balandlik == 50


def test_ramka_yuza():
    r = Ramka(0, 0, 50, 50)
    assert r.yuza == 2500


def test_ramka_markaz():
    r = Ramka(0, 0, 100, 100)
    mx, my = r.markaz
    assert mx == 50
    assert my == 50


def test_ramka_to_tuple():
    r = Ramka(1, 2, 3, 4)
    assert r.to_tuple() == (1, 2, 3, 4)


def test_ramka_frozen():
    r = Ramka(0, 0, 10, 10)
    with pytest.raises(Exception):
        r.x1 = 99  # type: ignore
