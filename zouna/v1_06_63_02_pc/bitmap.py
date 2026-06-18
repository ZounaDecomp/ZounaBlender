from ...common.util import safe_int
from ...common.constants import BmTransp, PalFormat, BmFormat
from ..bff.io import (
    BitmapBodyV106_63_02PC,
    ResourceObjectLinkHeaderV106_63_02PC,
    TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV106_63_02PC,
)
from ..generic.bitmap import Bitmap


class BitmapV1_06_63_02_PC:
    file_path: str
    bitmap: TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV106_63_02PC

    def __init__(
        self,
        bitmap: TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV106_63_02PC = None,
    ):
        if bitmap is not None:
            self.bitmap = bitmap.bitmap_v1_06_63_02_pc
            self.file_path = bitmap.file_path
            print(f"self.file_path: {self.file_path}")

    @staticmethod
    def from_generic(generic_bitmap: Bitmap):
        """
        Convert a generic Bitmap into a BitmapV1_06_63_02_PC instance,
        using the proper constructor for both body and container.
        """
        if generic_bitmap is None:
            return None
        flag = 149
        mip_count = generic_bitmap.mip_count
        if mip_count > 0:
            flag += 32
        body = BitmapBodyV106_63_02PC(
            flag=flag,
            format=generic_bitmap.format,
            format_copy=generic_bitmap.format,
            four=4,
            width=generic_bitmap.width,
            height=generic_bitmap.height,
            mipmap_count=mip_count,
            palette_format=generic_bitmap.palette_format,
            precalculated_size=generic_bitmap.precalculated_size,
            transp_format=generic_bitmap.transp_format,
        )

        link_header = ResourceObjectLinkHeaderV106_63_02PC(
            link_name=safe_int(generic_bitmap.file_name) or "", names=[], links=[]
        )

        versioned_bitmap = TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndBitmapBodyV106_63_02PC(
            body=body,
            class_name="Bitmap_Z",
            link_header=link_header,
            link_name=safe_int(generic_bitmap.file_name),
            name=safe_int(generic_bitmap.file_name) or "",
        )

        bmp = BitmapV1_06_63_02_PC()
        bmp.file_path = generic_bitmap.file_path
        bmp.bitmap = versioned_bitmap

        return bmp

    def to_generic(self) -> Bitmap:
        body: BitmapBodyV106_63_02PC = self.bitmap.body
        generic_bitmap = Bitmap()

        generic_bitmap.file_path = self.file_path
        generic_bitmap.file_name = str(self.bitmap.name)
        generic_bitmap.name = str(self.bitmap.link_header.link_name)
        generic_bitmap.transp_format = BmTransp(body.transp_format)

        return generic_bitmap
