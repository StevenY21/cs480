"""
Define a fixed scene with rotating lights
First version in 11/08/2021
:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math
import numpy as np
import ColorType
from Animation import Animation
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility
from DisplayableCube import DisplayableCube
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableTorus import DisplayableTorus
from DisplayableCylinder import DisplayableCylinder
# amongus character
class SceneThree(Component, Animation):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None
    lRadius = None
    lAngles = None
    lTransformations = None
    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()
        self.lTransformations = [self.glutility.translate(0, 2, 0, False),
                                 self.glutility.rotate(60, [0, 0, 1], False),
                                 self.glutility.rotate(120, [0, 0, 1], False)]
        self.lRadius = 3
        self.lAngles = [0, 0, 0]
        body = Component(Point((0, 0.75, 0)), DisplayableEllipsoid(shaderProg, 1.0, 1.5, 0.9, 48, 48, ColorType.RED))
        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.4, 0.8, 0.6, 0.1)), 64)
        body.setMaterial(m1)
        body.renderingRouting = "vertex lighting"
        self.addChild(body)
        eye = Component(Point((0, 1, 0.25)), DisplayableEllipsoid(shaderProg, 0.9, 0.5, 0.9, 36, 36))
        m2 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 1, 1)),
                      np.array((0.6, 0.4, 0.8, 1.0)), 64)
        eye.setMaterial(m2)
        eye.renderingRouting = "vertex lighting"
        self.addChild(eye)
        backpack = Component(Point((0, 0.8, -0.75)), DisplayableCube(shaderProg, 1.0, 1.5, 1.0, ColorType.RED))
        m3 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                np.array((0.6, 0.4, 0.8, 1.0)), 64)
        backpack.setMaterial(m3)
        backpack.renderingRouting = "vertex lighting"
        self.addChild(backpack)
        leg1 = Component(Point((0.5, -0.8, 0)), DisplayableCylinder(shaderProg, 0.25, 1.5, 36, ColorType.RED))
        m4 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
            np.array((0.6, 0.4, 0.8, 1.0)), 64)
        leg1.setMaterial(m4)
        leg1.renderingRouting = "vertex lighting"
        leg1.rotate(-90, leg1.uAxis)
        self.addChild(leg1)
        leg2 = Component(Point((-0.5, -0.8, 0)), DisplayableCylinder(shaderProg, 0.25, 1.5, 36, ColorType.RED))
        m5 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
            np.array((0.6, 0.4, 0.8, 1.0)), 64)
        leg2.setMaterial(m5)
        leg2.renderingRouting = "vertex lighting"
        leg2.rotate(-90, leg2.uAxis)
        self.addChild(leg2)
        l0 = Light(self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0]),
                   np.array((*ColorType.SOFTRED, 1.0)))
        lightCube0 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTRED))
        lightCube0.renderingRouting = "vertex"
        l1 = Light(self.lightPos(self.lRadius, self.lAngles[1], self.lTransformations[1]),
                   np.array((*ColorType.SOFTBLUE, 1.0)))
        lightCube1 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTBLUE))
        lightCube1.renderingRouting = "vertex"
        l2 = Light(self.lightPos(self.lRadius, self.lAngles[2], self.lTransformations[2]),
                   np.array((*ColorType.SOFTGREEN, 1.0)))
        lightCube2 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTGREEN))
        lightCube2.renderingRouting = "vertex"
        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.addChild(lightCube2)
        self.lights = [l0, l1, l2]
        self.lightCubes = [lightCube0, lightCube1, lightCube2]
    def lightPos(self, radius, thetaAng, transformationMatrix):
        r = np.zeros(4)
        r[0] = radius * math.cos(thetaAng / 180 * math.pi)
        r[2] = radius * math.sin(thetaAng / 180 * math.pi)
        r[3] = 1
        r = transformationMatrix @ r
        return r[0:3]
    def animationUpdate(self):
        self.lAngles[0] = (self.lAngles[0] + 0.5) % 360
        self.lAngles[1] = (self.lAngles[1] + 0.7) % 360
        self.lAngles[2] = (self.lAngles[2] + 1.0) % 360
        for i, v in enumerate(self.lights):
            lPos = self.lightPos(self.lRadius, self.lAngles[i], self.lTransformations[i])
            self.lightCubes[i].setCurrentPosition(Point(lPos))
            self.lights[i].setPosition(lPos)
            self.shaderProg.setLight(i, v)
        for c in self.children:
            if isinstance(c, Animation):
                c.animationUpdate()
    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()