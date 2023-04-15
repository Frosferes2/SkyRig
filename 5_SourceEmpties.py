import bpy

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')
    
try:
    _namePairs = bpy.context.scene['_namePairs']
except KeyError:
    raise Exception('Name pairs object is missing, run bone name script on meta-rig')
    
_collection = bpy.data.collections.new('Source Empties')
bpy.context.scene.collection.children.link(_collection)

for key in _skeleton.data.bones.keys():
    if key not in _namePairs.keys():
        continue
    
    print('Attaching empty to {}'.format(key))
    bpy.ops.object.empty_add()
    _empty = bpy.context.object
    _empty.name = 'SRC_' + key
    bpy.ops.object.constraint_add(type='COPY_TRANSFORMS')
    _constraint = _empty.constraints['Copy Transforms']
    _constraint.target = _skeleton
    _constraint.subtarget = key
    _constraint.mix_mode = 'BEFORE_SPLIT'
    if _empty.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(_empty)
    else:
        bpy.data.collections[_empty.users_collection[0].name].objects.unlink(_empty)
        
    _collection.objects.link(_empty)
    