import bpy

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')

try:
    _empties = bpy.data.collections['Rig Empties'].all_objects
except KeyError:
    raise Exception('Empties collection is missing, run empties script on animation rig')
    
try:
    _namePairs = bpy.context.scene['_namePairs']
except KeyError:
    raise Exception('Name pairs object is missing, run bone name script on meta-rig')
    
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='DESELECT')

for _from, _to in _namePairs.items():
    if _from in _empties.keys():
        _empty = _empties[_from]
    elif _to in _empties.keys():
        _empty = _empties[_to]
    else:
        print('WARNING: {} was not found in rig empty list'.format(_from))
        continue
    
    pb = _skeleton.pose.bones[_from]
    print('Constraining bone {} to empty {}'.format(pb.name, _empty.name))
    _skeleton.data.bones.active = pb.bone
    if 'Copy Transforms' not in pb.constraints:
        bpy.ops.pose.constraint_add(type='COPY_TRANSFORMS')
        
    pb.constraints['Copy Transforms'].target = _empty
    _empty.rotation_mode = 'QUATERNION'
    if _empty.rotation_quaternion[:] != (1.0, 0.0, 0.0, 0.0):
        print('WARNING: Empty {} already has a rotation applied. Ignoring'.format(_empty.name))
        continue
    
    _rotCache = _empty.matrix_world.to_quaternion()
    _empty.rotation_quaternion = pb.matrix.to_quaternion()
    _empty.rotation_quaternion.rotate(_rotCache.inverted())
    
bpy.ops.pose.select_all(action='INVERT')
bpy.ops.pose.hide()
