from maya.cmds import *
""" 
Creates twisty joints and IK spline between two selected joints
ex: select shoulder then elbow and specify 3 to create
3 intermediate joints
"""

n = 3 #user picks number of twisty joints to add
start, end = ls(sl=1)

twists = []
select(start)
for i in range(n+2):
    jnt = joint(rad = .01)
    jnt = rename(jnt, start.replace('_jnt', 'Twist' + str(i) + '_jnt'))
    twists.append(jnt)
    if i == 0:
        startTwist = jnt
    if i == n:
        delete(parentConstraint(end, jnt))
        endTwist = jnt

# evenly space out twisties
tx = getAttr(end + '.tx') / (n+1)
for twist in twists[1:]:
    setAttr(twist + '.tx', tx)

# make IK spline and connect twist
hdl, eff, crv = ikHandle(sj=startTwist, ee=endTwist, sol = 'ikSplineSolver')
hdl = rename(hdl, start.replace('_jnt', 'Twist_hdl'))
eff = rename(eff, start.replace('_jnt', 'Twist_eff'))
crv = rename(crv, start.replace('_jnt', 'Twist_crv'))
hide(hdl, eff, crv)
mult = shadingNode('multiplyDivide', asUtility=1)
connectAttr(end + '.rx', mult + '.input1X')
connectAttr(mult + '.outputX', hdl + '.twist')
