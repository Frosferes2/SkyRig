import bpy

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')
    
_collection = bpy.data.collections.new('Rig Empties')
bpy.context.scene.collection.children.link(_collection)

for key in _skeleton.data.bones.keys():
    if key.startswith('DEF-') is False and key not in ('root', 'torso'):
        continue
    
    print('Attaching empty to {}'.format(key))
    bpy.ops.object.empty_add()
    _empty = bpy.context.object
    if key.startswith('DEF-'):
        _empty.name = key[4:]
    else:
        _empty.name = key
        
    bpy.ops.object.constraint_add(type='COPY_TRANSFORMS')
    _constraint = _empty.constraints['Copy Transforms']
    _constraint.target = _skeleton
    _constraint.subtarget = key
    _constraint.mix_mode = 'BEFORE'
    if _empty.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(_empty)
    else:
        bpy.data.collections[_empty.users_collection[0].name].objects.unlink(_empty)
        
    _collection.objects.link(_empty)
    