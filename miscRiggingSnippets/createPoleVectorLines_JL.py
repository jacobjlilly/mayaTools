from maya import cmds
import sys

"""
Creates a visual line connecting a pole vector controller
to a joint (ie elbow, knee)

Will probably need to make another multDiv node for global scale
Also should make curve invisible in FK mode
Should also manually adjust 2X value on multDiv nodes

3 Feb 21
Jacob Lilly
"""

def createPoleVectorLines_JL():

	# Select controller and joint. Order doesn't matter
	joint = cmds.ls(sl=1, typ='joint')
	ctl = cmds.ls(sl=1, typ='transform')
	for i in ctl:
		if (cmds.nodeType(i) == 'joint'):
			ctl.remove(i)

	# Create distance measurement tool between joint and controller
	# Create, name, and position locators under joint and controller
	dist = cmds.distanceDimension(startPoint = [0,0,0], endPoint = [1,0,0])
	ctl_loc, joint_loc = cmds.listConnections(dist)
	ctl_loc = cmds.rename(ctl_loc, ctl[0].replace('_ctl', 'Ctl_loc'))
	joint_loc = cmds.rename(joint_loc, ctl[0].replace('_ctl', 'Jnt_loc'))
	cmds.delete(cmds.pointConstraint(ctl, ctl_loc))
	cmds.delete(cmds.pointConstraint(joint, joint_loc))
	cmds.makeIdentity(joint_loc, a=1, t=1, r=1, s=1)
	cmds.makeIdentity(ctl_loc, a=1, t=1, r=1, s=1)
	cmds.parent(joint_loc, joint)
	cmds.parent(ctl_loc, ctl)

	# Create curve
	ctl_xform = cmds.xform(ctl_loc, q=1, ws=1, rp=1)
	joint_xform = cmds.xform(joint_loc, q=1, ws=1, rp=1)
	curve = cmds.curve(d=1, p=[joint_xform, ctl_xform], k=[0,1], ws=1)
	curve = cmds.rename(curve, ctl[0].replace('_ctl', '_crv'))

	# Move curve's pivot to joint
	cmds.move(
		joint_xform[0], joint_xform[1], joint_xform[2],
		curve + '.scalePivot', curve + '.rotatePivot', absolute=True)

	# Get curve to move appropriately by 
	# parent constraining it to the joint locator and 
	# aim constraining it to the control locator
	cmds.parentConstraint(joint_loc, curve, mo=False)
	cmds.aimConstraint(ctl_loc, joint_loc, mo=True)

	# Scale the curve
	mult = cmds.shadingNode('multiplyDivide', asUtility=1,
		n=ctl[0].replace('_ctl', '_mult'))
	cmds.connectAttr(dist + '.distance', mult + '.input1X')
	cmds.connectAttr(mult + '.outputX', curve + '.scaleZ')
	cmds.setAttr(mult + '.input2X', 0.75) # May need manual adjustment

	# Make curve unselectable
	cmds.setAttr(curve + '.template', 1)

	# Hide and group stuff
	for i in [dist, ctl_loc, joint_loc]:
		cmds.hide(i)
	grp = cmds.group(em=1, n=ctl[0].replace('_ctl', 'Crv_grp'))
	cmds.parent(dist, curve, grp)

createPoleVectorLines_JL()
