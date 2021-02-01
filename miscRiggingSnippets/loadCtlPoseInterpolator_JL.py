"""
Automates loading in the controller for a joint's pose interpolator
in the pose editor.
"""

from maya import cmds

side = "lf_"
node = side + "arm0"
ctl = node + "_ctl"
jnt = node + "_jnt"
poseInterp = jnt + "_poseInterpolatorShape.driver[0].driverController["
axes = ["X", "Y", "Z"]
i = 0

while (i < len(axes)):
	cmds.connectAttr(ctl + ".rotate" + axes[i], poseInterp + str(i) + "]")
	i+=1