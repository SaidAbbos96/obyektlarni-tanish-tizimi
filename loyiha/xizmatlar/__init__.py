"""Xizmatlar paketi."""

from .jurnal_xizmati import jurnal_sozlash
from .rasm_yuklash_xizmati import RasmYuklashXizmati
from .aniqlash_xizmati import ObyektAniqlovchiXizmat
from .saqlash_xizmati import NatijaSaqlashXizmati

__all__ = [
    "jurnal_sozlash",
    "RasmYuklashXizmati",
    "ObyektAniqlovchiXizmat",
    "NatijaSaqlashXizmati",
]
