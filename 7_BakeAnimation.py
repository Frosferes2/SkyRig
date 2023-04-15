import bpy

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')
    
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='DESELECT')
_layers = _skeleton.data.layers[:]
_skeleton.data.layers = [True for i in range(32)]

for pb in _skeleton.pose.bones:
    if 'SOURCE_RETARGET' in pb.constraints:
        pb.bone.select = True

_skeleton.data.layers[:] = _layers
