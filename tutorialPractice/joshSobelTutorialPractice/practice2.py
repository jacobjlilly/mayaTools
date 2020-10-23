import maya.cmds as cmds
import maya.mel as mel
import sys

# Select and delete all (just for testing)
cmds.select(all=1)
cmds.delete()

# Create groups
cmds.group(n='joints_GRP', em=1)
cmds.group(n='control_GRP', em=1)

# Clear Selection
cmds.select(cl=1)

# Create joints
cmds.joint(n='shoulder_JNT')
cmds.joint(n='elbow_JNT', p=[4,0,0])
cmds.joint(n='wrist_JNT', p=[8,0,0])
cmds.parent('shoulder_JNT', 'joints_GRP')

# Freeze joints' rotations
cmds.makeIdentity('joints_GRP', a=1, r=1)

# Create control hierarchy
cmds.circle(n='shoulder_CTL', nr=[1,0,0], ch=0)
cmds.circle(n='elbow_CTL',    nr=[1,0,0], ch=0)
cmds.circle(n='wrist_CTL',    nr=[1,0,0], ch=0)
ctls = ['shoulder_CTL', 'elbow_CTL', 'wrist_CTL']
cmds.parent('shoulder_CTL', 'control_GRP')
cmds.parent('elbow_CTL', 'shoulder_CTL')
cmds.parent('wrist_CTL', 'elbow_CTL')

# Position controls on joints
cmds.parentConstraint('elbow_JNT', 'elbow_CTL', n='temp')
cmds.delete('temp')
cmds.parentConstraint('wrist_JNT', 'wrist_CTL', n='temp')
cmds.delete('temp')

# Freeze controllers' transforms
cmds.makeIdentity('control_GRP', a=1, t=1, r=1, s=1)

# Create Constraints
cmds.orientConstraint('shoulder_CTL', 'shoulder_JNT')
cmds.orientConstraint('elbow_CTL', 'elbow_JNT')
cmds.orientConstraint('wrist_CTL', 'wrist_JNT')

# Tidy up
attrs = ['.tx', '.ty', '.tz', '.sx', '.sy', '.sz']
for ctl in ctls:
	for attr in attrs:
		cmds.setAttr(ctl + attr, lock=1, k=0, cb=0)

sys.stdout.write('created arm rig')