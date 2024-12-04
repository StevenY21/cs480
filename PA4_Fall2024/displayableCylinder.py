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

# NOTE: FOR SOME REASON THE FILE NAME MIGHT BE LOWERCASE WHEN YOU DOWNLOAD IT, please make sure it says DisplayableCylinder
class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current cylinder's information, read-only
    nsides = 0
    radius = 0
    height = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, radius=0.5, height=1, nsides=36, color=ColorType.SOFTBLUE):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, height, nsides, color)

    def generate(self, radius=0.5, height=1, nsides=36, color=ColorType.SOFTBLUE):
        self.radius = radius
        self.height = height 
        self.nsides = nsides
        self.color = color
        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        # add one for padding
        # hard coded the stacks
        self.vertices = np.zeros([(nsides+1)*4 + 2, 11]) # 4 stacks of cylinder side vertices + bottom and top cap center vertices
        self.indices = np.zeros([(nsides+1)*4 + 2, 3]) # triangles for cylinder sides, bottom, and top
        for i in range(nsides+1):
            # params for cylinder
            # x = rcos(theta)
            # y = rsin(theta)
            # z = u, in this case hard coded based on which stack
            x = self.radius * math.cos(2 * math.pi * i/nsides)
            y = self.radius * math.sin(2 * math.pi * i/nsides)
            z = 0
            # 2 different vertices for both top and bottom/ +z and -z of the cylinder
            # surface normals
            # x = cos(theta)
            # y = sin(theta)
            # z = 0 
            nx = math.cos(2 * math.pi * i/nsides)
            ny = math.sin(2 * math.pi * i/nsides)
            nz = 0
            m = math.sqrt((nx**2)+(ny**2) + (nz**2))
            # "side" stacks, as in won't be part of the caps
            # this stack for closer to botton / -z
            self.vertices[i][0:9]  = [
                x,
                y,
                -height/2,
                nx/m,
                ny/m,
                0,
                *color
            ]
            # this stack for closer to top / +z
            # incrememnting by nsides to form the other stacks
            self.vertices[i + (nsides + 1)][0:9] = [
                x,
                y,
                height/2,
                nx/m,
                ny/m,
                0,
                *color
            ]
            # bottom cap stack, surface normals face "downward"
            self.vertices[i + ((nsides + 1)*2)][0:9] = [
                x,
                y,
                -height/2,
                0,
                0,
                -1,
                *color
            ]
            # top cap stack, surface normals faced "upward" 
            self.vertices[i + ((nsides + 1)*3)][0:9] = [
                x,
                y,
                height/2,
                0,
                0,
                1,
                *color
            ]
        
        index = 0
        for i in range(nsides+1):
            # Side triangles, 2 at a time
            self.indices[index] = [
                i, #v1
                i + 1, # v2
                i + nsides + 1 # v3
            ]
            self.indices[index + 1] = [
                i + 1, # v2
                i + nsides + 1, # v3
                i + nsides + 2, # v4
            ]
            index += 2
        # get indices for bottom cap / -z
        botCenterIdx = len(self.vertices) - 2 # a center index for connecting triangles to cap it
        self.vertices[botCenterIdx][0:9] = [0, 0, -height/2, 0, 0, -1, *color]
        index += 1
        # bottom cap vertices are the 3rd set vertices, so 2* needed
        for i in range(nsides+1):
            self.indices[index] = [
                botCenterIdx,
                i + 2 * (nsides + 1),
                (i + 1) % (nsides + 1) + 2 * (nsides + 1) # % needed as it loops in a circle
            ]

            index += 1

        # get indices for top cap / +z
        topCenterIdx = len(self.vertices) - 1 
        index += 1
        self.vertices[topCenterIdx][0:9] = [0, 0, height/2, 0, 0, 1, *color]
        for i in range(nsides+1):
            self.indices[index] =[
                topCenterIdx,
                i + (3 * (nsides + 1)),
                ((i + 1) % (nsides + 1)) + (3 * (nsides + 1))
            ]
            index += 1

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