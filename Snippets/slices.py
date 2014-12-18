# slices.py by Tamito Kajiyama
# https://blenderyard.wordpress.com/2014/10/17/contour-lines-as-in-maps/

import bpy
import math
from mathutils import Vector
 
def exec_slices(context, interval):
    print('interval', interval)
 
    ob = context.active_object
    ob.update_from_editmode()
    print('ob.name', ob.name)
 
    rad = max(Vector(point).length for point in ob.bound_box)
    print('rad', rad)
 
    zmin = min(point[2] for point in ob.bound_box)
    zmax = max(point[2] for point in ob.bound_box)
    print('zmin', zmin, 'zmax', zmax)
 
    imin = int(math.ceil(zmin / interval))
    imax = int(math.floor(zmax / interval))
    zvals = [i * interval for i in range(imin, imax+1)]
    print('zvals', zvals)
 
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.vertex_group_add()
 
    rot = Vector((0.0, 0.0, 0.0))
    for z in zvals:
        loc = Vector((0.0, 0.0, z)) + ob.location
        do_slice(rad, loc, rot)
 
    bpy.ops.object.vertex_group_remove(all=False)
    bpy.ops.object.mode_set(mode='OBJECT')
 
def do_slice(rad, loc, rot):
    bpy.ops.mesh.primitive_plane_add(radius=rad, location=loc, rotation=rot)
 
    bpy.ops.object.vertex_group_assign()
 
    bpy.ops.mesh.intersect()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.mark_freestyle_edge()
    bpy.ops.mesh.select_all(action='DESELECT')
 
    bpy.ops.object.vertex_group_select()
 
    bpy.ops.mesh.delete(type='VERT')
 
class Slices(bpy.types.Operator):
    """Slices"""
    bl_idname = "object.slices"
    bl_label = "Slices"
    bl_options = {'REGISTER', 'UNDO'}
 
    interval = bpy.props.FloatProperty(name="Slice Interval", default=1.0, min=0.01, max=100)
 
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob is not None and ob.type == 'MESH'
 
    def execute(self, context):
        exec_slices(context, self.interval)
        return {'FINISHED'}
 
def register():
    bpy.utils.register_class(Slices)
 
def unregister():
    bpy.utils.unregister_class(Slices)
 
if __name__ == "__main__":
    register()
 
    # test call
    bpy.ops.object.slices(interval=0.1)