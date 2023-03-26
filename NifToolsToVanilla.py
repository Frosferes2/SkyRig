import bpy

_skeleton = bpy.context.active_object
if _skeleton.type != 'ARMATURE':
    raise Exception('Active object is not an armature')
    
_namePairs = {
'NPC L Calf [LClf]': 'NPC Calf [Clf].L',
'NPC L Clavicle [RClv]': 'NPC Clavicle [Clv].L',
'NPC L Finger00 [RF00]': 'NPC Finger00 [RF00].L',
'NPC L Finger01 [RF01]': 'NPC Finger01 [RF01].L',
'NPC L Finger02 [RF02]': 'NPC Finger02 [RF02].L',
'NPC L Finger10 [RF10]': 'NPC Finger10 [RF10].L',
'NPC L Finger11 [RF11]': 'NPC Finger11 [RF11].L',
'NPC L Finger12 [RF12]': 'NPC Finger12 [RF12].L',
'NPC L Finger20 [RF20]': 'NPC Finger20 [RF20].L',
'NPC L Finger21 [RF21]': 'NPC Finger21 [RF21].L',
'NPC L Finger22 [RF22]': 'NPC Finger22 [RF22].L',
'NPC L Finger30 [RF30]': 'NPC Finger30 [RF30].L',
'NPC L Finger31 [RF31]': 'NPC Finger31 [RF31].L',
'NPC L Finger32 [RF32]': 'NPC Finger32 [RF32].L',
'NPC L Finger40 [RF40]': 'NPC Finger40 [RF40].L',
'NPC L Finger41 [RF41]': 'NPC Finger41 [RF41].L',
'NPC L Finger42 [RF42]': 'NPC Finger42 [RF42].L',
'NPC L Foot [Lft ]': 'NPC Foot [ft ].L',
'NPC L Forearm [RLar]': 'NPC Forearm [RLar].L',
'NPC L ForearmTwist1 [LLt1]': 'NPC ForearmTwist1 [Lt1].L',
'NPC L ForearmTwist2 [LLt2]': 'NPC ForearmTwist2 [Lt2].L',
'NPC L Hand [RHnd]': 'NPC Hand [RHnd].L',
'NPC L MagicNode [LMag]': 'NPC MagicNode [Mag].L',
'NPC L RearCalf [LrClf]': 'NPC RearCalf [rClf].L',
'NPC L Thigh [LThg]': 'NPC Thigh [Thg].L',
'NPC L Toe0 [LToe]': 'NPC Toe0 [Toe].L',
'NPC L UpperArm [RUar]': 'NPC UpperArm [RUar].L',
'NPC L UpperarmTwist1 [LUt1]': 'NPC UpperarmTwist1 [Ut1].L',
'NPC L UpperarmTwist2 [LUt2]': 'NPC UpperarmTwist2 [Ut2].L',
'NPC R Calf [LClf]': 'NPC Calf [LClf].R',
'NPC R Clavicle [RClv]': 'NPC Clavicle [Clv].R',
'NPC R Finger00 [RF00]': 'NPC Finger00 [F00].R',
'NPC R Finger01 [RF01]': 'NPC Finger01 [F01].R',
'NPC R Finger02 [RF02]': 'NPC Finger02 [F02].R',
'NPC R Finger10 [RF10]': 'NPC Finger10 [F10].R',
'NPC R Finger11 [RF11]': 'NPC Finger11 [F11].R',
'NPC R Finger12 [RF12]': 'NPC Finger12 [F12].R',
'NPC R Finger20 [RF20]': 'NPC Finger20 [F20].R',
'NPC R Finger21 [RF21]': 'NPC Finger21 [F21].R',
'NPC R Finger22 [RF22]': 'NPC Finger22 [F22].R',
'NPC R Finger30 [RF30]': 'NPC Finger30 [F30].R',
'NPC R Finger31 [RF31]': 'NPC Finger31 [F31].R',
'NPC R Finger32 [RF32]': 'NPC Finger32 [F32].R',
'NPC R Finger40 [RF40]': 'NPC Finger40 [F40].R',
'NPC R Finger41 [RF41]': 'NPC Finger41 [F41].R',
'NPC R Finger42 [RF42]': 'NPC Finger42 [F42].R',
'NPC R Foot [Lft ]': 'NPC Foot [Lft ].R',
'NPC R Forearm [RLar]': 'NPC Forearm [Lar].R',
'NPC R ForearmTwist1 [RLt1]': 'NPC ForearmTwist1 [Lt1].R',
'NPC R ForearmTwist2 [RLt2]': 'NPC ForearmTwist2 [Lt2].R',
'NPC R Hand [RHnd]': 'NPC Hand [Hnd].R',
'NPC R MagicNode [RMag]': 'NPC MagicNode [Mag].R',
'NPC R RearCalf [RrClf]': 'NPC RearCalf [rClf].R',
'NPC R Thigh [RThg]': 'NPC Thigh [Thg].R',
'NPC R Toe0 [LToe]': 'NPC Toe0 [LToe].R',
'NPC R UpperArm [RUar]': 'NPC UpperArm [Uar].R',
'NPC R UpperarmTwist1 [RUt1]': 'NPC UpperarmTwist1 [Ut1].R',
'NPC R UpperarmTwist2 [RUt2]': 'NPC UpperarmTwist2 [Ut2].R',
}

for _from, _to in _namePairs.items():
    
    for bone in _skeleton.data.bones:
        if bone.name == _from:
            bone.name = _to
        elif bone.name == _to:
            bone.name = _from
