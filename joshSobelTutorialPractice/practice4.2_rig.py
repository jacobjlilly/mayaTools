import maya.cmds as cmds
import maya.mel as mel
import sys

# Create rig from proxy locators

locs = cmds.ls('*_PRX')
if not locs:
	sys.stdout.write('No locators found. Try running proxy locators script.')

sc=0

for loc in locs:

	# Get locator's parent
	par = cmds.listRelatives(loc, p=1)

	# Joints
	cmds.select(cl=1)
	jnt = cmds.joint(n=loc.replace('_PRX', '_JNT'), sc=sc)
	cnst = cmds.parentConstraint(loc, jnt)
	cmds.delete(cnst)
	cmds.makeIdentity(jnt, a=1, r=1, s=1)
	if par:
		parJnt = par[0].replace('_PRX', '_JNT')
		cmds.parent(jnt, parJnt)

	# Controls
	con = cmds.circle(n=loc.replace('_PRX', '_CTL'), ch=0)
	grp = cmds.group(n=loc.replace('_PRX', '_GRP'), em=1, w=1)
	cmds.parent(con, grp)
	cnst = cmds.parentConstraint(loc, grp)
	cmds.delete(cnst)
	cmds.makeIdentity(con, a=1, t=1, r=1, s=1)
	
	if par:
		print par
		parCon = par[0].replace('_PRX', '_CTL')
		cmds.parent(grp, parCon)

	cmds.parentConstraint(con, jnt)

# Delete proxy locators
cmds.delete(locs)