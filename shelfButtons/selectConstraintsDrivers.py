from maya import cmds
import re
import sys

def selectConstraintsDrivers():
    # If the selected object(s) is constrained,
    # select its driver object(s)

    sel = cmds.ls(sl=1)
    consts = cmds.listRelatives(sel, c=1, typ='constraint')

    if (consts == None):
        sys.stdout.write("Found 0 constraints.")
        return

    attrs = []
    for const in consts:
        attrs.append(cmds.listAttr(const, k=1))
    attrs = str(attrs)

    drivers = []
    for driver in re.findall('\w+W[0-9]+', attrs):
        drivers.append(driver.split('W')[0])

    cmds.select(drivers)

    # Print the driver(s) we found
    if (len(drivers) == 1):
        sys.stdout.write("Found 1 driver: " + str(drivers[0]))
        return

    # String manipulation
    num = str(len(drivers))
    drivers = str(drivers).replace('[','').replace(']', '').replace("'", "")
    sys.stdout.write("Found " + num + " drivers: " + drivers)

selectConstraintsDrivers()
