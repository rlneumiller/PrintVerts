import bpy
import json
import os

bl_info = {
    "name": "Print verts",
    "author": "rlneumiller@gmail.com",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode > Vertex > Print vertices to console",
    "description": "Print the vertices of the active object to a file and to the console ",
    "category": "Development",
}
def float_to_str(num, precision=3):  # Default precision is 3
    return f"{num:.{precision}f}"

def print_verts():
    obj = bpy.context.active_object
    mesh = obj.data

    if not mesh.vertices:
        print("Error: The active object has no vertices.")
        return

    print("\033c", end="")  # Clear console 

    vertices_data = {
        obj.name: [
            {"x": float_to_str(v.co.x), "y": float_to_str(v.co.y), "z": float_to_str(v.co.z)}
            for v in mesh.vertices
        ]
    }

    blend_file_directory = os.path.dirname(bpy.data.filepath)
    output_file_path = os.path.join(blend_file_directory, f"{obj.name}.json")

    with open(output_file_path, "w") as outfile:
        json.dump(vertices_data, outfile, default=float_to_str, indent=4)

    print(f"Vertices saved to: {output_file_path}")
    print(json.dumps(vertices_data, default=float_to_str, indent=4))
    
class PrintVerts(bpy.types.Operator):
    """Print the vertices of the active object to the console and aa a file in the blend file directory"""
    bl_idname = "development.print_verts"
    bl_label = "Print vertices of active object to a console and a file"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context):
        print_verts()
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(PrintVerts.bl_idname)

def register():
    bpy.utils.register_class(PrintVerts)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)

def unregister():
    bpy.utils.unregister_class(PrintVerts)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)
