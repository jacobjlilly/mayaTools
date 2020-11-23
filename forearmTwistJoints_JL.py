"""
Forearm twist joints

Using TD Matt's method 2 from td-matt.blogspot.com, this sets up twist 
joints for the forearm using an aim constraint.

Jacob Lilly 11.22.2020
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
        elbowJnt, drivers[2], \
        u = (0, 1, 0), wut = "object", wuo = upVec, mo=0)
    

# Drive joints
def driveJoints(drivers):

    # Create multiply divide node
    twistDiv = cmds.shadingNode(
        "multiplyDivide", au=1, n = "rt_arm1Twist_div")
    cmds.setAttr(twistDiv + ".operation", 2)
    cmds.setAttr(twistDiv + ".input2X", 2)

    # Connections
    cmds.connectAttr(drivers[2] + ".rotate", twistDiv + ".input1")
    cmds.connectAttr(twistDiv + ".output", drivers[1] + ".rotate")


# Connect to skinning joints (may need to create skinning joint(s))


def run():
    
    elbow_jnt = "rt_arm1_jnt"
    wrist_jnt = "rt_arm2_jnt"
    
    drivers = createTwistJnts(wrist_jnt)
    createAimConstraint(elbow_jnt, wrist_jnt, drivers)
    driveJoints(drivers)
    print("Twist joints set up")

run()
