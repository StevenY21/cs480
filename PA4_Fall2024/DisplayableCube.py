"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType

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


class DisplayableCube(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    length = None
    width = None
    height = None
    color = None

    def __init__(self, shaderProg, length=1, width=1, height=1, color=ColorType.BLUE):
        super(DisplayableCube, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(length, width, height, color)

    def generate(self, length=1, width=1, height=1, color=None):
        self.length = length
        self.width = width
        self.height = height
        self.color = color

        self.vertices = np.zeros([24, 11])
        # can be reduced to only have unique vertices
        vl = np.array([
            # back face
            # 0, 1, 2, 0, 2, 3
            -length/2, -width/2, -height/2, 0, 0, -1, *color, # 0
            -length/2, width/2, -height/2, 0, 0, -1, *color, # 1
            length/2, width/2, -height/2, 0, 0, -1, *color, # 2
            #-length / 2, -width / 2, -height / 2, 0, 0, -1, *color, 0
            #length / 2, width / 2, -height / 2, 0, 0, -1, *color, 2
            length/2, -width/2, -height/2, 0, 0, -1, *color, # 3
            # front face
            # 4 5 6 4 6 7
            -length/2, -width/2, height/2, 0, 0, 1, *color, # 4
            length/2, -width/2, height/2, 0, 0, 1, *color, # 5
            length/2, width/2, height/2, 0, 0, 1, *color, # 6
            #-length / 2, -width / 2, height / 2, 0, 0, 1, *color, 
            #length / 2, width / 2, height / 2, 0, 0, 1, *color,
            -length/2, width/2, height/2, 0, 0, 1, *color, # 7
            # left face
            # 8 9 10 8 10 11
            -length/2, -width/2, -height/2, -1, 0, 0, *color, # 8
            -length/2, -width/2, height/2, -1, 0, 0, *color, # 9
            -length/2, width/2, height/2, -1, 0, 0, *color, # 10
            #-length / 2, -width / 2, -height / 2, -1, 0, 0, *color, 8
            #-length / 2, width / 2, height / 2, -1, 0, 0, *color, 10
            -length/2, width/2, -height/2, -1, 0, 0, *color, #11
            # right face
            # 12 13 14 12 14 15
            length/2, -width/2, height/2, 1, 0, 0, *color, # 12
            length/2, -width/2, -height/2, 1, 0, 0, *color, # 13
            length/2, width/2, -height/2, 1, 0, 0, *color, # 14
            #length / 2, -width / 2, height / 2, 1, 0, 0, *color, 12
            #length / 2, width / 2, -height / 2, 1, 0, 0, *color, 14
            length/2, width/2, height/2, 1, 0, 0, *color, # 15
            # top face
            # 16 17 18 16 18 19
            -length/2, width/2, height/2, 0, 1, 0, *color, # 16
            length/2, width/2, height/2, 0, 1, 0, *color, # 17
            length/2, width/2, -height/2, 0, 1, 0, *color, # 18
            #-length / 2, width / 2, height / 2, 0, 1, 0, *color, 16
            #length / 2, width / 2, -height / 2, 0, 1, 0, *color, 18
            -length/2, width/2, -height/2, 0, 1, 0, *color, # 19
            # bot face
            # 20 21 22 20 22 23
            -length/2, -width/2, -height/2, 0, -1, 0, *color, # 20
            length/2, -width/2, -height/2, 0, -1, 0, *color, # 21
            length/2, -width/2, height/2, 0, -1, 0, *color, # 22
            #-length / 2, -width / 2, -height / 2, 0, -1, 0, *color,
            #length / 2, -width / 2, height / 2, 0, -1, 0, *color,
            -length/2, -width/2, height/2, 0, -1, 0, *color, # 23
        ]).reshape((24, 9))
        self.vertices[0:24, 0:9] = vl

        self.indices = np.array([
            # back
            0, 1, 2,
            0, 2, 3,
            # front
            4, 5, 6,
            4, 6, 7,
            # left,
            8, 9, 10,
            8, 10, 11,
            # right
            12, 13, 14,
            12, 14, 15,
            # top
            16, 17, 18,
            16, 18, 19,
            # bottom
            20, 21, 22,
            20, 22, 23,
                                 ])

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is at here, switch from vbo to ebo
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
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
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

