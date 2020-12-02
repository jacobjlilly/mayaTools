"""
Sets up a reverse foot rig with custom attributes

Jacob Lilly
"""

from maya import cmds
import sys


class ReverseFoot:
    
    
    def __init__(self):
        self.side = "rt_"
        self.up_leg_jnt = self.side + "leg0_driver_jnt"
        self.lo_leg_jnt = self.side + "leg1_driver_jnt"
        self.foot_jnt = self.side + "leg2_driver_jnt"
        self.toe_jnt = self.side + "toe_driver_jnt"
        self.toe_end_jnt = self.side + "toeEnd_driver_jnt"
        
        self.foot_ctl = self.side + "legIK_ctl"
        
        self.create_iks()
        self.create_grps()
        self.hierarchy()
        self.createAttrs()

    def create_iks(self):
        # Create RP solver IK hdl from upLeg to foot
        self.leg_ik = cmds.ikHandle(
            sj = self.up_leg_jnt, ee = self.foot_jnt, sol = "ikRPsolver", \
            n = self.up_leg_jnt.replace("0_driver_jnt", "IK_hdl"))[0]
        # Create SC solver IK from foot to toe
        self.foot_ik = cmds.ikHandle(
            sj = self.foot_jnt, ee = self.toe_jnt, sol = "ikSCsolver", \
            n = self.foot_jnt.replace("leg2_driver_jnt", "footIK_hdl"))[0]
        # Create SC solver IK from toe to toeEnd
        self.toe_ik = cmds.ikHandle(
            sj = self.toe_jnt, ee = self.toe_end_jnt, sol = "ikSCsolver", \
            n = self.toe_jnt.replace("_driver_jnt", "IK_hdl"))[0]
           
    def create_grps(self):
        
        # Create and position groups
        
        self.heel_lift_grp = cmds.group(
            em=True, n = self.side + "heelLift_grp")
        cmds.delete(cmds.parentConstraint(
            self.toe_jnt, self.heel_lift_grp, mo=False))
        cmds.makeIdentity(self.heel_lift_grp, a=True)
        
        self.toe_curl_grp = cmds.group(em=True, n = self.side + "toeCurl_grp")
        cmds.delete(cmds.parentConstraint(
            self.toe_jnt, self.toe_curl_grp, mo=False))
        cmds.makeIdentity(self.toe_curl_grp, a=True)

        self.toe_tip_grp = cmds.group(em=True, n = self.side + "toeTip_grp")
        cmds.delete(cmds.parentConstraint(
                self.toe_end_jnt, self.toe_tip_grp, mo=False))
        cmds.makeIdentity(self.toe_tip_grp, a=True)
        
        self.foot_twist_grp = cmds.group(
            em=True, n = self.side + "foot_twist_grp")
        cmds.delete(cmds.parentConstraint(
                self.toe_jnt, self.foot_twist_grp, mo=False))
        cmds.makeIdentity(self.foot_twist_grp, a=True)

        # Manually move pivot of heel_roll_grp to back of heel geometry later
        self.heel_roll_grp = cmds.group(
            em=True, n = self.side + "heelRoll_grp")
        cmds.delete(cmds.pointConstraint(
            self.foot_jnt, self.heel_roll_grp, mo=False))
        cmds.setAttr(self.heel_roll_grp + ".translateY", 0)
        sys.stdout.write("Move heelRoll_grp to back of heel geometry")
        
    def hierarchy(self):
        cmds.parent(self.leg_ik, self.heel_lift_grp)
        cmds.parent(self.toe_ik, self.toe_curl_grp)
        cmds.parent(self.heel_lift_grp, self.toe_curl_grp, self.foot_ik, \
            self.toe_tip_grp)
        cmds.parent(self.toe_tip_grp, self.foot_twist_grp)
        cmds.parent(self.foot_twist_grp, self.heel_roll_grp)
        
    def createAttrs(self):
        
        # Create and connect custom attributes on the foot controller
        cmds.addAttr(self.foot_ctl, ln = "kneeTwist", at = "float", k=1)
        cmds.addAttr(self.foot_ctl, ln = "heelLift", at = "float", k=1)
        cmds.addAttr(self.foot_ctl, ln = "toeCurl", at = "float", k=1)
        cmds.addAttr(self.foot_ctl, ln = "toeTip", at = "float", k=1)
        cmds.addAttr(self.foot_ctl, ln = "ballTwist", at = "float", k=1)
        cmds.addAttr(self.foot_ctl, ln = "heelRoll", at = "float", k=1)
        cmds.addAttr(self.foot_ctl, ln = "toeTwist", at = "float", k=1)
        
        cmds.connectAttr(
            self.foot_ctl + ".kneeTwist", self.leg_ik + ".twist")
        cmds.connectAttr(
            self.foot_ctl + ".heelLift", self.heel_lift_grp + ".rotateX")        
        cmds.connectAttr(
            self.foot_ctl + ".toeCurl", self.toe_curl_grp + ".rotateX")        
        cmds.connectAttr(
            self.foot_ctl + ".toeTip", self.toe_tip_grp + ".rotateX")        
        cmds.connectAttr(
            self.foot_ctl + ".ballTwist", self.foot_twist_grp + ".rotateY")        
        cmds.connectAttr(
            self.foot_ctl + ".heelRoll", self.heel_roll_grp + ".rotateX")
        cmds.connectAttr(
            self.foot_ctl + ".toeTwist", self.toe_tip_grp + ".rotateY")
    
rf = ReverseFoot()
