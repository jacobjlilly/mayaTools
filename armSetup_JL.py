"""
Builds a standard triple-chain FK/IK arm setup
Also rigs fingers

Jacob Lilly
"""

from maya import cmds, mel

class ArmSetup:
    
    
    def __init__(self):
        
        self.side = "rt_"
        self.hi_bind = self.side + "arm0_jnt"
        self.lo_bind = self.side + "arm1_jnt"
        self.hand_bind = self.side + "arm2_jnt"
        self.bind_jnts = [self.hi_bind, self.lo_bind, self.hand_bind]
        self.settings_ctl = self.side + "armSettings_ctl"
        
        self.rig_grp = cmds.group(em=1, n=self.side + "armRig_grp")
        cmds.parentConstraint(
            self.side + "clavicleEnd_jnt", self.rig_grp, mo=0)
        
        self.duplicate_jnt_chains()
        self.fkik_blend()
        self.connect_bind_jnts()
        self.setup_ik()
        self.connect_fk()
        self.rig_fingers(self.hand_bind)

    def duplicate_jnt_chains(self):
        
        # Duplicates bind joints to make a triple joint chain that 
        # blends between fk and ik
        
        # Duplicate bind joints to make driver joints
        hi_driver = cmds.duplicate(
            self.hi_bind, parentOnly=True, \
            n = self.hi_bind.replace("jnt", "driver_jnt"))
        lo_driver = cmds.duplicate(
            self.lo_bind, parentOnly=True, \
            n = self.lo_bind.replace("jnt", "driver_jnt"))
        hand_driver = cmds.duplicate(
            self.hand_bind, parentOnly=True, \
            n = self.hand_bind.replace("jnt", "driver_jnt"))
        self.driver_jnts = [hi_driver, lo_driver, hand_driver]
        
        # Hierarchy
        cmds.parent(hi_driver, self.rig_grp)
        cmds.parent(lo_driver, hi_driver)
        cmds.parent(hand_driver, lo_driver)
        
        # Duplicate to make FK and IK chains
        self.ik_jnts = cmds.duplicate(hi_driver, rc=1)
        self.fk_jnts = cmds.duplicate(hi_driver, rc=1)
        i=0
        while i < len(self.ik_jnts):
            jnt = self.ik_jnts[i]
            self.ik_jnts[i] = cmds.rename(
                jnt, jnt.replace("driver", "ik").replace("jnt1", "jnt"))
            jnt = self.fk_jnts[i]
            self.fk_jnts[i] = cmds.rename(
                jnt, jnt.replace("driver", "fk").replace("jnt2", "jnt"))
            i+=1
    
    def fkik_blend(self):
        # Blend between fk and ik joint chains with a blendColors node
        cmds.addAttr(self.settings_ctl, ln="fkIkSwitch", k=1, min=0, max=1)          
        i=0
        while (i < len(self.driver_jnts)):
            blend = cmds.shadingNode(
                "blendColors", au=1, n = self.side+"arm"+str(i)+"FKIK_blend")
            cmds.connectAttr(self.fk_jnts[i] + ".rotate", blend + ".color1")
            cmds.connectAttr(self.ik_jnts[i] + ".rotate", blend + ".color2")
            cmds.connectAttr(
                blend + ".output", self.driver_jnts[i][0] + ".rotate")
            cmds.connectAttr(
                self.settings_ctl + ".fkIkSwitch", blend + ".blender")
            i+=1
    
    def setup_ik(self):
        arm_ik_hdl = cmds.ikHandle(
            sj = self.ik_jnts[0], ee = self.ik_jnts[2], sol = "ikRPsolver", \
            n = self.ik_jnts[0].replace("jnt", "hdl"))
        cmds.poleVectorConstraint(self.side + "armPV_ctl", arm_ik_hdl[0])
        cmds.parentConstraint(self.side + "armIK_ctl", arm_ik_hdl[0], mo=1)
        # May need to change parent constraint on group
        cmds.parent(arm_ik_hdl[0], self.rig_grp)
    
    def connect_fk(self):
        i=0
        fk_ctls = [ self.side + "arm0_ctl",
                    self.side + "arm1_ctl",
                    self.side + "arm2_ctl"]
        while i < len(self.fk_jnts):
            cmds.connectAttr(
                fk_ctls[i] + ".rotate", self.fk_jnts[i] + ".rotate")
            i+=1

    def connect_bind_jnts(self):
        # Drive the bind joints with the driver rig jnts through
        # offset parent constraints
        i=0
        while (i < len(self.bind_jnts)):
            grp = cmds.group(
                self.bind_jnts[i], n=self.bind_jnts[i].replace("jnt", "grp"))
            cmds.parentConstraint(self.driver_jnts[i], grp, mo=1)
            i+=1
    
    def rig_fingers(self, jnt):
        # Create orient constraints from finger controls to finger bind joints
        for child in cmds.listRelatives(jnt, c=1):
            if ("End" not in child and "orient" not in child):
                cmds.orientConstraint(child.replace("jnt", "ctl"), child, mo=0)
                if (cmds.listRelatives(child, c=1)):
                    self.rig_fingers(child)

arm = ArmSetup()
