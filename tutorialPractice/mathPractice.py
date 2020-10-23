from maya import cmds
import maya.api.openMaya as om
import math

jnt1 = cmds.joint()
cmds.select(cl=1)
jnt2 = cmds.joint()
cmds.xform(jnt2, t=0,0,10)
cmds.xform(jnt1, t=10,0,0)
cmds.select(cl=1)
root = cmds.joint()
cmds.parent([jnt1, jnt2], root)

v1 = om.MVector(cmds.xform(jnt1, t=1, q=1)).normal()
v1 = om.MVector(cmds.xform(jnt2, t=1, q=1)).normal()

dot = v1*v2
print dot
print math.acos(dot)
print.acos(dot) * 180 / math.pi