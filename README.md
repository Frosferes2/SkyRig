# SkyRig
These will work with any vanilla skeleton and modified skeletons such as XPMSE. It is assumed that the user has a reasonable 
level of experience with Blender, and so the intricacies of armature objects such as bone parenting and rigify usage will
not be discussed beyond what specific information relates to the scripts.

I am considering integrating these scripts into an interactive UI element to improve user friendliness, but I am unsure if SkyRig 
will have enough users to justify the time investment. If this is something you would be interested in, please let me know. 
Feedback on SkyRig is very much appreciated.

   Background

Skyrim's skeleton nodes are point-like, and thus preserve no information about bone tails and their connections.
Additionally, the bone axis orientations are not consistent with Blender's standards. Because exported animations are very
sensitive to deviations in bone orientations, it is not feasible to simply export animation data from a standard Blender 
rigify object for use in game. Instead, we can constrain the movements of a compatible export skeleton to a series of empty
objects, which are in turn constrained to this animation rig. These empty objects have corrective rotations applied to them,
allowing the export skeleton to copy the movements of the animation rig whilst preserving its original rotation data.

The general outline for the process of setting up an rig for producing Skyrim compatible animations is as follows:
   - Isolate the needed bones from the base skeleton.nif file
   - Produce a rigify compatible meta-rig from this striped down skeleton
   - Generate a rigify animation rig
   - Constrain the movements of the unmodified skeleton to the animation rig using empties

To begin, import the skeleton.nif you wish to turn into an animation rig. These scripts are written with NifTools in mind, but
should work fine for alternative addons such as Bad Dog's PyNifly. Next, import some skinned meshes that use the needed animation
nodes in the skeleton. Examples of these include the body, head, hands, feet and clothes such as skirts/capes. These will serve
as a visual model for your animations and the scripts will use them to determine which nodes are needed for the rig. Information
printed by all the scripts including warnings and constraint information can be found in Window > System Console.

   1_IsolateMetaRig

   - Duplicate the imported armature object; this duplicate will be used as the basis for our meta-rig
   - Shift-select all the meshes and the target armature, such that the armature is active
   - If the armature is active, its outline will be yellow instead of orange
   - Run the first script; this will add bones from the mesh vertex skinning groups to a list of animation and utility nodes,
   which will be isolated from the skeleton
   - This process will also isolate any HDT enabled bones are present in your meshes, you may want to delete these manually
   - After running the script, you should check the skeleton bone relations and make any needed corrections
   - If any overlapping bones are found, they should also be safe to delete
   - DO NOT rename any bones in the skeleton at this time

   2_SetBoneNames

   - The second script is ran on the corrected skeleton. It will generate a new text block containing a list of the current
   bone names on the left, and the names that the bones are to be renamed to on the right
   - Additionally, the riggify bones 'root' and 'torso' will be matched to the skyrim bones 'NPC Root' and 'NPC COM'
   - Boolean _renameBones if True will automatically generate a set of new, symmetrical bone names using my own protocol
   - If False, the set of renamed bones will be the same as the default
   - The skeleton bones will not be renamed until this new text block is ran, so you are free to make any adjustments to the
   right hand names before doing so
   - DO NOT rewrite the default names on the left hand side, only the renaming list on the right
   - The automatic renaming protocol is decently robust but can make mistakes, it is highly recommended you check the renaming
   list for errors after generation
   - When ran, the generated script will check for duplicates in the bone name list and stop if any are found, these must be
   corrected
   - This script will then toggle the bones in the skeleton between their default and new names each time it is ran
   - The new script must be ran at least once to commit the name pairs list to the scene variables for later use by script 4
   - Script 2 can be re-ran to regenerate the bone list, but only if the safeguard boolean _preventOverwrite is set to False
   - If you want to regenerate the name pair list or make subsequent adjustments to the bone names, make sure the skeleton is
   set to the default names first
   - From this point you are free to add new control bones or manipulate the bone tails and roll/rotations to begin constructing 
   a rigify meta-rig

   3_AttachEmpties
    
   - Simply run this script on the rigify armature after it has been generated from your completed meta-rig
   - The rigify object contains a set of bones which are duplicates of the meta-rig with the prefix 'DEF-'
   - The script will target these bones, along with 'root' and 'torso' and constrain a new empty object to each one
   - The empty objects will be added to a new collection named 'Rig Empties'
   - If the empties list needs regenerating, such as if the rig bones are rotated or their names are changed, delete the
   empties collection and re-run script 3

   4_ConstrainBones

   - The fourth script is ran on the original, unmodified skeleton, which will be used to export the animation data
   - This script will retrieve the name pair list scene variable and use it to match the export skeleton bones to the empties
   - When a match is made, the skeleton bone is constrained to the empty, and an offset is applied to the position and rotation of the empty such that the transformations of the bone are preserved
   - Now any change in the animation rig's pose will be reflected in the export skeleton, provided both are in pose position
   - If your imported skinned meshes are targetting the skeleton, you should be able to see these move as well
   - The empty collection and the export skeleton can be safely hidden to improve visual clarity
   - Script 4 can be re-ran if the empties collection has been modified in some way

The remaining scripts are either optional or relate to the propagation of imported animation and pose data to the animation rig. If you want to import animations, you must first create a new 'source' armature. This armature is a copy of the unmodified skeleton.nif onto which .kf data converted from .hkx via HKXCMD is imported.

   5_SourceEmpties

   - This script operates very similarly to script 3 and is ran on the source skeleton
   - It uses the cached bone name variable to choose the appropriate bones to constrain a set of 'Source Empties' to

   6_ConstrainToSource

   - Similar to script 4 and is ran on the animation rig
   - The script will automatically set all present rigify limbs to FK controls, which is needed for correct pose mapping
   - The script then matches the rig bones to their appropriate source empties and corrects for positional and rotational offset
   - The added constraints are given the name 'SOURCE_RETARGET', which will be needed later
   - The animation rig will now follow the source skeleton as it animates, but is now unusable since constrained bones cannot be moved manually
   - It is therefore necessary to bake the animation to the rig and remove the constraints to allow for free motion

   7_BakeAnimation

   - This is a simple utility script to select all rig pose bones with the SOURCE_RETARGET constraint
   - With these bones selected, go to Pose > Animation > Bake Action
   - In the menu that appears, set the frame range for the current animation
   - Check the boxes: 'Only Selected Bones', 'Visual Keying' and 'Clear Constraints'
   - Press OK, this operation may take a short while to complete
   - Now the animation rig will have its own copy of the source key frame data, and can be moved around freely
   - The animations are only applied to the FK controllers in the animation rig
   - Rigify adds a UI button which allows the user to snap the rig IK to FK for all keyframes in the current action

   NifToolsToVanilla

NifTools will automatically attempt to symmetrize the bones and vertex groups of anything it imports... and does a poor job of it.
There is also no way to disable this process. This script will swap the target armature between the imported NifTools bone names
and the vanilla bone names. If you are renaming bones, either manually or using my protocol, this is not necessary. This script
is simply here as a utility for people who may need to use vanilla bone names. For example, to bridge the gap between NifTools
and PyNifly.
