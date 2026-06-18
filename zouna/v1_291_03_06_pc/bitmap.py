from ..bff.io import (
    BitmapBodyV1291_03_06PC,
    BitmapHeader,
    ResourceObjectLinkHeaderV106_63_02PC,
    TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV1291_03_06PC,
)
from ..generic.bitmap import Bitmap
from ...common.constants import BmTransp
from ...common.util import safe_int


class BitmapV1_291_03_06_PC:
    file_path: str
    bitmap: (
        TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV1291_03_06PC
    )

    def __init__(
        self,
        bitmap: TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV1291_03_06PC = None,
    ):
        if bitmap is not None:
            self.bitmap = bitmap.bitmap_v1_291_03_06_pc
            self.file_path = bitmap.file_path
            print(f"self.file_path: {self.file_path}")

    @staticmethod
    def from_generic(generic_bitmap: Bitmap):
        """
        Convert a generic Bitmap into a BitmapV1_291_03_06_PC instance.

        Mirrors BitmapV1_06_63_02_PC.from_generic as closely as the
        V1291 schema allows.
        """
        if generic_bitmap is None:
            return None

        # ------------------------------------------------------------
        # Flag logic (copied verbatim from V106)
        # ------------------------------------------------------------
        flag = 149
        mip_count = generic_bitmap.mip_count
        if mip_count > 0:
            flag += 32

        # ------------------------------------------------------------
        # Body header (V1291 replacement for V106 body)
        # ------------------------------------------------------------
        header = BitmapHeader(
            flag=flag,
            format=generic_bitmap.format,
            height=generic_bitmap.height,
            mipmap_count=mip_count,
            precalculated_size=generic_bitmap.precalculated_size,
            unknown=4,  # mirrors V106 `four=4`
            width=generic_bitmap.width,
        )

        body = BitmapBodyV1291_03_06PC(header=header)

        # ------------------------------------------------------------
        # Link header (identical pattern to V106)
        # ------------------------------------------------------------
        link_header = ResourceObjectLinkHeaderV106_63_02PC(
            link_name=safe_int(generic_bitmap.file_name) or "",
            names=[],
            links=[],
        )

        versioned_bitmap = TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV1291_03_06PC(
            body=body,
            class_name="Bitmap_Z",
            link_header=link_header,
            link_name=safe_int(generic_bitmap.file_name),
            name=safe_int(generic_bitmap.file_name) or "",
        )

        bmp = BitmapV1_291_03_06_PC()
        bmp.file_path = generic_bitmap.file_path
        bmp.bitmap = versioned_bitmap

        return bmp

    def to_generic(self) -> Bitmap:
        body: BitmapBodyV1291_03_06PC = self.bitmap.body
        generic_bitmap = Bitmap()

        generic_bitmap.file_path = self.file_path
        generic_bitmap.file_name = str(self.bitmap.name)
        generic_bitmap.name = str(self.bitmap.link_header.link_name)
        # generic_bitmap.transp_format = BmTransp(body.transp_format)

        return generic_bitmap
