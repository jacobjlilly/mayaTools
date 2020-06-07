"""
Mirrors joints regardless of their position in hierarchy
for mirrored rotation behavior
"""

from maya import cmds, mel

#Strings to search and replace for new joints' names
search = 'L_'
replace = 'R_'

sel = cmds.ls(sl=1)
cmds.select(cl=1)
mirrorJnt = cmds.joint(n='temp_mirror_JNT')

for jnt in sel:
	parJnt = 0
	if cmds.listRelatives(jnt, p=1):
		parJnt = cmds.listRelatives(jnt, p=1)
		
	cmds.parent(jnt, mirrorJnt)
	cmds.mirrorJoint(myz=1, mb=1, sr=(search, replace))
	cmds.parent(w=1)
	
	#Reparent joint to its original parent
	if parJnt:
		cmds.parent(jnt, parJnt)

cmds.delete(mirrorJnt)