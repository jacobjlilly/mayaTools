# Shelf button to toggle Maya autosaving.

from maya.cmds import autoSave
import sys

if autoSave(q=1, en=1):
	autoSave(en=False)
	sys.stdout.write('Auto save disabled. Living dangerously ;)')
else:
	autoSave(en=True)
	sys.stdout.write('Auto save enabled. Laughs at Maya crashes.')
