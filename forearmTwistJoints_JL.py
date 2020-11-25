"""
Forearm twist joints

Using TD Matt's method 2 from td-matt.blogspot.com, this sets up twist 
joints for the forearm using an aim constraint.

Jacob Lilly
"""

from maya import cmds

# Given the original wrist joint, create twist skeleton
def createTwistJnts(wristJnt):
    
    cmds.select(cl=1)
    driverGroup = cmds.group(n="rt_arm1TwistRig_grp", em=1)
    
    # The driver1 joint will be in the center of the forearm
    driver1 = cmds.duplicate(
        wristJnt, rc=1, n = wristJnt.replace(
            "_jnt", "_twistDriver1_jnt"))[0]
    if (cmds.listRelatives(driver1, c=1) is not None):
        children = cmds.listRelatives(driver1, c=1)
        for child in children:
            if (cmds.objExists(child)):
                cmds.delete(child)
    
    # The driver2 joint will sit on top of the wrist (arm2)
    driver2 = cmds.duplicate(
        driver1, n = driver1.replace("1_jnt", "2_jnt"))[0]
    
    # Move the driver1 joint to the center of the forearm
    cmds.setAttr(
        driver1 + ".tx", cmds.getAttr(driver1 + ".tx") / 2)
    
    # The driver0 joint will sit on top of the elbow (arm1)
    driver0 = cmds.duplicate(
        driver1, n = driver1.replace("1_jnt", "0_jnt"))[0]
    cmds.setAttr(driver0 + ".tx", 0)
    
    cmds.parent(driver1, driver2, driver0)
    cmds.parent(driver0, driverGroup)
    
    return [driver0, driver1, driver2]


# Create aim constraint and locator for the constraint's up vector
def createAimConstraint(elbowJnt, wristJnt, drivers):
    
    # Create locator for our aim constraint's up vector
    cmds.select(cl=1)
    upVec = cmds.CreateLocator()
    upVec = cmds.rename(upVec, "rt_arm1TwistUpVec_loc")
    cmds.delete(cmds.parentConstraint(wristJnt, upVec, mo=0))
    cmds.setAttr(
        upVec + ".tz", cmds.getAttr(upVec + ".tz") - 0.25)
    cmds.select(upVec)
    cmds.scale(.2, .2, .2)
    cmds.parentConstraint(wristJnt, upVec, mo=1)
    
    # Create the aim constraint
    cmds.aimConstraint(
        elbowJnt, drivers[-1], \
        u = (0, 1, 0), wut = "object", wuo = upVec, mo=0)
    

# Set up connections from the wrist driver joint to the other twisty
# "driver" joints
def driveJoints(drivers):
    
    for i in range(len(drivers)):
        if (i != 0 and i != len(drivers)-1):
            # Create multiply divide nodes
            multDiv = cmds.shadingNode("multiplyDivide", au = 1, \
                n = drivers[i].replace("Bind", "").replace("jnt", "div"))
            cmds.setAttr(multDiv + ".operation", 2) # Set to divide
            cmds.setAttr(multDiv + ".input2X", 2) # Manually change these
            
            # Connect nodes
            cmds.connectAttr(drivers[-1] + ".rotate", multDiv + ".input1")
            cmds.connectAttr(multDiv + ".output", drivers[i] + ".rotate")


# Connect to skinning joints (may need to create skinning joint(s))
def connectSkinJoints(wristJnt, elbowJnt, drivers):
    
    # Duplicate the intermediate joint for skinning
    bindMidJnt = cmds.duplicate(
        drivers[1], n=drivers[1].replace("Driver1", "Bind1"))[0]
    grp = cmds.group(n=bindMidJnt.replace("jnt", "grp"))
    cmds.parent(grp, elbowJnt)
    
    cmds.connectAttr(drivers[1] + ".translate", grp + ".translate")
    cmds.connectAttr(drivers[1] + ".rotate", grp + ".rotate")
    cmds.connectAttr(drivers[1] + ".scale", grp + ".scale")

def run():
    
    elbow_jnt = "rt_arm1_jnt"
    wrist_jnt = "rt_arm2_jnt"
    jnt_num = 3 # Number of intermediate joints to create
    
    drivers = createTwistJnts(wrist_jnt)
    createAimConstraint(elbow_jnt, wrist_jnt, drivers)
    driveJoints(drivers)
    connectSkinJoints(wrist_jnt, elbow_jnt, drivers)
    print("Twist joints set up")

run()
