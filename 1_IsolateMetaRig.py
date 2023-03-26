import bpy

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')
    
_nodeList = ['AnimObjectA', 'AnimObjectB', 'AnimObjectL', 'AnimObjectR', 'SHIELD',
        'WEAPON', 'MagicEffectsNode', 'NPC MagicNode [Mag].L', 'NPC MagicNode [Mag].R',
        'NPC Head MagicNode [Hmag]', 'Camera3rd [Cam3]', 'Camera Control', 'NPC Neck [Neck]']

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        _nodeList.extend(obj.vertex_groups.keys())
    
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.armature.select_all(action='DESELECT')

for key in list(dict.fromkeys(_nodeList)):
    try:
        _skeleton.data.edit_bones[key].select = True
    except KeyError:
        print('Node {} was not found in armature bone list'.format(key))
        pass
    
bpy.ops.armature.select_all(action='INVERT')
bpy.ops.armature.delete()
