"""
Builds a standard triple-chain FK/IK arm setup
Also rigs fingers

Jacob Lilly
"""

from maya import cmds, mel

class ArmSetup:
    
    
    def __init__(self):
        
        self.side = "lf_"
        self.hi_bind = self.side + "arm0_jnt"
        self.lo_bind = self.side + "arm1_jnt"
        self.hand_bind = self.side + "arm2_jnt"
        self.bind_jnts = [self.hi_bind, self.lo_bind, self.hand_bind]
        self.settings_ctl = self.side + "armSettings_ctl"
        
        self.rig_grp = cmds.group(em=1, n=self.side + "armRig_grp")
        cmds.parentConstraint(
            self.side + "clavicleEnd_jnt", self.rig_grp, mo=0)
        
        self.duplicate_jnt_chains()
        self.ikfk_blend()
        self.connect_bind_jnts()
        self.setup_ik()
        self.connect_fk()
        self.rig_fingers(self.hand_bind)
        self.ctl_vis()

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
    
    def ikfk_blend(self):
        # Blend between fk and ik joint chains with a blendColors node
        cmds.addAttr(self.settings_ctl, ln="ikFkSwitch", k=1, min=0, max=1)          
        i=0
        while (i < len(self.driver_jnts)):
            blend = cmds.shadingNode(
                "blendColors", au=1, n = self.side+"arm"+str(i)+"IKFK_blend")
            cmds.connectAttr(self.fk_jnts[i] + ".rotate", blend + ".color1")
            cmds.connectAttr(self.ik_jnts[i] + ".rotate", blend + ".color2")
            cmds.connectAttr(
                blend + ".output", self.driver_jnts[i][0] + ".rotate")
            cmds.connectAttr(
                self.settings_ctl + ".ikFkSwitch", blend + ".blender")
            i+=1
    
    def setup_ik(self):
        # Create ik handle and constraints
        armIK_ctl = self.side + "armIK_ctl"
        arm_ik_hdl = cmds.ikHandle(
            sj = self.ik_jnts[0], ee = self.ik_jnts[2], sol = "ikRPsolver", \
            n = self.ik_jnts[0].replace("jnt", "hdl"))
        cmds.poleVectorConstraint(self.side + "armPV_ctl", arm_ik_hdl[0])
        cmds.parentConstraint(armIK_ctl, arm_ik_hdl[0], mo=1)
        # May need to change parent constraint on group
        cmds.parent(arm_ik_hdl[0], self.rig_grp)
        cmds.orientConstraint(armIK_ctl, self.ik_jnts[2], mo=0)
    
    def connect_fk(self):
        # Drive the fk joint chain with the fk controls through direct 
        # connections
        i=0
        fk_ctls = [ self.side + "arm0_ctl",
                    self.side + "arm1_ctl",
                    self.side + "arm2_ctl"]
        while i < len(self.fk_jnts):
            cmds.connectAttr(
                fk_ctls[i] + ".rotate", self.fk_jnts[i] + ".rotate")
            i+=1
        self.wrist_fix(fk_ctls[2])
        
    def wrist_fix(self, hand_fk_ctl):
        # Fix fingers always following the fk control due to ctl hierarchy
        fng_grp = cmds.duplicate(
            hand_fk_ctl, po=1, to=1, n = self.side + "fng_grp")
        cmds.parent(fng_grp, hand_fk_ctl)
        for child in cmds.listRelatives(hand_fk_ctl, c=1):
            if ("fng_grp" not in child and "Shape" not in child):
                cmds.parent(child, fng_grp)
        cmds.parentConstraint(self.hand_bind, fng_grp, mo=0)

    def ctl_vis(self):
        # Set visibility of fk and ik controls 
        # (so that fk controls are invisible in ik mode and vice versa).
        # All ctls should be visible when 0 < ikfk switch > 1,
        # so use set driven keys.
        switch = self.settings_ctl + ".ikFkSwitch"
        
        # Fk
        fk_ctls = []
        for i in range(3):
            fk_ctls.append(self.side + "arm%s_ctl" % i)
        for ctl in fk_ctls:
            shape_vis = cmds.listRelatives(ctl, c=1, s=1)[0] + ".visibility"
            cmds.setAttr(switch, 0)
            cmds.setDrivenKeyframe(
                shape_vis, cd = switch, v=0, itt="stepNext", ott="stepNext")
            cmds.setAttr(switch, 1)
            cmds.setDrivenKeyframe(
                shape_vis, cd = switch, v=1, itt="stepNext", ott="stepNext")
        
        # Ik
        for ctl in [self.side + "armPV_ctl", self.side + "armIK_ctl"]:
            shape_vis = cmds.listRelatives(ctl, c=1, s=1)[0] + ".visibility"
            cmds.setAttr(switch, 0)
            cmds.setDrivenKeyframe(
                shape_vis, cd = switch, v=1, itt="stepNext", ott="step")
            cmds.setAttr(switch, 1)
            cmds.setDrivenKeyframe(
                shape_vis, cd = switch, v=0, itt="stepNext", ott="step")
            
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
                cmds.orientConstraint(child.replace("jnt","ctl"), child, mo=0)
                if (cmds.listRelatives(child, c=1)):
                    self.rig_fingers(child)

mel.eval('file -f -options "v=0;"  -ignoreVersion  -typ "mayaAscii" -o \
    "C:/Users/yacob/Documents/maya/projects/riggingPractice/rain/rain_JL.ma"; \
    addRecentFile("C:/Users/yacob/Documents/maya/projects/riggingPractice/rain/rain_JL.ma", \
    "mayaAscii");')
arm = ArmSetup()
