from ..zouna.bff.io import ColBoxClass, BSphere, Seg, AmbitiousSchema, Cylindre, CunningSchema, Schema2
from typing import TypeAlias

Box: TypeAlias = ColBoxClass
Sphere: TypeAlias = BSphere
Segment: TypeAlias = Seg
BoxCol: TypeAlias = AmbitiousSchema
#Cylindre: TypeAlias = Cylindre
CylindreCol: TypeAlias = CunningSchema
SphereCol: TypeAlias = Schema2

__all__ = [
    "Box",
    "Sphere",
    "Segment",
    "BoxCol",
    "CylindreCol",
    "SphereCol",
    "Cylindre",
]
