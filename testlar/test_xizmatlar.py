"""Xizmatlar uchun testlar."""

import numpy as np
import pytest

from loyiha.sozlamalar.sozlamalar import Sozlamalar
from loyiha.xizmatlar.rasm_yuklash_xizmati import RasmYuklashXizmati
from loyiha.modellar.xatolar import RasmTopilmadiXatosi, NotogriFaqlFormatXatosi


@pytest.fixture
def sozlamalar():
    return Sozlamalar.standart()


def test_yuklash_fayl_yoq(sozlamalar):
    xizmat = RasmYuklashXizmati(sozlamalar)
    with pytest.raises(RasmTopilmadiXatosi):
        xizmat.yuklash("/mavjud/emas.jpg")


def test_yuklash_noto_gri_format(sozlamalar, tmp_path):
    xizmat = RasmYuklashXizmati(sozlamalar)
    fayl = tmp_path / "test.xyz"
    fayl.write_bytes(b"ma'lumot")
    with pytest.raises(NotogriFaqlFormatXatosi):
        xizmat.yuklash(str(fayl))
