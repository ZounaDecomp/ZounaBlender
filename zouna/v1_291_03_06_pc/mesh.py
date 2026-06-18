# from ..generic.mesh import Mesh, Vertex, Face
# from ..common.mesh import decode_vertex_buffer
# from ..common.resource import load_dependencies
# from collections import defaultdict
# from ..bff.io import (
#     MeshBodyV1291_03_06PC,
#     TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC,
#     MeshBuffers2,
#     IndexBuffer,  # index buffer
#     VertexBuffer,  # vertex buffer
#     VertexGroup,  # vertex group
#     LayoutNoBlend,
#     VertexGroupFlags,
#     Vertices,
#     Morpher2,
#     Points2,
#     ObjectType,
#     ObjectLinkHeaderV106_63_02PC,
# )
# from ..common.resource import save_dependencies
# from ...common.util import safe_int


# class MeshV1_291_03_06_PC:
#     file_path: str
#     mesh: TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC

#     def __init__(
#         self,
#         mesh: TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC = None,
#     ):
#         if mesh is not None:
#             self.mesh = mesh.mesh_v1_291_03_06_pc
#             self.file_path = mesh.file_path
#             print(f"self.file_path: {self.file_path}")

#     @staticmethod
#     def from_generic(generic_mesh: Mesh):
#         # ------------------------------------------------------------
#         # Group faces by material
#         # ------------------------------------------------------------
#         faces_by_material = defaultdict(list)
#         for face in generic_mesh.faces:
#             faces_by_material[face.material_id].append(face)

#         final_tris = []
#         final_layout_no_blend = []
#         vertex_groups = []

#         current_vertex_offset = 0
#         index_buffer_index_begin = 0

#         # ------------------------------------------------------------
#         # Build geometry per material
#         # ------------------------------------------------------------
#         for mat_id in sorted(faces_by_material.keys()):
#             faces = faces_by_material[mat_id]

#             vertex_map = {}
#             material_vertices = []

#             for face in faces:
#                 local_indices = []

#                 for v in face.vertices:
#                     key = (
#                         v.position_id,
#                         v.normal_id if v.normal_id is not None else -1,
#                         v.uv_id if v.uv_id is not None else -1,
#                         v.luv_id if v.luv_id is not None else -1,
#                     )

#                     if key not in vertex_map:
#                         local_index = len(material_vertices)
#                         vertex_map[key] = local_index
#                         local_indices.append(local_index)

#                         pos = generic_mesh.positions[v.position_id]
#                         norm = (
#                             generic_mesh.normals[v.normal_id]
#                             if v.normal_id is not None
#                             else [0.0, 0.0, 0.0]
#                         )
#                         uv = (
#                             generic_mesh.uvs[v.uv_id]
#                             if v.uv_id is not None
#                             else [0.0, 0.0]
#                         )
#                         luv = (
#                             generic_mesh.luvs[v.luv_id]
#                             if v.luv_id is not None
#                             else [0.0, 0.0]
#                         )

#                         material_vertices.append((pos, norm, uv, luv))
#                     else:
#                         local_indices.append(vertex_map[key])

#                 final_tris.append([i + current_vertex_offset for i in local_indices])

#             vertex_count = len(material_vertices)

#             # --------------------------------------------------------
#             # Vertex group (VertexGroup)
#             # --------------------------------------------------------
#             vertex_groups.append(
#                 VertexGroup(
#                     len(faces),                      # face_count
#                     VertexGroupFlags(1, 0, 0, 0, 0, 0, 0),
#                     index_buffer_index_begin,        # index_buffer_index_begin
#                     vertex_count - 1,                # unknown0
#                     mat_id,                          # unused  ✅ group index
#                     current_vertex_offset,           # vertex_buffer_range_begin
#                     vertex_count,                    # vertex_count
#                     36,                              # vertex_layout (layout_no_blend)
#                     current_vertex_offset,           # vertex_offset_in_groups
#                     0,                               # zero
#                     [0, 0, 0],                       # zeroes
#                 )
#             )

#             # --------------------------------------------------------
#             # Vertex data
#             # --------------------------------------------------------
#             for pos, norm, uv, luv in material_vertices:
#                 final_layout_no_blend.append(
#                     LayoutNoBlend(
#                         position=pos,
#                         normal=norm,
#                         normal_w=0,
#                         tangent=[0, 0, 0],
#                         tangent_w=0,
#                         uv=uv,
#                         luv=luv,
#                     )
#                 )

#             current_vertex_offset += vertex_count
#             index_buffer_index_begin += len(faces) * 3

#         # ------------------------------------------------------------
#         # Materials
#         # ------------------------------------------------------------
#         dependencies = [m for m in generic_mesh.materials if m is not None]
#         material_names = save_dependencies(generic_mesh.file_path, dependencies)

#         # ------------------------------------------------------------
#         # Buffers
#         # ------------------------------------------------------------
#         index_buffers = [IndexBuffer(flags=34, tris=final_tris)]

#         vertices = Vertices(
#             layout_position=None,
#             layout_position_uv=None,
#             layout_no_blend=final_layout_no_blend,
#             layout1_blend=None,
#             layout4_blend=None,
#             layout_unknown=None,
#         )

#         vertex_buffers = [VertexBuffer(flags=34, vertices=vertices)]

#         mesh_buffers = MeshBuffers2(
#             index_buffers=index_buffers,
#             morpher=Morpher2(morpher_descs=[], morpher_relateds=[]),
#             unknowns=[],
#             vertex_buffers=vertex_buffers,
#             vertex_groups=vertex_groups,
#         )

#         # ------------------------------------------------------------
#         # Body (ALL fields filled)
#         # ------------------------------------------------------------
#         body = MeshBodyV1291_03_06PC(
#             box_cols=list(generic_mesh.col_boxes),
#             collision_aabb_tris=[],
#             collision_aabbs=[],
#             cylindre_cols=list(generic_mesh.col_cylindres),
#             drawing_cutoff_distance=0.0,
#             drawing_start_distance=0.0,
#             material_names=material_names,
#             mesh_buffers=mesh_buffers,
#             normals=[],  # not used (vertex buffer contains normals)
#             points=Points2(
#                 [],  # points_related0
#                 [],  # points_related1
#                 [],  # points_related2
#             ),
#             related_to_counts=[0, 0, 0],
#             shadow_related=0,
#             sphere_cols=list(generic_mesh.col_spheres),
#             strips=[],
#             texcoords=[],  # unused in V1291 when vertex buffers exist
#             unknown4_s=None,
#             unknown5_s=[],
#             unknown6_s=[],
#             unknown8_s=[],
#             vertices=[],  # legacy, not used
#         )

#         # ------------------------------------------------------------
#         # Final mesh
#         # ------------------------------------------------------------
#         link_header = ObjectLinkHeaderV106_63_02PC(
#             b_box=generic_mesh.b_box,
#             b_sphere=generic_mesh.b_sphere,
#             data_name=generic_mesh.data_name,
#             fade_out_dist=generic_mesh.fade_out_dist,
#             flags=generic_mesh.flags,
#             link_name=safe_int(generic_mesh.name),
#             names=material_names,  # Use saved keys
#             type=ObjectType.MESH,
#         )
#         mesh_pc = TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC(
#             body=body,
#             class_name="Mesh_Z",
#             link_header=link_header,
#             link_name=safe_int(generic_mesh.name),
#             name=safe_int(generic_mesh.file_name),
#         )

#         wrapper = MeshV1_291_03_06_PC()
#         wrapper.file_path = generic_mesh.file_path
#         wrapper.mesh = mesh_pc
#         return wrapper

#     def to_generic(self) -> Mesh:
#         body: MeshBodyV1291_03_06PC = self.mesh.body
#         generic_mesh = Mesh()

#         for mat in body.material_names:
#             print(f"Material: {mat}")
#         generic_materials = load_dependencies(self.file_path, list(body.material_names))
#         for material in generic_materials:
#             if material is not None:
#                 print(f"{material.file_name!r} ->", str(material.name))
#             else:
#                 print(f"material was not found")

#         generic_mesh.file_path = self.file_path
#         generic_mesh.file_name = str(self.mesh.name)
#         generic_mesh.name = str(self.mesh.link_header.link_name)
#         generic_mesh.b_box = self.mesh.link_header.b_box
#         generic_mesh.b_sphere = self.mesh.link_header.b_sphere
#         generic_mesh.data_name = str(self.mesh.link_header.data_name)
#         generic_mesh.fade_out_dist = self.mesh.link_header.fade_out_dist
#         generic_mesh.flags = self.mesh.link_header.flags
#         generic_mesh.materials = list(generic_materials)

#         for generic_mat in generic_mesh.materials:
#             if generic_mat is not None:
#                 print(f"  Material: {generic_mat.name}")
#             else:
#                 print(f"  Material is None")

#         generic_mesh.col_spheres = list(body.sphere_cols)
#         generic_mesh.col_boxes = list(body.box_cols)
#         generic_mesh.col_cylindres = list(body.cylindre_cols)

#         tris = body.mesh_buffers.index_buffers[0].tris
#         vbuf = body.mesh_buffers.vertex_buffers[0]
#         pos_chunk, norm_chunk, uv_chunk, luv_chunk = decode_vertex_buffer(vbuf)

#         generic_mesh.positions = [list(pos) for pos in pos_chunk] if pos_chunk else []
#         generic_mesh.normals = [list(norm) for norm in norm_chunk] if norm_chunk else []
#         generic_mesh.uvs = [list(uv) for uv in uv_chunk] if uv_chunk else []
#         generic_mesh.luvs = [list(luv) for luv in luv_chunk] if luv_chunk else []

#         generic_mesh.faces = []
#         prim_infos = body.mesh_buffers.vertex_groups

#         for mat_id, prim in enumerate(prim_infos):
#             start = prim.index_buffer_index_begin // 3
#             for i in range(prim.face_count):
#                 tri = tris[start + i]
#                 face_verts = []

#                 for offset in tri:
#                     vert = Vertex(
#                         position_id=offset,
#                         normal_id=(offset if norm_chunk else None),
#                         uv_id=(offset if uv_chunk else None),
#                         luv_id=(offset if luv_chunk else None),
#                     )
#                     face_verts.append(vert)

#                 generic_mesh.faces.append(Face(vertices=face_verts, material_id=mat_id))

#         return generic_mesh
# old code above

from ..generic.mesh import Mesh, Vertex, Face
from ..common.mesh import decode_vertex_buffer
from ..common.resource import load_dependencies, save_dependencies
from collections import defaultdict
from ..bff.io import (
    MeshBodyV1291_03_06PC,
    TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC,
    MeshBuffers2,
    IndexBuffer,
    VertexBuffer,
    VertexGroup,
    LayoutNoBlend,
    VertexGroupFlags,
    Vertices,
    Morpher2,
    Points2,
    ObjectType,
    ObjectLinkHeaderV106_63_02PC,
    BoxCol2,
    CylindreCol4,
    SphereCol2,
)
from ...common.util import safe_int

MAX_VERTS = 65535
MAX_TRIS = MAX_VERTS // 3


class MeshV1_291_03_06_PC:
    file_path: str
    mesh: TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC

    def __init__(
        self,
        mesh: TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC = None,
    ):
        if mesh is not None:
            self.mesh = mesh.mesh_v1_291_03_06_pc
            self.file_path = mesh.file_path

    # ==================================================================
    # FROM GENERIC
    # ==================================================================

    @staticmethod
    def from_generic(generic_mesh: Mesh):
        faces_by_material = defaultdict(list)
        for face in generic_mesh.faces:
            faces_by_material[face.material_id].append(face)

        vertex_buffers = []
        index_buffers = []
        vertex_groups = []

        global_vertex_offset = 0

        # ------------------------------------------------------------
        # Build geometry per material
        # ------------------------------------------------------------
        for mat_id in sorted(faces_by_material.keys()):
            faces = faces_by_material[mat_id]

            vertex_map = {}
            material_vertices = []
            material_tris = []

            for face in faces:
                tri = []
                for v in face.vertices:
                    key = (
                        v.position_id,
                        v.normal_id if v.normal_id is not None else -1,
                        v.uv_id if v.uv_id is not None else -1,
                        v.luv_id if v.luv_id is not None else -1,
                    )
                    if key not in vertex_map:
                        idx = len(material_vertices)
                        vertex_map[key] = idx
                        pos = generic_mesh.positions[v.position_id]
                        norm = (
                            generic_mesh.normals[v.normal_id]
                            if v.normal_id is not None
                            else [0, 0, 0]
                        )
                        uv = (
                            generic_mesh.uvs[v.uv_id] if v.uv_id is not None else [0, 0]
                        )
                        luv = (
                            generic_mesh.luvs[v.luv_id]
                            if v.luv_id is not None
                            else [0, 0]
                        )
                        material_vertices.append((pos, norm, uv, luv))
                    tri.append(vertex_map[key])
                material_tris.append(tri)

            # ------------------------------------------------------------
            # Split vertex buffer
            # ------------------------------------------------------------
            vtx_cursor = 0
            while vtx_cursor < len(material_vertices):
                vb_start = vtx_cursor
                vb_end = min(vtx_cursor + MAX_VERTS, len(material_vertices))
                vb_index = len(vertex_buffers)

                # build vertex buffer slice
                layout = []
                for pos, norm, uv, luv in material_vertices[vb_start:vb_end]:
                    layout.append(
                        LayoutNoBlend(
                            position=pos,
                            normal=norm,
                            normal_w=0,
                            tangent=[0, 0, 0],
                            tangent_w=0,
                            uv=uv,
                            luv=luv,
                        )
                    )

                vertices = Vertices(
                    layout_position=None,
                    layout_position_uv=None,
                    layout_no_blend=layout,
                    layout1_blend=None,
                    layout4_blend=None,
                    layout_unknown=None,
                )

                vertex_buffers.append(VertexBuffer(flags=34, vertices=vertices))

                # collect tris fully inside this VB
                local_tris = []
                for tri in material_tris:
                    if all(vb_start <= i < vb_end for i in tri):
                        local_tris.append([i - vb_start for i in tri])

                # --------------------------------------------------------
                # Split index buffers
                # --------------------------------------------------------
                tri_cursor = 0
                while tri_cursor < len(local_tris):
                    chunk = local_tris[tri_cursor : tri_cursor + MAX_TRIS]
                    ib_index = len(index_buffers)

                    index_buffers.append(IndexBuffer(flags=34, tris=chunk))

                    vertex_groups.append(
                        VertexGroup(
                            len(chunk),  # face_count
                            VertexGroupFlags(1, 0, 0, 0, 0, 0, 0),
                            0,  # index_buffer_index_begin (local)
                            (vb_end - vb_start) - 1,
                            mat_id,
                            global_vertex_offset,
                            vb_end - vb_start,
                            36,
                            global_vertex_offset,
                            0,
                            [vb_index, ib_index, 0],
                        )
                    )

                    tri_cursor += MAX_TRIS

                global_vertex_offset += vb_end - vb_start
                vtx_cursor = vb_end

        # ------------------------------------------------------------
        # Materials
        # ------------------------------------------------------------
        dependencies = [m for m in generic_mesh.materials if m is not None]
        material_names = save_dependencies(generic_mesh.file_path, dependencies)

        mesh_buffers = MeshBuffers2(
            index_buffers=index_buffers,
            vertex_buffers=vertex_buffers,
            vertex_groups=vertex_groups,
            morpher=Morpher2([], []),
            unknowns=[],
        )

        body = MeshBodyV1291_03_06PC(
            box_cols=[
                BoxCol2(col_box=col.col_box, flag=col.flag, name=col.name)
                for col in generic_mesh.col_boxes
            ],
            collision_aabb_tris=[],
            collision_aabbs=[],
            cylindre_cols=[
                CylindreCol4(
                    col_cylindre=col.col_cylindre,
                    flag=col.flag,
                    name=col.name,
                )
                for col in generic_mesh.col_cylindres
            ],
            drawing_cutoff_distance=0.0,
            drawing_start_distance=0.0,
            material_names=material_names,
            mesh_buffers=mesh_buffers,
            normals=[],
            points=Points2([], [], []),
            related_to_counts=[0, 0, 0],
            shadow_related=0,
            sphere_cols=[
                SphereCol2(col_sph=col.col_sph, flag=col.flag, name=col.name)
                for col in generic_mesh.col_spheres
            ],
            strips=[],
            texcoords=[],
            unknown4_s=None,
            unknown5_s=[],
            unknown6_s=[],
            unknown8_s=[],
            vertices=[],
        )

        link_header = ObjectLinkHeaderV106_63_02PC(
            b_box=generic_mesh.b_box,
            b_sphere=generic_mesh.b_sphere,
            data_name=generic_mesh.data_name,
            fade_out_dist=generic_mesh.fade_out_dist,
            flags=generic_mesh.flags,
            link_name=safe_int(generic_mesh.name),
            names=material_names,
            type=ObjectType.MESH,
        )

        wrapper = MeshV1_291_03_06_PC()
        wrapper.file_path = generic_mesh.file_path
        wrapper.mesh = (
            TrivialClassForObjectLinkHeaderV106_63_02PCAndMeshBodyV1291_03_06PC(
                body=body,
                class_name="Mesh_Z",
                link_header=link_header,
                link_name=safe_int(generic_mesh.name),
                name=safe_int(generic_mesh.file_name),
            )
        )
        return wrapper

    # ==================================================================
    # TO GENERIC
    # ==================================================================

    def to_generic(self) -> Mesh:
        body = self.mesh.body
        generic_mesh = Mesh()

        generic_mesh.file_path = self.file_path
        generic_mesh.file_name = str(self.mesh.name)
        generic_mesh.name = str(self.mesh.link_header.link_name)
        generic_mesh.b_box = self.mesh.link_header.b_box
        generic_mesh.b_sphere = self.mesh.link_header.b_sphere
        generic_mesh.data_name = str(self.mesh.link_header.data_name)
        generic_mesh.fade_out_dist = self.mesh.link_header.fade_out_dist
        generic_mesh.flags = self.mesh.link_header.flags

        generic_mesh.materials = load_dependencies(
            self.file_path, list(body.material_names)
        )
        generic_mesh.col_spheres = list(body.sphere_cols)
        generic_mesh.col_boxes = list(body.box_cols)
        generic_mesh.col_cylindres = list(body.cylindre_cols)

        # ------------------------------------------------------------
        # Decode ALL vertex buffers
        # ------------------------------------------------------------
        pos_all, norm_all, uv_all, luv_all = [], [], [], []
        vb_offsets = []

        for vb in body.mesh_buffers.vertex_buffers:
            offset = len(pos_all)
            vb_offsets.append(offset)
            p, n, u, l = decode_vertex_buffer(vb)
            pos_all.extend(p or [])
            norm_all.extend(n or [])
            uv_all.extend(u or [])
            luv_all.extend(l or [])

        generic_mesh.positions = [list(v) for v in pos_all]
        generic_mesh.normals = [list(v) for v in norm_all] if norm_all else []
        generic_mesh.uvs = [list(v) for v in uv_all] if uv_all else []
        generic_mesh.luvs = [list(v) for v in luv_all] if luv_all else []

        # ------------------------------------------------------------
        # Rebuild faces from vertex groups
        # ------------------------------------------------------------
        generic_mesh.faces = []

        for vg in body.mesh_buffers.vertex_groups:
            vb_index, ib_index, _ = vg.zeroes
            vb_offset = vb_offsets[vb_index]
            ib = body.mesh_buffers.index_buffers[ib_index]

            for tri in ib.tris[: vg.face_count]:
                verts = []
                for idx in tri:
                    gi = vb_offset + idx
                    verts.append(
                        Vertex(
                            position_id=gi,
                            normal_id=gi if generic_mesh.normals else None,
                            uv_id=gi if generic_mesh.uvs else None,
                            luv_id=gi if generic_mesh.luvs else None,
                        )
                    )
                generic_mesh.faces.append(Face(vertices=verts, material_id=vg.unused))

        return generic_mesh
