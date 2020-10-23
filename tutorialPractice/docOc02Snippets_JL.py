"""
A few snippets from a doc oc tentacle rig
Just some random code I wrote and edited as I made SDK's on the claws
and space switches
Not intended to be run all at once
-Jacob Lilly
"""

from maya import cmds

for i in cmds.ls(sl=1):
	cmds.parent(i, i + "_jnt")
	
nodes = ["BLf_clawBase_ctl", "ALf_clawBase_ctl"]
attrs = ['clawSpin', 'pivotUpDown', 'pivotSideSide', \
			'clawBaseAOpen', 'clawBaseBOpen', 'clawBaseCOpen', 'clawBaseDOpen', \
			'clawTipAOpen', 'clawTipBOpen', 'clawTipCOpen', 'clawTipDOpen']

for node in nodes:
	for attr in attrs:
		cmds.addAttr(node, ln=attr, at='double', dv=0)
		cmds.setAttr("{}.{}".format(node,attr), e=1, keyable=True)

i=7
for pair in sdk:
	for attr in attrs[7:]:
		driver = pair[0] + '.' + attr
		driven = '{}Lf_claw_01a{}_jnt'.format(pair[0][0], i)
		if 'Tip' in attr:
			driven = driven.replace('01a', '01b')
		driven = driven + '.rotateZ'
		i+=1
		
		cmds.setAttr(driver, -10)
		cmds.setAttr(driven, -60)
		cmds.setDrivenKeyframe(driven, currentDriver = driver)
		cmds.setAttr(driver, 10)
		cmds.setAttr(driven, 60)
		cmds.setDrivenKeyframe(driven, currentDriver = driver)
		
		cmds.setAttr(driver, 0)
		i+=1

for pair in sdk:
	ctl = pair[0]
	for attr in attrs:
		cmds.addAttr(ctl + '.' + attr, e=1, minValue = -10)
		cmds.addAttr(ctl + '.' + attr, e=1, maxValue = 10)
		for attr in attrs[:3]:
			cmds.addAttr(ctl + '.' + attr, e=1, hasMinValue = False)
			cmds.addAttr(ctl + '.' + attr, e=1, hasMaxValue = False)
			
# Space switching
from maya import cmds

#add attributes to a config node
attrs = ['space', 'tentacleARtSpace', 'tentacleBRtSpace', \
				'tentacleALfSpace', 'tentacleBLfSpace']
				
sel = cmds.ls(sl=1)[0]
for attr in attrs:
	fullAttr = sel + '.' + attr
	if cmds.addAttr(fullAttr, q=1, exists=True):
		cmds.deleteAttr(fullAttr)

for attr in attrs:
	cmds.addAttr(sel, ln = attr, min=0, max=1, dv=0, at='double')
	attr = sel + '.' + attr
	if 'space' in attr:
		cmds.setAttr(attr, e=1, channelBox=True)
	else:
		cmds.setAttr(attr, e=1, keyable=True)
		
#create nodes for space switching (just the left side for now)
root = 'root_jnt'
spaces = attrs[3:]
for space in spaces:
	cmds.select(cl=1)
	grp = cmds.group(n=space + '_grp', em=1)
	
	#hierarchy
	ikGrp = grp.replace('Space', 'Cluster')
	cmds.parent(grp, cmds.listRelatives(ikGrp, p=1))
	cmds.parent(ikGrp, grp)
	
	point = cmds.pointConstraint(root, grp)[0]
	orient = cmds.orientConstraint(root, grp)[0]

	cmds.connectAttr('config_ctl.' + space, point + '.' + root + 'W0')
	cmds.connectAttr('config_ctl.' + space, orient + '.' + root + 'W0')

