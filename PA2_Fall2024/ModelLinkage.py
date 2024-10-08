"""
Model our creature and wrap it in one class.
First version on 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

Modified by Daniel Scrivener 09/2023
"""

from Component import Component
from Point import Point
import ColorType as Ct
from Shapes import Cube, Cylinder, Cone, Sphere
import numpy as np

class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 
    #
    # In order to simplify the process of constructing your model, the rotational origin of each Shape has been offset by -1/2 * dz,
    # where dz is the total length of the shape along its z-axis. In other words, the rotational origin lies along the smallest 
    # local z-value rather than being at the translational origin, or the object's true center. 
    # 
    # This allows Shapes to rotate "at the joint" when chained together, much like segments of a limb. 
    #
    # In general, you should construct each component such that it is longest in its local z-direction: 
    # otherwise, rotations may not behave as expected.
    #
    # Please see Blackboard for an illustration of how this behavior works.

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent

        # Torso
        torso_length = 1.0
        torso_radius = 0.1
        torso = Cylinder(Point((0, 0, 0)), shaderProg, [torso_radius, torso_radius, torso_length], Ct.SOFTBLUE)

        # Head
        head_size = 0.2
        head = Cube(Point((0, 0, torso_length)), shaderProg, [head_size, head_size, head_size], Ct.YELLOW)

        # assume joints are cylinder
        joint_radius = 0.1
        # assume limbs are cylinder
        limb_length = 0.5
        limb_radius = 0.05
        # Rememebr: default plane has x being uAxis, y being vAxis, and z being wAxis
        # limbxy, where x represents the limb number, and y represents upper(1) or lower(0) part of the limb

        # side 1
        limb11 = Cylinder(Point((0, 0, torso_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE4)
        limb11.rotate(90, self.vAxis)
        joint1 = Sphere(Point((0 , 0, limb_length)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb12 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.RED)
        limb12.rotate(90, self.uAxis)

        limb21 = Cylinder(Point((0, 0, torso_length * 0.5)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE4)
        limb21.rotate(90, self.vAxis)
        joint2 = Sphere(Point((0 , 0, limb_length)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb22 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.RED)
        limb22.rotate(90, self.uAxis)
        
        limb31 = Cylinder(Point((0, 0, 0)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE4)
        limb31.rotate(90, self.vAxis)
        joint3 = Sphere(Point((0 , 0, limb_length)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb32 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.RED)
        limb32.rotate(90, self.uAxis)

        # side 2/opposing side of side 1

        limb41 = Cylinder(Point((0, 0, torso_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE4)
        limb41.rotate(-90, self.vAxis)
        joint4 = Sphere(Point((0 , 0, limb_length)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb42 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.RED)
        limb42.rotate(90, self.uAxis)
        
        limb51 = Cylinder(Point((0, 0, torso_length * 0.5)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE4)
        limb51.rotate(-90, self.vAxis)
        joint5 = Sphere(Point((0 , 0, limb_length)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb52 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.RED)
        limb52.rotate(90, self.uAxis)

        limb61 = Cylinder(Point((0, 0, 0)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE4)
        limb61.rotate(-90, self.vAxis)
        joint6 = Sphere(Point((0 , 0, limb_length)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb62 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.RED)
        limb62.rotate(90, self.uAxis)
        
        # attach head and torso
        self.addChild(torso)
        torso.addChild(head)

        # attaching limbs
        torso.addChild(limb11)
        limb11.addChild(joint1)
        joint1.addChild(limb12)

        torso.addChild(limb21)
        limb21.addChild(joint2)
        joint2.addChild(limb22)
        
        torso.addChild(limb31)
        limb31.addChild(joint3)
        joint3.addChild(limb32)

        torso.addChild(limb41)
        limb41.addChild(joint4)
        joint4.addChild(limb42)

        torso.addChild(limb51)
        limb51.addChild(joint5)
        joint5.addChild(limb52)

        torso.addChild(limb61)
        limb61.addChild(joint6)
        joint6.addChild(limb62)

        # Store components in a dictionary for easier access
        self.componentList = [torso, head, limb11, joint1, limb12, limb21, joint2, limb22, limb31, joint3, limb32, limb41, joint4, limb42, limb51, joint5, limb52, limb61, joint6, limb62]
        self.componentDict = {
            "torso": torso,
            "head": head,
            "limb11": limb11, "joint1": joint1, "limb12": limb12,
            "limb21": limb21, "joint2": joint2, "limb22": limb22,
            "limb31": limb31, "joint3": joint3, "limb32": limb32,
            "limb41": limb41, "joint4": joint4, "limb42": limb42,
            "limb51": limb51, "joint5": joint5, "limb52": limb52,
            "limb61": limb61, "joint6": joint6, "limb62": limb62
        }


        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
        # 

    """
    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent

        # Define the main body and color scheme
        body_length = 1.0
        body = Cube(Point((0, 0, 0)), shaderProg, [0.5, 0.5, body_length], Ct.SOFTBLUE)

        # Define the left and right limbs using Cubes and Cylinders
        limb_length = 0.4
        limb_radius = 0.1

        # Left Front Limb: 3 segments
        lf_link1 = Cylinder(Point((0.25, 0, 0.2)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE1)
        lf_link2 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE2)
        lf_link3 = Cube(Point((0, 0, limb_length)), shaderProg, [limb_radius * 2, limb_radius * 2, limb_length], Ct.DARKORANGE3)

        # Right Front Limb: Mirror of left front limb
        rf_link1 = Cylinder(Point((-0.25, 0, 0.2)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE1)
        rf_link2 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKORANGE2)
        rf_link3 = Cube(Point((0, 0, limb_length)), shaderProg, [limb_radius * 2, limb_radius * 2, limb_length], Ct.DARKORANGE3)

        # Left Back Limb: 2 segments
        lb_link1 = Cube(Point((0.25, 0, 0.8)), shaderProg, [limb_radius * 2, limb_radius * 2, limb_length], Ct.DARKGREEN)
        lb_link2 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKGREEN)

        # Right Back Limb: Mirror of left back limb
        rb_link1 = Cube(Point((-0.25, 0, 0.8)), shaderProg, [limb_radius * 2, limb_radius * 2, limb_length], Ct.DARKGREEN)
        rb_link2 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length], Ct.DARKGREEN)

        # Assemble the creature by connecting components
        self.addChild(body)

        # Left limbs
        body.addChild(lf_link1)
        lf_link1.addChild(lf_link2)
        lf_link2.addChild(lf_link3)

        body.addChild(lb_link1)
        lb_link1.addChild(lb_link2)

        # Right limbs
        body.addChild(rf_link1)
        rf_link1.addChild(rf_link2)
        rf_link2.addChild(rf_link3)

        body.addChild(rb_link1)
        rb_link1.addChild(rb_link2)

        # Store components in a dictionary for easier access
        self.componentList = [body, lf_link1, lf_link2, lf_link3, rf_link1, rf_link2, rf_link3, lb_link1, lb_link2, rb_link1, rb_link2]
        self.componentDict = {
            "body": body,
            "lf_link1": lf_link1, "lf_link2": lf_link2, "lf_link3": lf_link3,
            "rf_link1": rf_link1, "rf_link2": rf_link2, "rf_link3": rf_link3,
            "lb_link1": lb_link1, "lb_link2": lb_link2,
            "rb_link1": rb_link1, "rb_link2": rb_link2,
        }


       Stick figure thingy

        super().__init__(position, display_obj)
        self.contextParent = parent

        # Torso
        torso_length = 1.0
        torso_radius = 0.1
        torso = Cylinder(Point((0, 0, 0)), shaderProg, [torso_radius, torso_radius, torso_length], Ct.LIGHTBLUE)

        # Head
        head_size = 0.2
        head = Cube(Point((0, 0, torso_length)), shaderProg, [head_size, head_size, head_size], Ct.YELLOW)

        # Left Arm: Two segments connected by a joint
        upper_arm_length = 0.5
        lower_arm_length = 0.5
        arm_radius = 0.05

        left_upper_arm = Cylinder(Point((torso_radius, 0, torso_length * 0.75)), shaderProg, [arm_radius, arm_radius, upper_arm_length], Ct.RED)
        left_lower_arm = Cylinder(Point((0, 0, upper_arm_length)), shaderProg, [arm_radius, arm_radius, lower_arm_length], Ct.DARKRED)

        # Right Arm: Mirror of left arm
        right_upper_arm = Cylinder(Point((-torso_radius, 0, torso_length * 0.75)), shaderProg, [arm_radius, arm_radius, upper_arm_length], Ct.RED)
        right_lower_arm = Cylinder(Point((0, 0, upper_arm_length)), shaderProg, [arm_radius, arm_radius, lower_arm_length], Ct.DARKRED)

        # Left Leg: Two segments connected by a joint
        upper_leg_length = 0.6
        lower_leg_length = 0.6
        leg_radius = 0.07

        left_upper_leg = Cylinder(Point((torso_radius, 0, -torso_length * 0.5)), shaderProg, [leg_radius, leg_radius, upper_leg_length], Ct.DARKGREEN)
        left_lower_leg = Cylinder(Point((0, 0, upper_leg_length)), shaderProg, [leg_radius, leg_radius, lower_leg_length], Ct.GREEN)

        # Right Leg: Mirror of left leg
        right_upper_leg = Cylinder(Point((-torso_radius, 0, -torso_length * 0.5)), shaderProg, [leg_radius, leg_radius, upper_leg_length], Ct.DARKGREEN)
        right_lower_leg = Cylinder(Point((0, 0, upper_leg_length)), shaderProg, [leg_radius, leg_radius, lower_leg_length], Ct.GREEN)

        # Assemble the stick figure
        self.addChild(torso)
        torso.addChild(head)

        # Attach arms to torso
        torso.addChild(left_upper_arm)
        left_upper_arm.addChild(left_lower_arm)

        torso.addChild(right_upper_arm)
        right_upper_arm.addChild(right_lower_arm)

        # Attach legs to torso
        torso.addChild(left_upper_leg)
        left_upper_leg.addChild(left_lower_leg)

        torso.addChild(right_upper_leg)
        right_upper_leg.addChild(right_lower_leg)

        # Store components in a dictionary for easier access
        self.componentDict = {
            "torso": torso,
            "head": head,
            "left_upper_arm": left_upper_arm, "left_lower_arm": left_lower_arm,
            "right_upper_arm": right_upper_arm, "right_lower_arm": right_lower_arm,
            "left_upper_leg": left_upper_leg, "left_lower_leg": left_lower_leg,
            "right_upper_leg": right_upper_leg, "right_lower_leg": right_lower_leg,
        }

        Default thingy
                super().__init__(position, display_obj)
        self.contextParent = parent

        linkageLength = 0.5
        linkageRadius = 0.5

        link1 = Cube(Point((0, 0, 0)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE1)
        link2 = Cone(Point((0, 0, linkageLength)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE2)
        link3 = Sphere(Point((0, 0, linkageLength)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE3)
        link4 = Cube(Point((0, 0, linkageLength)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE4)
        # cone cube cylinder sphere

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.componentList = [link1, link2, link3, link4]
        self.componentDict = {
            "link1": link1,
            "link2": link2,
            "link3": link3,
            "link4": link4,
        }

        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
        # 
    """