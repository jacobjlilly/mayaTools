# replaceCurves_JL
# Replaces curves using "parent -r -s"
# Select the old curve you want to replace last

from maya import cmds

children, par = cmds.ls(sl=1)[0:-1], cmds.ls(sl=1)[-1]
cmds.makeIdentity(par, a=1, t=1, r=1, s=1)
ogShape = cmds.listRelatives(par, c=1, s=1)

for child in children:
	cmds.makeIdentity(child, a=1, t=1, r=1, s=1)
	shape = cmds.listRelatives(child, c=1, s=1)
	
	for s in shape:
		cmds.parent(s, par, r=1,s=1)
		
	cmds.delete(child)

cmds.delete(ogShape)