from maya import cmds, mel

""" 
This script creates a ribbon with 8 bind joints and 5 driver joints.
I'm using it for lips right now.
Jacob Lilly
"""

# Create ribbon geo (nurbs plane) and driver joints
l = 8
geo = cmds.nurbsPlane(n='ribbon_GEO', ax=(0,1,0),lr=0.1666666667, d=3, w=l, u=l, v=1, ch=0)
cmds.makeIdentity(geo, a=1, t=1, r=1, s=1)
cmds.DeleteHistory()


cmds.select(cl=1)
drv1 = cmds.joint(n='ribbon_01_DRV', p=(-4,0,0))
cmds.select(cl=1)
drv2 = cmds.joint(n='ribbon_02_DRV', p=(-2,0,0))
cmds.select(cl=1)
drv3 = cmds.joint(n='ribbon_03_DRV', p=(0,0,0))
cmds.select(cl=1)
drv4 = cmds.joint(n='ribbon_04_DRV', p=(2,0,0))
cmds.select(cl=1)
drv5 = cmds.joint(n='ribbon_05_DRV', p=(4,0,0))
drvs = [drv1, drv2, drv3, drv4, drv5]


"""Might automate above later. Hard-coded for now

	drvCount = 5
	drvs = []
	for i in range(1,drvCount+1):
		cmds.select(cl=1)
		x=i
		if i <= drvCount / 2:
			x = -i
		else:
			x = i
		drvs.append(cmds.joint(n='ribbon_0{}_DRV'.format(i), p=(x,0,0)))
	"""

# Create locator, group, and parent for each driver joint
grps = []
for drv in drvs:
	# Create locator and group
	loc = cmds.spaceLocator()
	grp = cmds.group(em=1)
	
	# Move grp, loc, ctl to jnt
	cnst1 = cmds.parentConstraint(drv, grp)
	cnst2 = cmds.parentConstraint(drv, loc)
	cmds.delete(cnst1, cnst2)
	
	# Hierarchy
	cmds.parent(loc, grp)
	cmds.parent(drv, loc)

	# Freeze Transforms
	cmds.makeIdentity(drv, a=1, t=1, r=1, s=1, n=0)

	# Rename
	cmds.select(loc)
	cmds.rename(drv + '_LOC')
	cmds.select(grp)
	grp = cmds.rename(drv + '_GRP')

	# Mirror negative drivers
	if cmds.getAttr(grp + '.tx') < 0:
		cmds.setAttr(grp + '.ry', 180)
		cmds.setAttr(grp + '.sz', -1)

	# Add to list so I can group them all after
	grps.append(grp)

cmds.select(grps)
cmds.group()

# Create hair follicles and delete unneccessary stuff.
# (Later, I might replace this with creating just follicles 
# and manually connecting them)
cmds.select(geo)
mel.eval('createHair {} 1 10 0 0 0 0 5 0 2 2 1;'.format(l))
cmds.delete('hairSystem1', 'hairSystem1OutputCurves', 'nucleus1')
folGrp = cmds.rename('hairSystem1Follicles', 'ribbon_FOL_GRP')
i=1
jnt,folName = '',''
for fol in cmds.listRelatives(folGrp, c=1):
	cmds.delete(cmds.listRelatives(fol,c=1)[1])
	cmds.select(fol)
	jnt = cmds.joint()
	folName = cmds.rename(fol, 'ribbon_{}{}_FOL'.format('0', str(i)))
	jnt = cmds.rename(jnt, folName.replace('_FOL', '_BND'))
	cmds.setAttr(jnt + '.radius', .2)
	i+=1
	
# Bind geometry to the driver joints
cmds.select(drvs, geo)
mel.eval('SmoothBindSkin;')


"""
Things to fix:

Fairly hard-coded for that setup (good for lips) right now,
but might make it more flexible later.

Errors if you make multiple ribbons (due to naming).
Currently I get around this by renaming the existing ribbon stuff
with a renaming tool.
"""
