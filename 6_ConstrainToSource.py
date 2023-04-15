import bpy

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')

try:
    _empties = bpy.data.collections['Source Empties'].all_objects
except KeyError:
    raise Exception('Source collection is missing, run empties script on import skeleton')
    
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
_layers = _skeleton.data.layers[:]
_skeleton.data.layers = [True for i in range(32)]
_skeleton.data.pose_position = 'REST'
bpy.context.view_layer.update()

for pb in _skeleton.pose.bones:
    pb['IK_FK'] = 1.0

for _from, _to in _namePairs.items():
    _empty = _empties['SRC_' + _from]
    if _from in _skeleton.pose.bones.keys():
        pb = _skeleton.pose.bones[_from]
    elif _to in _skeleton.pose.bones.keys():
        pb = _skeleton.pose.bones[_to]
    elif _to + '_fk' in _skeleton.pose.bones.keys():
        pb = _skeleton.pose.bones[_to + '_fk']
    elif _to[:-2] + '_fk' + _to[-2:] in _skeleton.pose.bones.keys():
        pb = _skeleton.pose.bones[_to[:-2] + '_fk' + _to[-2:]]
    else:
        print('WARNING: no corresponding pose bone found for source empty ' + _empty.name)
        continue
    
    print('Constraining bone {} to empty {}'.format(pb.name, _empty.name))
    _skeleton.data.bones.active = pb.bone
    if 'SOURCE_RETARGET' in pb.constraints:
        _constraint = pb.constraints['SOURCE_RETARGET']
    else:
        bpy.ops.pose.constraint_add(type='COPY_TRANSFORMS')
        _constraint = pb.constraints['Copy Transforms']
        _constraint.name = 'SOURCE_RETARGET'
        
    _constraint.target = _empty
    _empty.location = pb.matrix.to_translation() - _empty.matrix_world.to_translation()
    _rotCache = _empty.matrix_world.to_quaternion()
    _empty.rotation_quaternion = pb.matrix.to_quaternion()
    _empty.rotation_quaternion.rotate(_rotCache.inverted())
    
bpy.ops.pose.select_all(action='DESELECT')
_skeleton.data.layers[:] = _layers
_skeleton.data.pose_position = 'POSE'
