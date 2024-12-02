# displayableCylinder for displaying the cylinder with the caps
"""
Define Torus here.
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

##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    rings = 0
    innerRadius = 0
    outerRadius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(innerRadius, outerRadius, nsides, rings, color)

    def generate(self, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        self.innerRadius = innerRadius # 
        self.outerRadius = outerRadius # radius of the ring
        self.nsides = nsides
        self.rings = rings
        self.color = color

        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        # add one for padding
        self.vertices = np.zeros([(nsides+1) * (rings+1), 11])
        self.indices = np.zeros([rings * nsides * 2, 3])
        # for vertices
        for i in range(0, rings+1):
            u = i/rings
            for j in range(0, nsides+1):
                v = j/nsides
                # u is for the outer ring angle
                # v is for the "inside" of the torus
                # [x, y, z, normal, color, texture coords]
                self.vertices[i * (nsides+1) + j] [0:9] = [
                    # x, y, z calculated using parametric equations for a torus
                    # x(u,v)=(outerRadius+innerRadius*cosv)cosu, 
                    # y(u,v)=(outerRadius+innerRadius*cosv)sinu, 
                    # z(u,v)=innerRadius*sinv
                    (self.outerRadius + self.innerRadius * math.cos(v*2*math.pi)) * math.cos(u*2*math.pi),
                    (self.outerRadius + self.innerRadius * math.cos(v*2*math.pi)) * math.sin(u*2*math.pi),
                    (self.innerRadius * math.sin(v*2*math.pi)),
                    # normal
                    (self.outerRadius + self.innerRadius * math.cos(v*2*math.pi)) * math.cos(u*2*math.pi),
                    (self.outerRadius + self.innerRadius * math.cos(v*2*math.pi)) * math.sin(u*2*math.pi),
                    (self.innerRadius * math.sin(v*2*math.pi)),
                    # color
                    *color
                    # textures maybe add later
                ]
        index = 0
        for i in range(rings):
            for j in range(nsides):
                # 2 triangles per "surface"
                self.indices[index] = [
                    i * (nsides + 1) + j, 
                    (i + 1) * (nsides + 1) + j, 
                    i * (nsides + 1) + j + 1
                ]
                self.indices[index+1] = [
                    (i + 1) * (nsides + 1) + j, 
                    (i + 1) * (nsides + 1) + j + 1, 
                    i * (nsides + 1) + j + 1
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

        self.vao.unbind()