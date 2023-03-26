import bpy

_renameBones = True

_preventOverwrite = True

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')
    
try:
    _text = bpy.data.texts['{}_BoneNames.py'.format(_skeleton.name)]
except KeyError:
    bpy.ops.text.new()
    _text = bpy.data.texts['Text']
    _text.name = '{}_BoneNames.py'.format(_skeleton.name)
    pass
else:
    if _preventOverwrite:
        raise Exception("""This would overwrite previous bone list.
If you are sure, set _preventOverwrite to False""")
    _text.clear()
    
_text.write("""import bpy

_skeleton = bpy.data.objects['{}']

_namePairs = {{
'NPC Root [Root]': 'root',
'NPC COM [COM ]': 'torso',\n""".format(_skeleton.name))

for _from in sorted(_skeleton.data.bones.keys()):
    _to = _from
    
    if _renameBones is False:
        _text.write("'{}': '{}',\n".format(_from, _to))
        continue
    
    if _to.startswith('NPC '):
        _to = _to[4:]
        
    _sq = _to.find('['), _to.find(']')
    if (_sq[0] and _sq[1]) != -1 and _sq[0] < _sq[1]:
        _to = _to[:_sq[0]] + _to[_sq[1] + 1:]
    
    if _to.endswith('.L') is False and _to.endswith('.R') is False:
        _lr = _to.find('L'), _to.find('R')
        
        if _lr[0] != -1 and (_lr[1] == -1 or _lr[0] < _lr[1]):
            _to = _to.replace('L', '', 1)
            _to += '.L'
        elif _lr[1] != -1 and (_lr[0] == -1 or _lr[0] > _lr[1]):
            _to = _to.replace('R', '', 1)
            _to += '.R'
            
    _to = _to.replace('  ', ' ')
    _to = _to.replace(' .', '.')
    _to = _to.strip()
    _text.write("'{}': '{}',\n".format(_from, _to))
    
_text.write("""}

_dupe = len(_namePairs.values()) - len(set(_namePairs.values()))
if _dupe != 0:
    raise Exception('Found {} duplicate(s) in the list of bone names'.format(_dupe))

for _from, _to in _namePairs.items():
    
    for bone in _skeleton.data.bones:
        if bone.name == _from:
            bone.name = _to
        elif bone.name == _to:
            bone.name = _from
            
bpy.context.scene['_namePairs'] = _namePairs\n""")
