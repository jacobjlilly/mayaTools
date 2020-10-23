from maya import cmds, mel
import sys

def ui():
	win = 'testUI'
	if cmds.window(win, exists=1):
		cmds.deleteUI(win)
	cmds.window(win, rtf=1, w=2, h=2, t='Connect Attributes', s=1)
	cmds.columnLayout(adj=1)
	cmds.showWindow(win)

	cmds.rowColumnLayout(nr=2, adj=1)

	cmds.textField('driver_tf', tx='load one driver', w=200)
	cmds.textField('drivens_tf', tx='load drivens', w=200)
	cmds.button(l='Driver', w=100, c='import testUI as jl; reload(jl); jl.loadDriver()')
	cmds.button(l='Driven', w=100, c='import testUI as jl; reload(jl); jl.loadDrivens()')
	cmds.setParent('..')
	cmds.button(l='Run', w=200, c='import testUI as jl; reload(jl); jl.run()')

def loadDriver():
	obj = cmds.ls(sl=1)
	if len(obj) != 1:
		cmds.warning('Select exactly one object please.')
	else:
		attr = cmds.channelBox('mainChannelBox', q=1, sma=1)
		if not attr or len(attr) != 1:
			cmds.warning('Select exactly one attribute please.')
		else:
			# String manipulation
			driver = obj + attr
			driver = str(driver).replace("[u'", "")
			driver = driver.replace("', u'", ".")
			driver = driver.replace("']", "")

			cmds.textField('driver_tf', e=1, tx=driver)

def loadDrivens():
	objs = cmds.ls(sl=1)
	if len(objs) < 1:
		cmds.warning('Select at least one object please.')
	else:
		attrs = cmds.channelBox('mainChannelBox', q=1, sma=1)
		if not attrs:
			cmds.warning('Select at least one attribute please.')
		else:
			drivens = []
			for attr in attrs:
				for obj in objs:
					driven = '{}.{}'.format(obj,attr)
					print driven
					drivens.append(driven)

			# String manipulation
			drivens = str(drivens).replace ('[','')
			drivens = str(drivens).replace (']','')
			drivens = str(drivens).replace ("'","")

			cmds.textField('drivens_tf', e=1, tx=drivens)

def run():
	driver = cmds.textField('driver_tf', q=1, tx=1)
	drivens = cmds.textField('drivens_tf', q=1, tx=1)
	drivens = drivens.split(',')
	# Connect attrs
	for d in drivens:
		if not cmds.isConnected(driver, d):
			cmds.connectAttr(driver, d)
	sys.stdout.write('connected!')
