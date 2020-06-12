"""
	skinning_opacity_tool_JL

	I wanted a faster way to adjust opacity for painting skin weights,
	especially at low values, which I found slightly annoying in default Maya.

	Any button also opens the paint skin weights tool.

	Jacob Lilly 12 Jun 20
"""

from maya import cmds, mel
import sys

def sot_ui_JL(): 
	win = 'testUI'
	if cmds.window(win, exists=1):
		cmds.deleteUI(win)
	cmds.window(win, rtf=1, w=2, h=2, t='Skinning Opacity', s=1)
	cmds.columnLayout(adj=1)
	cmds.showWindow(win)

	cmds.rowColumnLayout(nr=10, adj=1)

	cmds.button(l='0.0097', c = 'import skinning_opacity_tool_JL as sot; reload(sot); sot.lowest()')
	cmds.button(l='1.0', c = 'import skinning_opacity_tool_JL as sot; reload(sot); sot.max()')

def lowest():
	mel.eval('ArtPaintSkinWeightsToolOptions')
	mel.eval('artAttrSkinPaintCtx -e -opacity 0.00970874 `currentCtx`;')

def max():
	mel.eval('ArtPaintSkinWeightsToolOptions')
	mel.eval('artAttrSkinPaintCtx -e -opacity 1.0 `currentCtx`;')

"""
	To do:
	*add more options as need
	*maybe add sliders with granular control (using floatSlider?)
		possible ex: from 0.0-0.1 with ten increments
		similar to Maya's normal ui, but with tighter control
		through multiple sliders
"""
