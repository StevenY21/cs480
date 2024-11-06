"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

Modified by Daniel Scrivener 08/2022
"""
import random

from Component import Component
from Shapes import Cone, Cube, Cylinder, Sphere
from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.
class Predator(Component, EnvironmentObject):
    """
    
    """
    components = None
    contextParent = None
    componentDict = None
    leg_components = None
    rotation_speed = []
    translation_speed = None
    speed = None
    direction = 1

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super(Predator, self).__init__(position)
        jointRad = 0.1 * 0.6
        jointLen = 0.25 * 0.6
        # body parts are Cylinders
        bodyLen = 0.25 * 0.6
        bodyWid = 0.3 * 0.6
        bodyRad = 0.1 * 0.6
        # body parts and joints get smaller and smaller the closer it gets to the head
        body1 = Cylinder(Point((0, 0, 0)), shaderProg, [bodyWid, bodyRad, jointLen], Ct.SOFTBLUE)
        bodyJoint1 = Sphere(Point((0, 0, jointLen)), shaderProg, [bodyWid, bodyRad, jointLen/2], Ct.YELLOW)
                # Head is a sphere
        headSize = 0.2 * 0.6
        headJoint = Sphere(Point((0, 0, jointLen)), shaderProg, [bodyWid * 0.7, bodyRad * 0.8, jointLen/4], Ct.BLUEGREEN)
        head = Sphere(Point((0, 0, jointLen * 0.5)), shaderProg, [bodyWid , bodyRad, headSize], Ct.YELLOW)
        # mouth has 2 cones
        mouth_size = headSize/5
        mouth1 = Cone(Point((bodyRad, 0, headSize)), shaderProg, [mouth_size, mouth_size, mouth_size], Ct.GRAY)
        mouth2 = Cone(Point((-bodyRad, 0, headSize)), shaderProg, [mouth_size, mouth_size, mouth_size], Ct.GRAY)

        # eyes are 2 small spheres
        eyeSize = 0.02 * 0.6
        eye1 = Cube(Point((eyeSize*2, bodyRad * 0.75, headSize * 0.5)), shaderProg, [eyeSize, eyeSize, eyeSize], Ct.GRAY)
        eye2 = Cube(Point((eyeSize*-2, bodyRad * 0.75, headSize * 0.5)), shaderProg, [eyeSize, eyeSize, eyeSize], Ct.GRAY)
        self.translation_speed = Point([random.random()-0.5 for _ in range(3)]).normalize() * 0.01
        # assume limbs are cylinder
        limbLen = 0.2 * 0.6
        limbRad = 0.05 * 0.6
        # Rememebr: default plane has x being uAxis, y being vAxis, and z being wAxis
        # limbxy, where x represents the limb number, and y represents upper(1) or lower(0) part of the limb
        # side 1
        joint0 =  Sphere(Point(( jointRad *2 , 0, bodyLen * 0.125)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb11 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint0.setDefaultAngle(45, self.wAxis)
        joint0.setDefaultAngle(90, self.uAxis)
        self.rotation_speed.append([0.5, 0, 0])

        joint1 =  Sphere(Point(( jointRad *2 , 0, bodyLen * 0.875)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb21 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint1.setDefaultAngle(45, self.wAxis)
        joint1.setDefaultAngle(90, self.uAxis)
        self.rotation_speed.append([0.5, 0, 0])
        # side 2/opposing side of side 1, which puts on the other side/ negative x side
        joint3 =  Sphere(Point(( -jointRad *2 , 0, bodyLen * 0.125)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb41 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint3.setDefaultAngle(315, self.wAxis)
        joint3.setDefaultAngle(90, self.uAxis)
        self.rotation_speed.append([0.5, 0, 0])
        
        joint4 =  Sphere(Point(( -jointRad *2 , 0, bodyLen * 0.875)), shaderProg, [jointRad, jointRad, jointRad], Ct.DARKORANGE3)
        limb51 = Cylinder(Point((0, 0, limbLen)), shaderProg, [limbRad, limbRad, limbLen* 0.75], Ct.DARKORANGE4)
        joint4.setDefaultAngle(315, self.wAxis)
        joint4.setDefaultAngle(90, self.uAxis)
        self.rotation_speed.append([0.5, 0, 0])
        tailLen = 0.25 * 0.6
        # joint 6 is a little different due to being attached to the initial body, and will have a "reflected" angle range
        joint6 = Sphere(Point((0 , 0, -bodyLen * 0.25)), shaderProg, [bodyWid, bodyRad, tailLen/2], Ct.PURPLE)
        tail1 = Cylinder(Point((0, 0, tailLen)), shaderProg, [limbRad*5, bodyRad, tailLen], Ct.DARKORANGE1) 
        joint6.setDefaultAngle(-180, self.uAxis)
        joint10 = Sphere(Point((0 , 0, tailLen)), shaderProg, [bodyRad, bodyRad, tailLen/2], Ct.PURPLE)
        joint10.setDefaultAngle(0, self.uAxis)
        tail5= Cone(Point((0, 0, tailLen)), shaderProg, [limbRad*3.5, bodyRad, tailLen], Ct.BLACK) 

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.5
        self.species_id = 1
        # attach head and body parts
        self.addChild(body1)
        body1.addChild(headJoint)
        
        headJoint.addChild(head)
        head.addChild(eye1)
        head.addChild(eye2)
        head.addChild(mouth1)
        head.addChild(mouth2)

        # attaching regular limbs
        body1.addChild(joint0)
        joint0.addChild(limb11)

        body1.addChild(joint1)
        joint1.addChild(limb21)
        body1.addChild(joint3)
        joint3.addChild(limb41)

        body1.addChild(joint4)
        joint4.addChild(limb51)
        # attaching tail
        body1.addChild(joint6)
        joint6.addChild(tail1)
        tail1.addChild(joint10)
        joint10.addChild(tail5)

        # Store moveable components in a list and all components in the dict
        self.componentList = [bodyJoint1, headJoint, joint0, joint1, joint3, joint4, joint6, joint10]

        self.componentDict = {
            "body1": body1, "headJoint": headJoint,
            "head": head, "eye1": eye1, "eye2": eye2, "mouth1": mouth1, "mouth2": mouth2,
            "joint0": joint0, "limb11": limb11,
            "joint1": joint1, "limb21": limb21, 
            "joint3": joint3, "limb41": limb41, 
            "joint4": joint4, "limb51": limb51, 
            "joint6": joint6, "tail1": tail1,
            "joint10": joint10, "bodyJoint1": bodyJoint1

        }
        self.leg_components = [joint0, joint1, joint3, joint4]
        joint0.setRotateExtent(self.uAxis, 45, 135)
        joint0.setRotateExtent(self.vAxis, joint0.default_vAngle, joint0.default_vAngle)
        joint0.setRotateExtent(self.wAxis, 0, 120)
        joint1.setRotateExtent(self.uAxis, 45, 135)
        joint1.setRotateExtent(self.vAxis, joint1.default_vAngle, joint1.default_vAngle)
        joint1.setRotateExtent(self.wAxis, 0, 120)
        joint3.setRotateExtent(self.uAxis, 45, 135)
        joint3.setRotateExtent(self.vAxis, joint3.default_vAngle, joint3.default_vAngle)
        joint3.setRotateExtent(self.wAxis, 240, 360)
        joint4.setRotateExtent(self.uAxis, 45, 135)
        joint4.setRotateExtent(self.vAxis, joint4.default_vAngle, joint4.default_vAngle)
        joint4.setRotateExtent(self.wAxis, 240, 360)

        # body and other static components
        # set to not be able to be moved, this part is possibly redundant but keeping in case
        body1.setRotateExtent(self.uAxis, body1.default_uAngle, body1.default_uAngle)
        body1.setRotateExtent(self.vAxis, body1.default_vAngle, body1.default_vAngle)
        body1.setRotateExtent(self.wAxis, body1.default_wAngle, body1.default_wAngle)
        tail1.setRotateExtent(self.uAxis, tail1.default_uAngle, tail1.default_uAngle)
        tail1.setRotateExtent(self.vAxis, tail1.default_vAngle, tail1.default_vAngle)
        tail1.setRotateExtent(self.wAxis, tail1.default_wAngle, tail1.default_wAngle)     
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

        # tail joints, 6-10
        # all tail joints can move along x and y but not z
        joint6.setRotateExtent(self.uAxis, -225, -135)
        joint6.setRotateExtent(self.vAxis, -15, 15)
        joint6.setRotateExtent(self.wAxis, joint6.default_wAngle, joint6.default_wAngle)
        joint10.setRotateExtent(self.uAxis, -45, 45)
        joint10.setRotateExtent(self.vAxis, -15, 15)
        joint10.setRotateExtent(self.wAxis, joint10.default_wAngle, joint10.default_wAngle)

        # head
        # the joint can rotate all axis
        head.setRotateExtent(self.uAxis, head.default_uAngle, head.default_uAngle)
        head.setRotateExtent(self.vAxis, head.default_vAngle, head.default_vAngle)
        head.setRotateExtent(self.wAxis, head.default_wAngle, head.default_wAngle)  
        headJoint.setRotateExtent(self.uAxis, -45, 45)
        headJoint.setRotateExtent(self.wAxis, 15, -15)
        headJoint.setRotateExtent(self.vAxis, -15, 15)
    def animationUpdate(self):

        for i, comp in enumerate(self.leg_components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            #comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            #comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1

    def stepForward(self, components, tank_dimensions, vivarium):
        for i, comp in enumerate(components):
            if self == comp:
                main_component = components[i]
                break
        pos = main_component.currentPos
        u_max = tank_dimensions[0]/2
        u_min = u_max * -1
        v_max = tank_dimensions[1]/2
        v_min = v_max * -1
        w_max = tank_dimensions[2]/2
        w_min = w_max * -1
            # 1. Tank Boundary Collision Detection
        # Check each axis and reverse direction if beyond boundaries
        # currently just going to reverse direction
        if pos[0] - self.bound_radius < u_min or pos[0] + self.bound_radius > u_max:
            self.translation_speed = self.translation_speed.reflect(Point([1, 0, 0]))
        if pos[1] - self.bound_radius < v_min or pos[1] + self.bound_radius > v_max:
            self.translation_speed = self.translation_speed.reflect(Point([0, 1, 0])) 
        if pos[2] - self.bound_radius < w_min or pos[2] + self.bound_radius > w_max:
            self.translation_speed = self.translation_speed.reflect(Point([0, 0, 1]))
        for i, comp in enumerate(components):
            if comp is not self and i != 0 and comp.species_id == self.species_id:  # ignore self and the tank
                other_pos = comp.currentPos
                dist = pos.distance(other_pos)
                if dist < self.bound_radius + comp.bound_radius:  # Bounding sphere collision
                    # for now just change direction
                    self.direction *= -1
                    

        # Update position by translation speed
        new_pos = pos + (self.translation_speed * self.direction)
        main_component.setCurrentPosition(new_pos)
class Prey(Component, EnvironmentObject):
    """
    Prey model with animation
    """
    components = None
    moving_components = None
    rotation_speed = None
    translation_speed = None
    speed = None
    direction = 1

    def __init__(self, parent, position, shaderProg):
        super(Prey, self).__init__(position)
        body = ModelBody(parent, Point((0, 0,0)), shaderProg)
        arm1 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2.setDefaultAngle(90, arm2.vAxis)
        arm3 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm3.setDefaultAngle(180, arm3.vAxis)
        arm4 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm4.setDefaultAngle(270, arm4.vAxis)

        self.components = body.components + arm1.components + arm2.components + arm3.components + arm4.components
        self.moving_components = arm1.components + arm2.components + arm3.components + arm4.components
        self.addChild(body)
        self.addChild(arm1)
        self.addChild(arm2)
        self.addChild(arm3)
        self.addChild(arm4)
        self.rotation_speed = []
        for comp in self.moving_components:
            comp.setRotateExtent(comp.uAxis, 0, 30)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)
            self.rotation_speed.append([0.5, 0, 0])

        self.translation_speed = Point([random.random()-0.5 for _ in range(3)]).normalize() * 0.01

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.3
        self.species_id = 1

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints
        for i, comp in enumerate(self.moving_components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            #comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1
        #self.vAngle = (self.vAngle + 3) % 360

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.
        # Assume the main position and translation are handled by the first component of `components`
        for i, comp in enumerate(components):
            if self == comp:
                main_component = components[i]
                break
        pos = main_component.currentPos
        u_max = tank_dimensions[0]/2
        u_min = u_max * -1
        v_max = tank_dimensions[1]/2
        v_min = v_max * -1
        w_max = tank_dimensions[2]/2
        w_min = w_max * -1
            # 1. Tank Boundary Collision Detection
        # Check each axis and reverse direction if beyond boundaries
        # reflects based on what axis limit it reached
        if pos[0] - self.bound_radius < u_min or pos[0] + self.bound_radius > u_max:
            self.translation_speed = self.translation_speed.reflect(Point([1, 0, 0]))
        if pos[1] - self.bound_radius < v_min or pos[1] + self.bound_radius > v_max:
            self.translation_speed = self.translation_speed.reflect(Point([0, 1, 0])) 
        if pos[2] - self.bound_radius < w_min or pos[2] + self.bound_radius > w_max:
            self.translation_speed = self.translation_speed.reflect(Point([0, 0, 1]))
        for i, comp in enumerate(components):
            if comp is not self and i != 0:  # ignore self and the tank
                other_pos = comp.currentPos
                dist = pos.distance(other_pos)
                if dist < self.bound_radius + comp.bound_radius:  # Bounding sphere collision
                    # for now just change direction
                    self.direction *= -1
                    

        # Update position by translation speed
        new_pos = pos + (self.translation_speed * self.direction)
        main_component.setCurrentPosition(new_pos)

class ModelArm(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE1)
        link2 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE2)
        link3 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE3)
        link4 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]
class ModelBody(Component):
    """
    Linkage model for the main body, including antennae eyes
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        torso = Sphere(Point((0, 0, 0)), shaderProg, [linkageLength, linkageLength, linkageLength], Ct.RED)
        self.addChild(torso)
        antenna_radius = linkageLength * 0.125
        antenna_length = linkageLength * 0.66
        # Left antenna
        left_antenna_shaft = Cylinder(Point((antenna_radius*2, 0, linkageLength)), shaderProg, [antenna_radius, antenna_radius, antenna_length], Ct.GREEN)
        left_antenna_tip = Sphere(Point((0, 0, antenna_length)), shaderProg, [antenna_radius * 1.2, antenna_radius * 1.2, antenna_radius * 1.2], Ct.GREENYELLOW)
        torso.addChild(left_antenna_shaft)
        left_antenna_shaft.addChild(left_antenna_tip)
        # Right antenna
        right_antenna_shaft = Cylinder(Point((-antenna_radius*2, 0, linkageLength)), shaderProg, [antenna_radius, antenna_radius, antenna_length], Ct.GREEN)
        right_antenna_tip = Sphere(Point((0, 0, antenna_length)), shaderProg, [antenna_radius * 1.2, antenna_radius * 1.2, antenna_radius * 1.2], Ct.GREENYELLOW)
        torso.addChild(right_antenna_shaft)
        right_antenna_shaft.addChild(right_antenna_tip)

        # Add components to the list
        self.components = [torso, left_antenna_shaft, left_antenna_tip, right_antenna_shaft, right_antenna_tip]
        left_antenna_shaft.setCurrentAngle(-90, self.uAxis)
        right_antenna_shaft.setCurrentAngle(-90, self.uAxis)

