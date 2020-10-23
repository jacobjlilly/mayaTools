from maya import cmds

# so far, this creates joints, ik splines, and basic controls for the splines

def createTentJnt(obj):
	jnt = cmds.joint(n = '{}_jnt'.format(obj), rad = 0.1)
	cnst = cmds.parentConstraint(obj, jnt)
	cmds.delete(cnst)
	return jnt

def createTentIk(tentGrpName, tentGrp, parJnt):
	ik = cmds.ikHandle( \
		n = tentGrpName.replace('Geo', '_ikHdl'), \
		sj = tentGrp[1] + '_jnt', ee = parJnt, \
		sol = 'ikSplineSolver', \
		shf=True, sticky='sticky', ccv=True, \
		roc=True, tws='easeInOut', \
		pcv=False, ns=3)
	ikGrp = cmds.group(n= ik[0] + '_grp')
	crv = cmds.rename(ik[2], str(ik[0]).replace('ikHdl', 'ikCrv'))
	
	#cluster time
	crvCVs = cmds.ls('{}.cv[:]'.format(crv), fl=True)
	clusterGrps = []
	i=0
	for cv in crvCVs:
		clstr = cmds.cluster(cv)
		#create controllers
		ctl = cmds.circle(n=tentGrpName.replace('Geo', '_ikCtl{}'.format(i)), nr = [1,0,0])
		grp = cmds.group(n=ctl[0] + '_grp')
		cnst = cmds.parentConstraint(clstr, grp)
		cmds.delete(cnst)
		cmds.parent(clstr, ctl)
		clusterGrps.append(grp)
		i+=1
	clusterGrp = cmds.group(clusterGrps, n=tentGrpName.replace('Geo', 'Cluster_grp'))
	cmds.group(clusterGrp, ikGrp, crv, n=tentGrpName.replace('Geo', '_ik_grp'))

cmds.select(cl=1)
root = cmds.joint(n = 'root_jnt')
tentGrps = ['tentacleALfGeo', 'tentacleBLfGeo']

for tentGrp in tentGrps:
	tentGrpName = str(tentGrp)
	cmds.select(cl=1)
	tentGrp = cmds.listRelatives(tentGrp, c=1)
	parJnt = createTentJnt(tentGrp[0])
	cmds.parent(parJnt, root)
	
	for tent in tentGrp[1:]:
		cmds.select(cl=1)
		if 'pCylinder' in tent:
			break

		jnt = createTentJnt(tent)
		cmds.parent(jnt, parJnt)
		cmds.parent(tent, jnt) # <--parent geo to jnts

		if 'Tent' in tent:
			parJnt = jnt
		elif 'clawBase' in tent:
			createTentIk(tentGrpName, tentGrp, parJnt)
			parJnt = jnt
			continue
