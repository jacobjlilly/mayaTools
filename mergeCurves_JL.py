# mergeCurves_JL
# Merges curves using "parent -r -s"
# Select the parent curve last

from maya import cmds

children, par = cmds.ls(sl=1)[0:-1], cmds.ls(sl=1)[-1]
cmds.makeIdentity(par, a=1, t=1, r=1, s=1)

for child in children:
	cmds.makeIdentity(child, a=1, t=1, r=1, s=1)
	shape = cmds.listRelatives(child, c=1, s=1)
	
	for s in shape:
		cmds.parent(s, par, r=1,s=1)
		
	cmds.delete(child)
	