"""
Define ellipsoid here.
First version in 11/01/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
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


class DisplayableEllipsoid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    stacks = 0
    slices = 0
    radiusX = 0
    radiusY = 0
    radiusZ = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, radiusX=0.6, radiusY=0.3, radiusZ=0.9, stacks=18, slices=36, color=ColorType.SOFTBLUE):
        super(DisplayableEllipsoid, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radiusX, radiusY, radiusZ, stacks, slices, color)

    def generate(self, radiusX=0.6, radiusY=0.3, radiusZ=0.9, stacks=18, slices=36, color=ColorType.SOFTBLUE):
        self.radiusX = radiusX
        self.radiusY = radiusY
        self.radiusZ = radiusZ
        self.stacks = stacks
        self.slices = slices
        self.color = color

        # we need to pad two more rows for poles and one more column for slice seam, to assign correct texture coord
        # add 2 to both stacks and slices
        self.vertices = np.zeros([(stacks+2) * (slices+2), 11])
        # u is for the horizontal angle, v for the vertical
        for i in range(0, stacks+1):
            u = i/stacks
            for j in range(0, slices+1):
                v = j/slices
                # [x, y, z, normal, color, texture coords]
                # x, y, z calculated using parametric equations for a torus
                # x(u,v)=radX*cosv*cosu
                # y(u,v)=radY*cosv*sinu
                # z(u,v)=radZ*sinv
                x = (self.radiusX*math.cos(v*2*math.pi)*math.cos(u*2*math.pi))
                y = self.radiusY*math.cos(v*2*math.pi)*math.sin(u*2*math.pi)
                z = self.radiusZ*math.sin(v*2*math.pi)
                # surface normals
                nx = (2*x)/(self.radiusX**2)
                ny = (2*y)/(self.radiusY**2)
                nz = (2*z)/(self.radiusZ**2)
                m = math.sqrt((nx**2)+(ny**2)+(nz**2))
                self.vertices[i * (slices+2) + j] [0:9] = [
                    x,
                    y,
                    z,
                    nx/m,
                    ny/m,
                    nz/m,
                    # color
                    *color
                    # textures maybe add later
                ]
        index = 0
        self.indices = np.zeros([stacks * slices * 2, 3])
        for i in range(stacks):
            for j in range(slices):
                # 2 triangles per "surface"
                self.indices[index] = [
                    i * (slices+2) + j, #v1 
                    i * (slices+2) + j + 1, #v2
                    (i + 1) * (slices+2) + j, #v3
                ]
                self.indices[index+1] = [
                    i * (slices+2) + j + 1, #v2
                    (i + 1) * (slices+2) + j, #v3
                    (i + 1) * (slices+2) + j + 1 #v4
                ]
                index+=2

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems which don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=11, offset=9, attribSize=2)
        self.vao.unbind()
