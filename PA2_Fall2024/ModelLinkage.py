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

        # assume joints are sphere
        joint_radius = 0.1
        jointLength = 0.25
        # Torso
        torso_length = 0.25
        torso_radius = 0.1
        torso1 = Cylinder(Point((0, 0, 0)), shaderProg, [torso_radius * 3, torso_radius, jointLength], Ct.SOFTBLUE)
        torJoint1 = Sphere(Point((0, 0, jointLength)), shaderProg, [torso_radius, torso_radius * 0.5, jointLength/2], Ct.YELLOW)
        torso2 = Cylinder(Point((0, 0, jointLength)), shaderProg, [torso_radius * 3 * 0.9, torso_radius * 0.9, jointLength], Ct.CYAN)
        torJoint2 = Sphere(Point((0, 0, jointLength)), shaderProg, [torso_radius * 3 * 0.8, torso_radius * 0.25, jointLength/2], Ct.YELLOW)
        torso3 = Cylinder(Point((0, 0, jointLength)), shaderProg, [torso_radius * 3 * 0.8, torso_radius * 0.8, jointLength], Ct.BLUE)

        # Head
        head_size = 0.2
        head = Sphere(Point((0, 0, torso_length)), shaderProg, [torso_radius * 3, torso_radius, head_size], Ct.YELLOW)
        # mouth
        mouth_size = head_size/5
        mouth1 = Cone(Point((torso_radius, 0, head_size)), shaderProg, [mouth_size, mouth_size, mouth_size], Ct.GRAY)
        mouth2 = Cone(Point((-torso_radius, 0, head_size)), shaderProg, [mouth_size, mouth_size, mouth_size], Ct.GRAY)

        # eyes
        eye_size = 0.02
        eye1 = Cube(Point((eye_size*2, torso_radius * 0.75, head_size * 0.5)), shaderProg, [eye_size, eye_size, eye_size], Ct.GRAY)
        eye2 = Cube(Point((eye_size*-2, torso_radius * 0.75, head_size * 0.5)), shaderProg, [eye_size, eye_size, eye_size], Ct.GRAY)

        # assume limbs are cylinder
        limb_length = 0.2
        limb_radius = 0.05
        # Rememebr: default plane has x being uAxis, y being vAxis, and z being wAxis
        # limbxy, where x represents the limb number, and y represents upper(1) or lower(0) part of the limb
        """
        For Rotations
        Standard Limbs:
        - lower limbs: -120-120

        tail1 (the part that connects to torso): -115 to -180

        """

        # side 1
        joint0 =  Sphere(Point(( joint_radius *2 , 0, torso_length * 0.5)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb11 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length* 0.75], Ct.DARKORANGE4)
        joint0.setDefaultAngle(45, self.wAxis)
        joint0.setDefaultAngle(90, self.uAxis)

        joint1 =  Sphere(Point(( joint_radius *2 , 0, torso_length * 0.5)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb21 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius,limb_length* 0.75], Ct.DARKORANGE4)
        joint1.setDefaultAngle(45, self.wAxis)
        joint1.setDefaultAngle(90, self.uAxis)

        joint2 =  Sphere(Point(( joint_radius *2 , 0, torso_length * 0.5)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb31 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length* 0.75], Ct.DARKORANGE4)
        joint2.setDefaultAngle(45, self.wAxis)
        joint2.setDefaultAngle(90, self.uAxis)

        # side 2/opposing side of side 1
        joint3 =  Sphere(Point(( -joint_radius *2 , 0, torso_length * 0.5)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb41 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length* 0.75], Ct.DARKORANGE4)
        joint3.setDefaultAngle(-45, self.wAxis)
        joint3.setDefaultAngle(90, self.uAxis)
        
        joint4 =  Sphere(Point(( -joint_radius *2 , 0, torso_length * 0.5)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb51 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length* 0.75], Ct.DARKORANGE4)
        joint4.setDefaultAngle(-45, self.wAxis)
        joint4.setDefaultAngle(90, self.uAxis)

        joint5 =  Sphere(Point(( -joint_radius *2 , 0, torso_length * 0.5)), shaderProg, [joint_radius, joint_radius, joint_radius], Ct.DARKORANGE3)
        limb61 = Cylinder(Point((0, 0, limb_length)), shaderProg, [limb_radius, limb_radius, limb_length* 0.75], Ct.DARKORANGE4)
        joint5.setDefaultAngle(-45, self.wAxis)
        joint5.setDefaultAngle(90, self.uAxis)    
        
        # tail 
        tail_length = 0.25
        joint6 = Sphere(Point((0 , 0, -torso_length * 0.25)), shaderProg, [torso_radius, torso_radius/2, torso_radius], Ct.PURPLE)
        tail1 = Cylinder(Point((0, 0, tail_length)), shaderProg, [limb_radius*5, torso_radius, tail_length], Ct.DARKORANGE4) 
        joint6.setDefaultAngle(-180, self.uAxis)
        joint7 = Sphere(Point((0 , 0, tail_length)), shaderProg, [torso_radius, torso_radius/2, torso_radius], Ct.PURPLE)
        joint7.setDefaultAngle(0, self.uAxis)
        tail2 = Cylinder(Point((0, 0, tail_length)), shaderProg, [limb_radius*4.5, torso_radius, tail_length], Ct.DARKORANGE4) 
        joint8 = Sphere(Point((0 , 0, tail_length)), shaderProg, [torso_radius, torso_radius/2, torso_radius], Ct.PURPLE)
        joint8.setDefaultAngle(0, self.uAxis)
        tail3= Cylinder(Point((0, 0, tail_length)), shaderProg, [limb_radius*4, torso_radius, tail_length], Ct.DARKORANGE4) 
        joint9 = Sphere(Point((0 , 0, tail_length)), shaderProg, [torso_radius, torso_radius/2, torso_radius], Ct.PURPLE)
        joint9.setDefaultAngle(0, self.uAxis)
        tail4= Cylinder(Point((0, 0, tail_length)), shaderProg, [limb_radius*3.5, torso_radius, tail_length], Ct.DARKORANGE4) 
        joint10 = Sphere(Point((0 , 0, tail_length)), shaderProg, [torso_radius, torso_radius/2, torso_radius], Ct.PURPLE)
        joint10.setDefaultAngle(0, self.uAxis)
        tail5= Cone(Point((0, 0, tail_length)), shaderProg, [limb_radius*3.5, torso_radius, tail_length], Ct.DARKORANGE4) 


        # attach head and torso
        self.addChild(torso1)
        torso1.addChild(torso2)
        torso1.addChild(torJoint1)
        torJoint1.addChild(torso2)
        torso2.addChild(torJoint2)
        torJoint2.addChild(torso3)
        torso3.addChild(head)
        
        head.addChild(eye1)
        head.addChild(eye2)
        head.addChild(mouth1)
        head.addChild(mouth2)

        # attaching regular limbs
        torso3.addChild(joint0)
        joint0.addChild(limb11)

        torso2.addChild(joint1)
        joint1.addChild(limb21)
        
        torso1.addChild(joint2)
        joint2.addChild(limb31)

        torso3.addChild(joint3)
        joint3.addChild(limb41)

        torso2.addChild(joint4)
        joint4.addChild(limb51)

        torso1.addChild(joint5)
        joint5.addChild(limb61)


        # attaching tail
        torso1.addChild(joint6)
        joint6.addChild(tail1)
        tail1.addChild(joint7)
        joint7.addChild(tail2)
        tail2.addChild(joint8)
        joint8.addChild(tail3)
        tail3.addChild(joint9)
        joint9.addChild(tail4)
        tail4.addChild(joint10)
        joint10.addChild(tail5)

        # Store components in a dictionary for easier access
        self.componentList = [torJoint1, torJoint2, head, joint0, joint1, joint2, joint3, joint4, joint5, joint6, joint7, joint8, joint9, joint10]
        self.componentDict = {
            "torso1": torso1, "torso2":torso2, "torso3": torso3,
            "head": head, "eye1": eye1, "eye2": eye2, "mouth1": mouth1, "mouth2": mouth2,
            "joint0": joint0, "limb11": limb11,
            "joint2": joint1, "limb21": limb21, 
            "joint4": joint2, "limb31": limb31, 
            "joint6": joint3, "limb41": limb41, 
            "joint8": joint4, "limb51": limb51, 
            "joint10": joint5, "limb61": limb61, 
            "joint12": joint6, "tail1": tail1, "joint13": joint7, "tail2": tail2, "joint14": joint8, "tail3": tail3, "joint15": joint9, "tail4": tail4
        }
        
        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
        # 
        
        # the opposing limbs have the same rotations, just in opposite directions:
        # for joints 0 through 5
        joint0.setRotateExtent(self.uAxis, 45, 135)
        joint0.setRotateExtent(self.vAxis, joint0.default_vAngle, joint0.default_vAngle)
        joint0.setRotateExtent(self.wAxis, 0, 180)
        joint1.setRotateExtent(self.uAxis, 45, 135)
        joint1.setRotateExtent(self.vAxis, joint1.default_vAngle, joint1.default_vAngle)
        joint1.setRotateExtent(self.wAxis, 0, 180)
        joint2.setRotateExtent(self.uAxis, 45, 135)
        joint2.setRotateExtent(self.vAxis, joint2.default_vAngle, joint2.default_vAngle)
        joint2.setRotateExtent(self.wAxis, 0, 180)
        joint3.setRotateExtent(self.uAxis, 45, 135)
        joint3.setRotateExtent(self.vAxis, joint3.default_vAngle, joint3.default_vAngle)
        joint3.setRotateExtent(self.wAxis, -180, 0)
        joint4.setRotateExtent(self.uAxis, 45, 135)
        joint4.setRotateExtent(self.vAxis, joint4.default_vAngle, joint4.default_vAngle)
        joint4.setRotateExtent(self.wAxis, -180, 0)
        joint5.setRotateExtent(self.uAxis, 45, 135)
        joint5.setRotateExtent(self.vAxis, joint5.default_vAngle, joint5.default_vAngle)
        joint5.setRotateExtent(self.wAxis, -180, 0)

        # torso and other static components
        torso1.setRotateExtent(self.uAxis, torso1.default_uAngle, torso1.default_uAngle)
        torso1.setRotateExtent(self.vAxis, torso1.default_vAngle, torso1.default_vAngle)
        torso1.setRotateExtent(self.wAxis, torso1.default_wAngle, torso1.default_wAngle)
        torso2.setRotateExtent(self.uAxis, torso2.default_uAngle, torso2.default_uAngle)
        torso2.setRotateExtent(self.vAxis, torso2.default_vAngle, torso2.default_vAngle)
        torso2.setRotateExtent(self.wAxis, torso2.default_wAngle, torso2.default_wAngle)
        torso3.setRotateExtent(self.uAxis, torso3.default_uAngle, torso3.default_uAngle)
        torso3.setRotateExtent(self.vAxis, torso3.default_vAngle, torso3.default_vAngle)
        torso3.setRotateExtent(self.wAxis, torso3.default_wAngle, torso3.default_wAngle)
        tail1.setRotateExtent(self.uAxis, tail1.default_uAngle, tail1.default_uAngle)
        tail1.setRotateExtent(self.vAxis, tail1.default_vAngle, tail1.default_vAngle)
        tail1.setRotateExtent(self.wAxis, tail1.default_wAngle, tail1.default_wAngle)    
        tail2.setRotateExtent(self.uAxis, tail2.default_uAngle, tail2.default_uAngle)
        tail2.setRotateExtent(self.vAxis, tail2.default_vAngle, tail2.default_vAngle)
        tail2.setRotateExtent(self.wAxis, tail2.default_wAngle, tail2.default_wAngle)    
        tail3.setRotateExtent(self.uAxis, tail3.default_uAngle, tail3.default_uAngle)
        tail3.setRotateExtent(self.vAxis, tail3.default_vAngle, tail3.default_vAngle)
        tail3.setRotateExtent(self.wAxis, tail3.default_wAngle, tail3.default_wAngle)   
        tail4.setRotateExtent(self.uAxis, tail4.default_uAngle, tail4.default_uAngle)
        tail4.setRotateExtent(self.vAxis, tail4.default_vAngle, tail4.default_vAngle)
        tail4.setRotateExtent(self.wAxis, tail4.default_wAngle, tail4.default_wAngle)  
        eye1.setRotateExtent(self.uAxis, eye1.default_uAngle, eye1.default_uAngle)
        eye1.setRotateExtent(self.vAxis, eye1.default_vAngle, eye1.default_vAngle)
        eye1.setRotateExtent(self.wAxis, eye1.default_wAngle, eye1.default_wAngle)  
        eye2.setRotateExtent(self.uAxis, eye2.default_uAngle, eye2.default_uAngle)
        eye2.setRotateExtent(self.vAxis, eye2.default_vAngle, eye2.default_vAngle)
        eye2.setRotateExtent(self.wAxis, eye2.default_wAngle, eye2.default_wAngle)  
        mouth1.setRotateExtent(self.uAxis, mouth1.default_uAngle, mouth1.default_uAngle)
        mouth1.setRotateExtent(self.vAxis, mouth1.default_vAngle, mouth1.default_vAngle)
        mouth1.setRotateExtent(self.wAxis, mouth1.default_wAngle, mouth1.default_wAngle)  
        mouth2.setRotateExtent(self.uAxis, mouth2.default_uAngle, mouth2.default_uAngle)
        mouth2.setRotateExtent(self.vAxis, mouth2.default_vAngle, mouth2.default_vAngle)
        mouth2.setRotateExtent(self.wAxis, mouth2.default_wAngle, mouth2.default_wAngle)            

        # for torso joints
        torJoint1.setRotateExtent(self.uAxis, -30, 30)
        torJoint1.setRotateExtent(self.vAxis, torJoint1.default_vAngle, torJoint1.default_vAngle)
        torJoint1.setRotateExtent(self.wAxis, torJoint1.default_wAngle, torJoint1.default_wAngle)
        torJoint2.setRotateExtent(self.uAxis, -30, 30)
        torJoint2.setRotateExtent(self.vAxis, torJoint2.default_vAngle, torJoint2.default_vAngle)
        torJoint2.setRotateExtent(self.wAxis, torJoint2.default_wAngle, torJoint2.default_wAngle)

        # tail joints, 6-10
        joint6.setRotateExtent(self.uAxis, -225, -135)
        joint6.setRotateExtent(self.vAxis, joint6.default_vAngle, joint6.default_vAngle)
        joint6.setRotateExtent(self.wAxis, joint6.default_wAngle, joint6.default_wAngle)
        joint7.setRotateExtent(self.uAxis, -45, 45)
        joint7.setRotateExtent(self.vAxis, joint7.default_vAngle, joint7.default_vAngle)
        joint7.setRotateExtent(self.wAxis, joint7.default_wAngle, joint7.default_wAngle)
        joint8.setRotateExtent(self.uAxis, -45, 45)
        joint8.setRotateExtent(self.vAxis, joint8.default_vAngle, joint8.default_vAngle)
        joint8.setRotateExtent(self.wAxis, joint8.default_wAngle, joint8.default_wAngle)
        joint9.setRotateExtent(self.uAxis, -45, 45)
        joint9.setRotateExtent(self.vAxis, joint9.default_vAngle, joint9.default_vAngle)
        joint9.setRotateExtent(self.wAxis, joint9.default_wAngle, joint9.default_wAngle)
        joint10.setRotateExtent(self.uAxis, -45, 45)
        joint10.setRotateExtent(self.vAxis, joint10.default_vAngle, joint10.default_vAngle)
        joint10.setRotateExtent(self.wAxis, joint10.default_wAngle, joint10.default_wAngle)

        # head
        head.setRotateExtent(self.uAxis, head.default_uAngle, head.default_uAngle)
        head.setRotateExtent(self.vAxis, head.default_vAngle, head.default_vAngle)

