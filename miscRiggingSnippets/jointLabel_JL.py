# Auto joint labelling
# Just assigns sides (lf, rt, cn) for now

from maya.cmds import *

for jnt in ls(type = 'joint'):
	if "cn_" in jnt:
		setAttr(jnt + ".side", 0)
	elif "lf_" in jnt:
		setAttr(jnt + ".side", 1)
	elif "rt_" in jnt:
		setAttr(jnt + ".side", 2)
