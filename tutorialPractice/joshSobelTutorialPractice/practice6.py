from maya import cmds, mel
import sys

def versionIncr():

	# Get info
	path = cmds.file(q=1, sn=1)
	fileName = path.split('/')[-1]
	verNum = fileName.replace('.ma', '').split('.')[-1]

	# Increment Version
	newNum = int(verNum) + 1
	length = len(str(newNum))
	newNum = '{}{}'.format(verNum[:-length], newNum)

	newName = fileName.replace(verNum, str(newNum))
	newPath = path.replace(fileName, newName)

	# Save as
	cmds.file(rn=newPath)
	cmds.file(save=1)

	sys.stdout.write('Saved {}'.format(newPath))

versionIncr()
