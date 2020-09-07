from maya.cmds import *
""" 
Creates twisty joints and IK spline between two selected joints
ex: select shoulder then elbow and specify 3 to create
3 intermediate joints
"""

twistNum = 3 #user picks number of twisty joints to add
n = twistNum + 2
start, end = ls(sl=1)

twists = []
select(start)
while n > 0:
    jnt = joint(n=start) #might have to name better
    if n == twistNum + 2:
        startTwist = jnt
    twists.append(jnt)
    if n == 1:
        delete(parentConstraint(end, jnt))
        endTwist = jnt
    n -= 1

# evenly space out twisties
tx = getAttr(endTwist + '.tx') / (twistNum + 2)
for twist in twists[1:]:
    setAttr(twist + '.tx', tx)

# make IK spline and connect twist
hdl = ikHandle(sj=startTwist, ee=endTwist, sol = 'ikSplineSolver')[0]
mult = shadingNode('multiplyDivide', asUtility=1)
connectAttr(end + '.rx', mult + '.input1X')
connectAttr(mult + '.outputX', hdl + '.twist')
