import maya.cmds as cmds
import maya.mel as mel
import sys

cmds.select(all=1)
cmds.delete()

# Create proxy locators
amount = 5 # How many locators to create
locs = []
count=1
for i in range(amount):
	loc = locs.append(cmds.spaceLocator(n='locator{}_PRX'.format(count), p=[0,i*2.5,0]))
	# p arg above doesn't center pivot)
	mel.eval('CenterPivot;')
	count+=1
