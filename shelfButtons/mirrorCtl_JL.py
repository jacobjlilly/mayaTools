from maya import cmds

for obj in cmds.ls(sl=1):
	dupl = cmds.duplicate(obj)
	grp = cmds.group(em=1, n = '{}_grp'.format(obj))
	cmds.parent(dupl, grp)
	cmds.setAttr('{}.scaleX'.format(grp), -1)
	if obj[0:3] == 'lf_':
		cmds.rename(grp, grp.replace('lf_', 'rt_'))
		cmds.rename(dupl, dupl[0].replace('lf_', 'rt_'))
	elif obj[0:3]=='rt_':
		cmds.rename(grp, grp.replace('rt_', 'lf_'))
		cmds.rename(dupl, dupl[0].replace('rt_', 'lf_'))
