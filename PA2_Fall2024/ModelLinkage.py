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
        # note: a few of these variables are not used exactly as specified, due to me constantly modifying each individual component
        # they are the standard for some parts, but not the standard for other parts
        # assume joints are sphere
        jointRad = 0.1
        jointLen = 0.25
        # body parts are Cylinders
        bodyLen = 0.25
        bodyWid = 0.3
        bodyRad = 0.1
        # body parts and joints get smaller and smaller the closer it gets to the head
        body1 = Cylinder(Point((0, 0, 0)), shaderProg, [bodyWid, bodyRad, jointLen], Ct.SOFTBLUE)
        bodyJoint1 = Sphere(Point((0, 0, jointLen)), shaderProg, [bodyWid, bodyRad, jointLen/2], Ct.YELLOW)
        body2 = Cylinder(Point((0, 0, jointLen)), shaderProg, [bodyWid * 0.9, bodyRad * 0.9, jointLen], Ct.CYAN)
        bodyJoint2 = Sphere(Point((0, 0, jointLen)), shaderProg, [bodyWid * 0.8, bodyRad * 0.9, jointLen/2], Ct.YELLOW)
        body3 = Cylinder(Point((0, 0, jointLen)), shaderProg, [bodyWid * 0.8, bodyRad * 0.8, jointLen], Ct.BLUE)

        # Head is a sphere
        headSize = 0.2
        headJoint = Sphere(Point((0, 0, jointLen)), shaderProg, [bodyWid * 0.7, bodyRad * 0.8, jointLen/4], Ct.GREEN)
        head = Sphere(Point((0, 0, jointLen * 0.5)), shaderProg, [bodyWid , bodyRad, headSize], Ct.YELLOW)
        # mouth has 2 cones
        mouth_size = headSize/5
        mouth1 = Cone(Point((bodyRad, 0, headSize)), shaderProg, [mouth_size, mouth_size, mouth_size], Ct.GRAY)
        mouth2 = Cone(Point((-bodyRad, 0, headSize)), shaderProg, [mouth_size, mouth_size, mouth_size], Ct.GRAY)

        # eyes are 2 small spheres
        eyeSize = 0.02
        eye1 = Cube(Point((eyeSize*2, bodyRad * 0.75, headSize * 0.5)), shaderProg, [eyeSize, eyeSize, eyeSize], Ct.GRAY)
        eye2 = Cube(Point((eyeSize*-2, bodyRad * 0.75, headSize * 0.5)), shaderProg, [eyeSize, eyeSize, eyeSize], Ct.GRAY)

        # assume limbs are cylinder
        limbLen = 0.2
        limbRad = 0.05
        # Rememebr: default plane has x being uAxis, y being vAxis, and z being wAxis
        # limbxy, where x represents the limb number, and y represents upper(1) or lower(0) part of the limb

        # side 1
        joint0 =  Sphere(Point(( jointRad *2 , 0, bodyLen * 0.5)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb11 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint0.setDefaultAngle(45, self.wAxis)
        joint0.setDefaultAngle(90, self.uAxis)

        joint1 =  Sphere(Point(( jointRad *2 , 0, bodyLen * 0.5)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb21 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint1.setDefaultAngle(45, self.wAxis)
        joint1.setDefaultAngle(90, self.uAxis)

        joint2 =  Sphere(Point(( jointRad *2 , 0, bodyLen * 0.5)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb31 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint2.setDefaultAngle(45, self.wAxis)
        joint2.setDefaultAngle(90, self.uAxis)

        # side 2/opposing side of side 1, which puts on the other side/ negative x side
        joint3 =  Sphere(Point(( -jointRad *2 , 0, bodyLen * 0.5)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb41 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint3.setDefaultAngle(315, self.wAxis)
        joint3.setDefaultAngle(90, self.uAxis)
        
        joint4 =  Sphere(Point(( -jointRad *2 , 0, bodyLen * 0.5)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb51 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint4.setDefaultAngle(315, self.wAxis)
        joint4.setDefaultAngle(90, self.uAxis)

        joint5 =  Sphere(Point(( -jointRad *2 , 0, bodyLen * 0.5)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb61 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint5.setDefaultAngle(315, self.wAxis)
        joint5.setDefaultAngle(90, self.uAxis)    
        
        # tailparts are cylinders and one cone
        tailLen = 0.25
        # joint 6 is a little different due to being attached to the initial body, and will have a "reflected" angle range
        joint6 = Sphere(Point((0 , 0, -bodyLen * 0.25)), shaderProg, [bodyWid, bodyRad, tailLen/2], Ct.PURPLE)
        tail1 = Cylinder(Point((0, 0, tailLen)), shaderProg, [limbRad*5, bodyRad, tailLen], Ct.DARKORANGE1) 
        joint6.setDefaultAngle(-180, self.uAxis)
        # tail parts get smaller and smaller 
        joint7 = Sphere(Point((0 , 0, tailLen)), shaderProg, [bodyRad, bodyRad, tailLen/2], Ct.PURPLE)
        joint7.setDefaultAngle(0, self.uAxis)
        tail2 = Cylinder(Point((0, 0, tailLen)), shaderProg, [limbRad*4.5, bodyRad, tailLen], Ct.DARKORANGE2) 
        joint8 = Sphere(Point((0 , 0, tailLen)), shaderProg, [bodyRad, bodyRad, tailLen/2], Ct.PURPLE)
        joint8.setDefaultAngle(0, self.uAxis)
        tail3= Cylinder(Point((0, 0, tailLen)), shaderProg, [limbRad*4, bodyRad, tailLen], Ct.DARKORANGE3) 
        joint9 = Sphere(Point((0 , 0, tailLen)), shaderProg, [bodyRad, bodyRad, tailLen/2], Ct.PURPLE)
        joint9.setDefaultAngle(0, self.uAxis)
        tail4= Cylinder(Point((0, 0, tailLen)), shaderProg, [limbRad*3.5, bodyRad, tailLen], Ct.DARKORANGE4) 
        joint10 = Sphere(Point((0 , 0, tailLen)), shaderProg, [bodyRad, bodyRad, tailLen/2], Ct.PURPLE)
        joint10.setDefaultAngle(0, self.uAxis)
        tail5= Cone(Point((0, 0, tailLen)), shaderProg, [limbRad*3.5, bodyRad, tailLen], Ct.BLACK) 


        # attach head and body parts
        self.addChild(body1)
        body1.addChild(body2)
        body1.addChild(bodyJoint1)
        bodyJoint1.addChild(body2)
        body2.addChild(bodyJoint2)
        bodyJoint2.addChild(body3)
        body3.addChild(headJoint)
        
        headJoint.addChild(head)
        head.addChild(eye1)
        head.addChild(eye2)
        head.addChild(mouth1)
        head.addChild(mouth2)

        # attaching regular limbs
        body3.addChild(joint0)
        joint0.addChild(limb11)

        body2.addChild(joint1)
        joint1.addChild(limb21)
        
        body1.addChild(joint2)
        joint2.addChild(limb31)

        body3.addChild(joint3)
        joint3.addChild(limb41)

        body2.addChild(joint4)
        joint4.addChild(limb51)

        body1.addChild(joint5)
        joint5.addChild(limb61)


        # attaching tail
        body1.addChild(joint6)
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
        self.componentList = [bodyJoint1, bodyJoint2, headJoint, joint0, joint1, joint2, joint3, joint4, joint5, joint6, joint7, joint8, joint9, joint10
                              
                              ]
        self.componentDict = {
            "body1": body1, "body2":body2, "body3": body3, "headJoint": headJoint,
            "head": head, "eye1": eye1, "eye2": eye2, "mouth1": mouth1, "mouth2": mouth2,
            "joint0": joint0, "limb11": limb11,
            "joint1": joint1, "limb21": limb21, 
            "joint2": joint2, "limb31": limb31, 
            "joint3": joint3, "limb41": limb41, 
            "joint4": joint4, "limb51": limb51, 
            "joint5": joint5, "limb61": limb61, 
            "joint6": joint6, "tail1": tail1, "joint7": joint7, "tail2": tail2, "joint8": joint8, "tail3": tail3, "joint9": joint9, "tail4": tail4,
            "joint10": joint10, "bodyJoint1": bodyJoint1, "bodyJoint2": bodyJoint2

        }
        
        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
        # 
        
        # the opposing limbs have the same rotation extent, will be rotating differently to deal with mirrored movement
        # for joints 0 through 5
        # all these joints cannot rotate in the y axis, only in x and z
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
        joint3.setRotateExtent(self.wAxis, 180, 360)
        joint4.setRotateExtent(self.uAxis, 45, 135)
        joint4.setRotateExtent(self.vAxis, joint4.default_vAngle, joint4.default_vAngle)
        joint4.setRotateExtent(self.wAxis, 180, 360)
        joint5.setRotateExtent(self.uAxis, 45, 135)
        joint5.setRotateExtent(self.vAxis, joint5.default_vAngle, joint5.default_vAngle)
        joint5.setRotateExtent(self.wAxis, 180, 360)

        # body and other static components
        # set to not be able to be moved, this part is possibly redundant
        body1.setRotateExtent(self.uAxis, body1.default_uAngle, body1.default_uAngle)
        body1.setRotateExtent(self.vAxis, body1.default_vAngle, body1.default_vAngle)
        body1.setRotateExtent(self.wAxis, body1.default_wAngle, body1.default_wAngle)
        body2.setRotateExtent(self.uAxis, body2.default_uAngle, body2.default_uAngle)
        body2.setRotateExtent(self.vAxis, body2.default_vAngle, body2.default_vAngle)
        body2.setRotateExtent(self.wAxis, body2.default_wAngle, body2.default_wAngle)
        body3.setRotateExtent(self.uAxis, body3.default_uAngle, body3.default_uAngle)
        body3.setRotateExtent(self.vAxis, body3.default_vAngle, body3.default_vAngle)
        body3.setRotateExtent(self.wAxis, body3.default_wAngle, body3.default_wAngle)
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

        # for body joints
        bodyJoint1.setRotateExtent(self.uAxis, -30, 30)
        bodyJoint1.setRotateExtent(self.vAxis, -15, 15)
        bodyJoint1.setRotateExtent(self.wAxis, bodyJoint1.default_wAngle, bodyJoint1.default_wAngle)
        bodyJoint2.setRotateExtent(self.uAxis, -30, 30)
        bodyJoint2.setRotateExtent(self.vAxis,-15, 15)
        bodyJoint2.setRotateExtent(self.wAxis, bodyJoint2.default_wAngle, bodyJoint2.default_wAngle)

        # tail joints, 6-10
        # all tail joints can move along x and y but not z
        joint6.setRotateExtent(self.uAxis, -225, -135)
        joint6.setRotateExtent(self.vAxis, -15, 15)
        joint6.setRotateExtent(self.wAxis, joint6.default_wAngle, joint6.default_wAngle)
        joint7.setRotateExtent(self.uAxis, -45, 45)
        joint7.setRotateExtent(self.vAxis, -15, 15)
        joint7.setRotateExtent(self.wAxis, joint7.default_wAngle, joint7.default_wAngle)
        joint8.setRotateExtent(self.uAxis, -45, 45)
        joint8.setRotateExtent(self.vAxis, -15, 15)
        joint8.setRotateExtent(self.wAxis, joint8.default_wAngle, joint8.default_wAngle)
        joint9.setRotateExtent(self.uAxis, -45, 45)
        joint9.setRotateExtent(self.vAxis, -15, 15)
        joint9.setRotateExtent(self.wAxis, joint9.default_wAngle, joint9.default_wAngle)
        joint10.setRotateExtent(self.uAxis, -45, 45)
        joint10.setRotateExtent(self.vAxis, -15, 15)
        joint10.setRotateExtent(self.wAxis, joint10.default_wAngle, joint10.default_wAngle)

        # head
        # the joint can rotate the entire z-axis, and move in x and y
        head.setRotateExtent(self.uAxis, head.default_uAngle, head.default_uAngle)
        head.setRotateExtent(self.vAxis, head.default_vAngle, head.default_vAngle)
        head.setRotateExtent(self.wAxis, head.default_wAngle, head.default_wAngle)  
        headJoint.setRotateExtent(self.uAxis, -45, 45)
        headJoint.setRotateExtent(self.wAxis, 15, -15)
        headJoint.setRotateExtent(self.vAxis, -15, 15)

