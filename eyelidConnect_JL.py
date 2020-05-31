from maya import cmds, mel

driver = cmds.ls(sl=1)[0]
driven = cmds.ls(sl=1)[1]

cmds.connectAttr(driver + '.rotateY', driven + '.rotateY')
cmds.connectAttr(driver + '.rotateZ', driven + '.rotateZ')

cmds.connectAttr(driver + '.scaleX', driven + '.scaleX')
cmds.connectAttr(driver + '.scaleY', driven + '.scaleY')
cmds.connectAttr(driver + '.scaleZ', driven + '.scaleZ')

multDiv = cmds.shadingNode('multiplyDivide', au=1)
if cmds.isConnected(driver + '.rotateX', driven + '.rotateX'):
	print("they're connected")
	cmds.disconnectAttr(driver + '.rotateX', driven + '.rotateX')
cmds.connectAttr(driver + '.rotateX', multDiv + '.input1X')
cmds.connectAttr(multDiv + '.outputX', driven + '.rotateX')
cmds.setAttr(multDiv + '.input2X', 3)

cmds.rename(multDiv, driver.replace(driver[-3:], 'multDiv'))