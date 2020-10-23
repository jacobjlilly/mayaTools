from maya import cmds, mel

def docOcChallenge():
	
	#variables
	i=1
	nodeNum = 20
	spline = "extrudeCurveShape"
	nodeBase = "nodeLink"
	linkGrp = []

	#loopy time
	while i <= nodeNum:
		newNodeName = nodeBase + str(i)
		motionPath = "motionPath" + str(i)
		motionPathAttr = "motionPath" + str(i) + ".u"
		newNode = cmds.duplicate(nodeBase, n=newNodeName)

		cmds.select(newNode, spline)
		cmds.pathAnimation(fractionMode = False, follow = True,	\
			followAxis = 'z', upAxis = 'y',	useNormal = False, \
			inverseUp = False, bank = False, startTimeU = 1, endTimeU = 90)
		cmds.cutKey(motionPath, at="u")
		cmds.setAttr(motionPathAttr, float(i)/float(nodeNum))
		linkGrp.append(newNode)

		i+=1

	cmds.select(cl=1)
	for link in linkGrp:
		cmds.select(link, add=1)
	cmds.group(n='nodeLink_grp')

docOcChallenge()
