import bpy

bl_info = {
    "name": "Print verts",
    "author": "rlneumiller@gmail.com",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode > Vertex > Print vertices to console",
    "description": "Print vertices of the active object to the console",
    "category": "Development",
}

def print_verts():
    obj = bpy.context.active_object
    mesh = obj.data

    print("\033c") # Clear the console
    print("/033")

    print(obj.name + " = [")

    for i, vertex in enumerate(mesh.vertices):
        print(f"({vertex.co.x}, {vertex.co.y}, {vertex.co.z})", end="")
        if i != len(mesh.vertices) - 1:
            print(",")
            
    print('\n]')
    

class PrintVerts(bpy.types.Operator):
    """Print vertices of the active object to the console"""
    bl_idname = "development.print_verts"
    bl_label = "Print vertices of active object to the console"
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
