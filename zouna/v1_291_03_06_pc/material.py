from ..bff.io import (
    MaterialBodyV1291_03_06PC,
    ResourceObjectLinkHeaderV106_63_02PC,
    TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndMaterialBodyV1291_03_06PC,
)
from ..common.resource import load_dependencies, save_dependencies
from ..generic.material import Material
from ...common.constants import WalleMaterialRenderFlags
from ...common.util import safe_int
import math
import struct


def as_u32(v):
    return int(v) & 0xFFFFFFFF


# ----------------------------------------------------------------------
# TYPE PUNNING HELPERS (float32 <-> u32)
# ----------------------------------------------------------------------


def u32_to_f32_pun(u: int) -> float:
    """Bitcast u32 -> float32 (preserve bits)."""
    return struct.unpack("<f", struct.pack("<I", as_u32(u)))[0]


def f32_to_u32_pun(f: float) -> int:
    """Bitcast float -> u32 using float32 representation."""
    return struct.unpack("<I", struct.pack("<f", float(f)))[0]


class MaterialV1_291_03_06_PC:
    file_path: str
    material: (
        TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndMaterialBodyV1291_03_06PC
    )

    def __init__(
        self,
        material: TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndMaterialBodyV1291_03_06PC = None,
    ):
        if material is not None:
            self.material = material.material_v1_291_03_06_pc
            self.file_path = material.file_path
            print(f"self.file_path: {self.file_path}")

    # ======================================================================
    # FROM GENERIC
    # ======================================================================

    @staticmethod
    def from_generic(generic_material: Material):
        if generic_material is None:
            return None

        # ------------------------------------------------------------
        # Body defaults
        # ------------------------------------------------------------
        body = MaterialBodyV1291_03_06PC(
            cdcdcdcd=0xCDCDCDCD,
            diffuse=[1.0, 1.0, 1.0, 1.0],
            diffuse_rotation=0.0,
            diffuse_scale=[1.0, 1.0],
            diffuse_translation=[0.0, 0.0],
            emission=[0.0, 0.0, 0.0],
            flags=[0, WalleMaterialRenderFlags.DEFAULT, 0],
            params=[0, 0, 0, 0],  # 4 × u32
            specular=[0.0, 0.0, 0.0],
            specular_pow=1.0,
            texture_flag=0,
            textures=[""] * 8,
            uv_transform_matrix=[
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [-1.0, -1.0, 1.0, 0.0],
            ],
        )

        # ------------------------------------------------------------
        # Link header
        # ------------------------------------------------------------
        link_header = ResourceObjectLinkHeaderV106_63_02PC(
            link_name=safe_int(generic_material.name),
            links=[],
            names=[],
        )

        material_pc = MaterialV1_291_03_06_PC()
        material_pc.file_path = generic_material.file_path
        material_pc.material = TrivialClassForResourceObjectLinkHeaderV106_63_02PCAndMaterialBodyV1291_03_06PC(
            body=body,
            class_name="Material_Z",
            link_header=link_header,
            link_name=safe_int(generic_material.file_name or ""),
            name=safe_int(generic_material.file_name or ""),
        )

        material_pc.material.name = safe_int(generic_material.file_name or "")
        material_pc.material.link_header.link_name = safe_int(
            generic_material.name or ""
        )

        # ------------------------------------------------------------
        # Material properties
        # ------------------------------------------------------------
        diffuse_color = generic_material.diffuse_color
        opacity = generic_material.opacity
        body.diffuse = [
            diffuse_color[0],
            diffuse_color[1],
            diffuse_color[2],
            opacity,
        ]

        body.emission = list(generic_material.emissive_color)
        body.specular = list(generic_material.specular_color)
        body.specular_pow = generic_material.specular_power

        # ------------------------------------------------------------
        # PARAMS
        # generic_material.rat_params: 4 × float
        # body.params: 4 × u32 (TYPE-PUNNED)
        # ------------------------------------------------------------
        rp = generic_material.rat_params  # assumed always len == 4

        body.params[0] = f32_to_u32_pun(rp[0])
        body.params[1] = f32_to_u32_pun(rp[1])
        body.params[2] = f32_to_u32_pun(rp[2])
        body.params[3] = f32_to_u32_pun(rp[3])

        body.diffuse_rotation = generic_material.uv_rotation
        body.diffuse_translation = list(generic_material.uv_translation)
        body.diffuse_scale = list(generic_material.uv_scale)

        # ------------------------------------------------------------
        # UV transform matrix
        # ------------------------------------------------------------
        tx, ty = body.diffuse_translation
        sx, sy = body.diffuse_scale
        theta = body.diffuse_rotation

        cos_r = math.cos(theta)
        sin_r = math.sin(theta)

        body.uv_transform_matrix = [
            [sx * cos_r, -sy * sin_r, 0.0, tx],
            [sx * sin_r, sy * cos_r, 0.0, ty],
            [-1.0, -1.0, 1.0, 0.0],
        ]

        # ------------------------------------------------------------
        # Render flags
        # ------------------------------------------------------------
        if generic_material.env_alpha_mask:
            body.flags[1] |= WalleMaterialRenderFlags.ALPHA_MASK

        # ------------------------------------------------------------
        # Textures
        # ------------------------------------------------------------
        texture_slots = ["tex_diffuse", "tex_envmap", "tex_normal", "tex_specular"]

        generic_bitmaps_to_save = []
        export_attempted_slots = [False] * len(texture_slots)

        for i, slot_name in enumerate(texture_slots):
            generic_bitmap = getattr(generic_material, slot_name, None)
            if generic_bitmap is not None:
                generic_bitmaps_to_save.append(generic_bitmap)
                export_attempted_slots[i] = True
                body.texture_flag |= 1 << i

        exported_keys = []
        if generic_bitmaps_to_save:
            exported_keys = save_dependencies(
                generic_material.file_path, generic_bitmaps_to_save
            )

        key_index = 0
        for i in range(len(texture_slots)):
            if export_attempted_slots[i] and key_index < len(exported_keys):
                key = exported_keys[key_index]
                body.textures[i] = key
                material_pc.material.link_header.names.append(key)
                key_index += 1
            else:
                body.textures[i] = ""

        return material_pc

    # ======================================================================
    # TO GENERIC
    # ======================================================================

    def to_generic(self) -> Material:
        body: MaterialBodyV1291_03_06PC = self.material.body
        generic_material = Material()

        generic_material.file_path = self.file_path
        generic_material.file_name = str(self.material.name)
        generic_material.name = str(self.material.link_header.link_name)

        generic_bitmaps = load_dependencies(self.file_path, list(body.textures))

        generic_material.diffuse_color = tuple(body.diffuse[:3])
        generic_material.opacity = body.diffuse[3]
        generic_material.emissive_color = tuple(body.emission)
        generic_material.specular_color = tuple(body.specular)
        generic_material.specular_power = body.specular_pow

        # ------------------------------------------------------------
        # PARAMS
        # body.params: 4 × u32
        # generic_material.rat_params: 4 × float (TYPE-PUNNED)
        # ------------------------------------------------------------
        p = body.params  # assumed always len == 4

        generic_material.rat_params = [
            u32_to_f32_pun(p[0]),
            u32_to_f32_pun(p[1]),
            u32_to_f32_pun(p[2]),
            u32_to_f32_pun(p[3]),
        ]

        generic_material.uv_rotation = body.diffuse_rotation
        generic_material.uv_translation = tuple(body.diffuse_translation)
        generic_material.uv_scale = tuple(body.diffuse_scale)

        generic_material.env_alpha_mask = bool(
            body.flags[1] & WalleMaterialRenderFlags.ALPHA_MASK
        )

        slots = ["tex_diffuse", "tex_envmap", "tex_normal", "tex_specular"]
        for slot_name, bitmap in zip(slots, generic_bitmaps):
            setattr(generic_material, slot_name, bitmap)

        return generic_material
