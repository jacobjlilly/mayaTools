from maya import cmds, mel
import mgear.shifter as mg

"""
misc_mgearRebuildRig_JL.py
Rebuilds mgear Shifter rig. For use after adjusting Shifter's guides

23 Jul 20
Jacob Lilly
"""

# variables for potential future use
guide = 'guide'
geo = 'rain_fullBody_GEO'
rig = 'rig'
rootJnt = 'spine_C0_0_jnt' # shouldn't need to change this

# A checkbox for opening the bind skin options or using the settings from last time
bindOption = 0 

# Unbind Skin and delete rig
cmds.select(geo)
cmds.bindSkin(unbind=True)
cmds.delete(rig)

# Build new rig from mgear
cmds.select(guide)
mg.Rig.buildFromSelection(Rig=rig) 
"""
#BUG: needs a Rig object. For now, just manually use 
Build from Selection in Shifter Guide Manager."""

# Resize joints
cmds.select(rootJnt, hi=True)
for jnt in cmds.ls(sl=1):
	cmds.setAttr("{}.radius".format(jnt), .07)

# Bind Skin
cmds.select(rootJnt, geo)
if defaultBindOp:
	cmds.bindSkin()
else:
	mel.eval('SmoothBindSkinOptions;')
