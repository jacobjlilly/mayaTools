from maya import cmds, mel

def ctlBuild(jnt):
	# Builds and names a nurbs circle and offset group
	# for a selected joint
	
	ctlSize = .1
	cmds.select(cl=1)
	
	# Create controller curve and offset group
	ctl = cmds.circle(n = jnt.replace(jnt[-3:], 'ctl'))
	cmds.setAttr('{}.scaleX'.format(ctl[0]), ctlSize)
	cmds.setAttr('{}.scaleY'.format(ctl[0]), ctlSize)
	cmds.setAttr('{}.scaleZ'.format(ctl[0]), ctlSize)
	cmds.makeIdentity(ctl, a=1, t=1, r=1, s=1, n=0)
	grp = cmds.group(em=1, n = jnt.replace(jnt[-3:], 'grp'))
	cmds.parent(ctl[0], grp)
	
	# Move offset group to joint
	cnst = cmds.parentConstraint(jnt, grp)
	cmds.delete(cnst)
	
	return ctl, grp
	
def ctlBuildHierarchy(jnt):
	# Builds, names, and organizes nurbs circles and offset groups
	# for the child hierarchy of a selected joint
	
	par = ctlBuild(jnt)
	parCtl = par[0][0]
	parGrp = par[1]
	
	# Recurse and arrange hierarchy
	if cmds.listRelatives(jnt, c=1):
		jntChildren = cmds.listRelatives(jnt, c=1)
		for child in jntChildren:
			cmds.parent(ctlBuildHierarchy(child), parCtl)
				
	return parGrp

ctlBuildHierarchy(cmds.ls(sl=1)[0])
	