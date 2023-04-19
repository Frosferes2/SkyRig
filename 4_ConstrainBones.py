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
    
for _empty in _empties:
    _empty.location[:] = (0.0, 0.0, 0.0)
    _empty.rotation_mode = 'QUATERNION'
    _empty.rotation_quaternion[:] = (1.0, 0.0, 0.0, 0.0)
    
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='DESELECT')
_skeleton.data.pose_position = 'REST'
bpy.context.view_layer.update()

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
    if 'RIG_POSITION' in pb.constraints:
        _constraint = pb.constraints['RIG_POSITION']
    else:
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        _constraint = pb.constraints[-1]
        _constraint.name = 'RIG_POSITION'
        
    _constraint.target = _empty
    
    if 'RIG_ROTATION' in pb.constraints:
        _constraint = pb.constraints['RIG_ROTATION']
    else:
        bpy.ops.pose.constraint_add(type='COPY_ROTATION')
        _constraint = pb.constraints[-1]
        _constraint.name = 'RIG_ROTATION'
        
    _constraint.target = _empty
    
    if 'RIG_SCALE' in pb.constraints:
        _constraint = pb.constraints['RIG_SCALE']
    else:
        bpy.ops.pose.constraint_add(type='COPY_SCALE')
        _constraint = pb.constraints[-1]
        _constraint.name = 'RIG_SCALE'
        
    _constraint.target = _empty
    _constraint.use_make_uniform = True
    
    _empty.location = pb.matrix.to_translation() - _empty.matrix_world.to_translation()
    _rotCache = _empty.matrix_world.to_quaternion()
    _empty.rotation_quaternion = pb.matrix.to_quaternion()
    _empty.rotation_quaternion.rotate(_rotCache.inverted())
    
bpy.ops.pose.select_all(action='INVERT')
bpy.ops.pose.hide()
_skeleton.data.pose_position = 'POSE'
