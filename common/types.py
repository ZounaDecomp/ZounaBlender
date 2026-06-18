from typing import TypeAlias

from ..zouna.bff.io import (
    BffBox as _BffBox,
    BoxCol as _BoxCol,
    Cylindre,
    CylindreCol3 as _CylindreCol,
    Segment as _Segment,
    Sphere as _Sphere,
    SphereCol as _SphereCol,
)

Box: TypeAlias = _BffBox
Sphere: TypeAlias = _Sphere
Segment: TypeAlias = _Segment
BoxCol: TypeAlias = _BoxCol
CylindreCol: TypeAlias = _CylindreCol
SphereCol: TypeAlias = _SphereCol

__all__ = [
    "Box",
    "Sphere",
    "Segment",
    "BoxCol",
    "CylindreCol",
    "SphereCol",
    "Cylindre",
]
