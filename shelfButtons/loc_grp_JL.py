from maya import cmds, mel

for jnt in cmds.ls(sl=1):
	# Create controller, locator, and group
	loc = cmds.spaceLocator()
	grp = cmds.group(em=1)
	
	# Move grp, loc, ctl to jnt
	cnst1 = cmds.parentConstraint(jnt, grp)
	cnst2 = cmds.parentConstraint(jnt, loc)
	cmds.delete(cnst1, cnst2)
	
	# Hierarchy
	cmds.parent(loc, grp)
	cmds.parent(jnt, loc)

	# Freeze Transforms
	cmds.makeIdentity(jnt, a=1, t=1, r=1, s=1, n=0)

	# Rename
	cmds.select(loc)
	cmds.rename(jnt.replace(jnt[-3:], 'LOC'))
	cmds.select(grp)
	cmds.rename(jnt.replace(jnt[-3:], 'GRP'))