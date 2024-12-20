"""
This is the main entry of your program. Almost all things you need to implement is in this file.
The main class Sketch inherit from CanvasBase. For the parts you need to implement, they all marked TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1

Submitted version modifed drawLine and drawTriangle
author: Steven Yao (styao@bu.edu)
id: U38800489
"""

import os

import wx
import math
import random
import numpy as np

from Buff import Buff
from Point import Point
from ColorType import ColorType
from CanvasBase import CanvasBase

try:
    # From pip package "Pillow"
    from PIL import Image
except Exception:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError


class Sketch(CanvasBase):
    """
    Please don't forget to override interrupt methods, otherwise NotImplementedError will throw out
    
    Class Variable Explanation:

    * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging
    
    * texture(Buff): loaded texture in Buff instance
    * random_color(bool): Control flag of random color generation of point.
    * doTexture(bool): Control flag of doing texture mapping
    * doSmooth(bool): Control flag of doing smooth
    * doAA(bool): Control flag of doing anti-aliasing
    * doAAlevel(int): anti-alising super sampling level
        
    Method Instruction:

    * Interrupt_MouseL(R): Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
    * Interrupt_Keyboard: Used to deal with key board press interruption. Use this to add new keys or new methods
    * drawPoint: method to draw a point
    * drawLine: method to draw a line
    * drawTriangle: method to draw a triangle with filling and smoothing
    
    List of methods to override the ones in CanvasBase:

    * Interrupt_MouseL
    * Interrupt_MouseR
    * Interrupt_Keyboard
        
    Here are some public variables in parent class you might need:

    * points_r: list<Point>. to store all Points from Mouse Right Button
    * points_l: list<Point>. to store all Points from Mouse Left Button
    * buff    : Buff. buff of current frame. Change on it will change display on screen
    * buff_last: Buff. Last frame buffer
        
    """

    debug = 0
    texture_file_path = "./pattern.jpg"
    texture = None

    # control flags
    randomColor = False
    doTexture = False
    doSmooth = False
    doAA = False
    doAAlevel = 4

    # test case status
    MIN_N_STEPS = 6
    MAX_N_STEPS = 192
    n_steps = 12  # For test case only
    test_case_index = 0
    test_case_list = []  # If you need more test case, write them as a method and add it to list

    def __init__(self, parent):
        """
        Initialize the instance, load texture file to Buff, and load test cases.

        :param parent: wxpython frame
        :type parent: wx.Frame
        """
        super(Sketch, self).__init__(parent)
        self.test_case_list = [lambda _: self.clear(),
                               self.testCaseLine01,
                               self.testCaseLine02,
                               self.testCaseTri01,
                               self.testCaseTri02,
                               self.testCaseTriTexture01]  # method at here must accept one argument, n_steps
        # Try to read texture file
        if os.path.isfile(self.texture_file_path):
            # Read image and make it to an ndarray
            texture_image = Image.open(self.texture_file_path)
            texture_array = np.array(texture_image).astype(np.uint8)
            # Because imported image is upside down, reverse it
            texture_array = np.flip(texture_array, axis=0)
            # Store texture image in our Buff format
            self.texture = Buff(texture_array.shape[1], texture_array.shape[0])
            self.texture.setStaticBuffArray(np.transpose(texture_array, (1, 0, 2)))
            if self.debug > 0:
                print("Texture Loaded with shape: ", texture_array.shape)
                print("Texture Buff have size: ", self.texture.size)
        else:
            raise ImportError("Cannot import texture file")

    def __addPoint2Pointlist(self, pointlist, x, y):
        if self.randomColor:
            p = Point((x, y), ColorType(random.random(), random.random(), random.random()))
        else:
            p = Point((x, y), ColorType(1, 0, 0))
        pointlist.append(p)

    # Deal with Mouse Left Button Pressed Interruption
    def Interrupt_MouseL(self, x, y):
        self.__addPoint2Pointlist(self.points_l, x, y)
        # Draw a point when one point provided or a line when two ends provided
        if len(self.points_l) % 2 == 1:
            if self.debug > 0:
                print("draw a point", self.points_l[-1])
            self.drawPoint(self.buff, self.points_l[-1])
        elif len(self.points_l) % 2 == 0 and len(self.points_l) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_l[-1], " -> ", self.points_l[-2])
            # TODO 0: uncomment this and comment out drawPoint when you finished the drawLine function 
            self.drawLine(self.buff, self.points_l[-2], self.points_l[-1], self.doSmooth, self.doAA, self.doAAlevel)
            # self.drawPoint(self.buff, self.points_l[-1]) 
            # drawRectangle for lab 1, comment it out and use drawLine when done with drawLine func
            # self.drawRectangle(self.buff, self.points_l[-2], self.points_l[-1])
            self.points_l.clear()

    # Deal with Mouse Right Button Pressed Interruption
    def Interrupt_MouseR(self, x, y):
        self.__addPoint2Pointlist(self.points_r, x, y)
        if len(self.points_r) % 3 == 1:
            if self.debug > 0:
                print("draw a point", self.points_r[-1])
            self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 2:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            # TODO 0: uncomment this and comment out drawPoint when you finished the drawLine function 
            self.drawLine(self.buff, self.points_r[-2], self.points_r[-1], self.doSmooth, self.doAA, self.doAAlevel)
            #self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 0 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a triangle {} -> {} -> {}".format(self.points_r[-3], self.points_r[-2], self.points_r[-1]))
            # TODO 0: uncomment drawTriangle and comment out drawPoint when you finished the drawTriangle function 
            self.drawTriangle(self.buff, self.points_r[-3], self.points_r[-2], self.points_r[-1], self.doSmooth, self.doAA, self.doAAlevel, self.doTexture)
            #self.drawPoint(self.buff, self.points_r[-1])
            self.points_r.clear()

    def Interrupt_Keyboard(self, keycode):
        """
        keycode Reference: https://docs.wxpython.org/wx.KeyCode.enumeration.html#wx-keycode

        * r, R: Generate Random Color point
        * c, C: clear buff and screen
        * LEFT, UP: Last Test case
        * t, T, RIGHT, DOWN: Next Test case
        """
        # Trigger for test cases
        if keycode in [wx.WXK_LEFT, wx.WXK_UP]:  # Last Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index - 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if keycode in [ord("t"), ord("T"), wx.WXK_RIGHT, wx.WXK_DOWN]:  # Next Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index + 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ",<":
            self.clear()
            self.n_steps = max(self.MIN_N_STEPS, round(self.n_steps / 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ".>":
            self.clear()
            self.n_steps = min(self.MAX_N_STEPS, round(self.n_steps * 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)

        # Switches
        if chr(keycode) in "rR":
            self.randomColor = not self.randomColor
            print("Random Color: ", self.randomColor)
        if chr(keycode) in "cC":
            self.clear()
            print("clear Buff")
        if chr(keycode) in "sS":
            self.doSmooth = not self.doSmooth
            print("Do Smooth: ", self.doSmooth)
        if chr(keycode) in "aA":
            self.doAA = not self.doAA
            print("Do Anti-Aliasing: ", self.doAA)
        if chr(keycode) in "mM":
            self.doTexture = not self.doTexture
            print("texture mapping: ", self.doTexture)

    def queryTextureBuffPoint(self, texture: Buff, x: int, y: int) -> Point:
        """
        Query a point at texture buff, should only be used in texture buff query

        :param texture: The texture buff you want to query from
        :type texture: Buff
        :param x: The query point x coordinate
        :type x: int
        :param y: The query point y coordinate
        :type y: int
        :rtype: Point
        """
        if self.debug > 1:
            if x != min(max(0, int(x)), texture.width - 1):
                print("Warning: Texture Query x coordinate outbound")
            if y != min(max(0, int(y)), texture.height - 1):
                print("Warning: Texture Query y coordinate outbound")
        return texture.getPointFromPointArray(x, y)

    @staticmethod
    def drawPoint(buff, point):
        """
        Draw a point on buff

        :param buff: The buff to draw point on
        :type buff: Buff
        :param point: A point to draw on buff
        :type point: Point
        :rtype: None
        """
        x, y = point.coords
        c = point.color
        # because we have already specified buff.buff has data type uint8, type conversion will be done in numpy
        buff.buff[x, y, 0] = c.r * 255
        buff.buff[x, y, 1] = c.g * 255
        buff.buff[x, y, 2] = c.b * 255

    def drawLine(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        """
        Draw a line between p1 and p2 on buff

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: One end point of the line
        :type p1: Point
        :param p2: Another end point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :rtype: None
        """
        ##### TODO 1: Use Bresenham algorithm to draw a line between p1 and p2 on buff.
        # Requirements:
        #   1. Only integer is allowed in interpolate point coordinates between p1 and p2
        #   2. Float number is allowed in interpolate point color

        x1, y1 = p1.coords
        x2, y2 = p2.coords
        
        # difference in x and y values, aka slope
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        # for determing the direction of the line
        sx, sy = 0, 0
        # positive means go x1 is "behind" x2, negative is the opposite
        if x1 < x2: 
            sx = 1
        if x1 > x2:
            sx = -1
        # positive means y1 lower, negative means y2 lower
        if y1 < y2:
            sy = 1
        if y1 > y2:
            sy= -1
        prev_p = 0
        # negative slope has a slightly different decision parameter
        if dx > dy: # base case/p0 for decision parameter
            # negative slope has a slightly different decision parameter
            if sy==-1:
                prev_p = (dx) - (2*dy)
            else:
                prev_p = (2*dy) - (dx)
        else:
            if sy==-1:
                prev_p = (dy) - (2*dx)
            else:
                prev_p = (2*dx) - (dy)
        #print(sx, sy, p1.coords, p2.coords)
        #base case for decision parameter
        # inc factor essentially checks if x or y value should be changed based on the decision paramter
        # which one to change(x or y) depends on the slope
        # 0 means no change(keep yk), 1 means change( y(k+1))
        inc_factor = 0
        if sy == -1:
            if prev_p > 0:
                inc_factor = 0
            else:
                inc_factor = 1
        else:
            if prev_p > 0:
                inc_factor = 1
        steps = max(dx, dy) 
        # checking if double clicked same point
        if p1 == p2:
            self.drawPoint(buff, p1)
        else:
            for i in range(steps + 1):
                t = i / steps  
                color = p1.color
                #smoothing out/interpolating will gradually transform the line from first dot color to second dot color
                # based on how far along are we in the making of the line
                if doSmooth:
                    color_r = p1.color.r * (1 - t) + p2.color.r * t
                    color_g = p1.color.g * (1 - t) + p2.color.g * t
                    color_b = p1.color.b * (1 - t) + p2.color.b * t
                    color = ColorType(color_r, color_g, color_b)
                # a line is just a lot of points so drawPoint works fine
                #print(x1, y1)
                self.drawPoint(buff, Point((x1,y1), color))
                # Bresenham's Algorithm
                if dx == dy: # slope is 1, which means x and y both change by 1 for every new pixel
                    x1 += sx
                    y1 += sy
                elif dx == 0: # vertical line
                    y1 += sy
                elif dy == 0: # horizontal line
                    x1 += sx
                elif dx > dy: # abs(m) or abs(dy/dx) would be less than one, meaning each column contains a pixel
                # x coord always changes by 1, y coord will depend on decision parameter
                    x1 += sx
                    curr_p = prev_p
                    if sy == -1:
                        # negative slope has the inequality reversed as the whole thing is multipled by -1
                        curr_p = curr_p - (2*dy) + (2*dx*(inc_factor))
                        if curr_p > 0: # greater than 0 would mean we stay, less means we go
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            y1 += sy
                    else:
                        curr_p = curr_p + (2*dy) - (2*dx*(inc_factor))
                        if curr_p < 0:
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            y1 += sy
                    prev_p = curr_p
                else: # dx slope is > 1, which means each row would contain a pixel
                    #y coord will always change, x is based on decision
                    y1 += sy
                    curr_p = prev_p
                    if sy == -1:
                        curr_p = curr_p - (2*dx) + (2*dy*(inc_factor))
                        if curr_p > 0:
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            x1 += sx
                    else:
                        curr_p = curr_p + (2*dx) - (2*dy*(inc_factor))
                        if curr_p < 0:
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            x1 += sx
                    prev_p = curr_p
    def drawTriangle(self, buff, p1, p2, p3, doSmooth=True, doAA=False, doAAlevel=4, doTexture=False):
        """
        draw Triangle to buff. apply smooth color filling if doSmooth set to true, otherwise fill with first point color
        if doAA is true, apply anti-aliasing to triangle based on doAAlevel given.

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: First triangle vertex
        :param p2: Second triangle vertex
        :param p3: Third triangle vertex
        :type p1: Point
        :type p2: Point
        :type p3: Point
        :param doSmooth: Color smooth filling control flag
        :type doSmooth: bool
        :param doAA: Anti-aliasing control flag
        :type doAA: bool
        :param doAAlevel: Anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :rtype: None
        """
        ##### TODO 2: Write a triangle rendering function, which support smooth bilinear interpolation of the vertex color
        ##### TODO 3(For CS680 Students): Implement texture-mapped fill of triangle. Texture is stored in self.texture
        # Requirements:
        #   1. For flat shading of the triangle, use the first vertex color.
        #   2. Polygon scan fill algorithm and the use of barycentric coordinate are not allowed in this function
        #   3. You should be able to support both flat shading and smooth shading, which is controlled by doSmooth
        #   4. For texture-mapped fill of triangles, it should be controlled by doTexture flag.

        # draws out the outline of the triangle
        self.drawLine(buff, p1, p3, doSmooth, doAA, doAAlevel)
        self.drawLine(buff, p2, p3, doSmooth, doAA, doAAlevel)
        default_color = p1.color # when random color not needed
        # for storing all the points on the outline of the triangle
        points_dict = {}

        # repeat of drawLine(), but modified to get the points of the outine instead of drawing them out again
        # essentially 1st part of bilinear interpolation
        def getPoints(v1, v2, doSmooth, doAA, doAAlevel):
            x1, y1 = v1.coords
            x2, y2 = v2.coords
            # difference in x and y values, aka slope
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            # for determing the direction of the line
            sx, sy = 0, 0
            # positive means go x1 is "behind" x2, negative is the opposite
            if x1 < x2:
                sx = 1
            else:
                sx = -1
            # positive means y1 lower, negative means y2 lower
            if y1 < y2:
                sy = 1
            else:
                sy= -1
            prev_p = 0
            if dx > dy: # base case/p0 for decision parameter
                # negative slope has a slightly different decision parameter
                if sy==-1:
                    prev_p = (dx) - (2*dy)
                else:
                    prev_p = (2*dy) - (dx)
            else:
                if sy==-1:
                    prev_p = (dy) - (2*dx)
                else:
                    prev_p = (2*dx) - (dy)
            #base case for decision parameter
            # inc factor essentially checks if x or y value should be changed based on the decision paramter
            # which one to change(x or y) depends on the slope
            # 0 means no change(keep yk), 1 means change(use y(k)+1)
            inc_factor = 0
            if sy == -1:
                if prev_p > 0:
                    inc_factor = 0
                else:
                    inc_factor = 1
            else:
                if prev_p > 0:
                    inc_factor = 1
            steps = max(dx, dy) 
            # print("steps ", steps)
            #print(p1.color.r, p2.color.r)
            for i in range(steps + 1):
                t = i / steps  
                color = default_color
                #smoothing out/interpolating will gradually transform the line from first dot color to second dot color
                # based on how far along are we in the making of the line
                if doSmooth:
                    color_r = v1.color.r * (1 - t) + v2.color.r * t
                    color_g = v1.color.g * (1 - t) + v2.color.g * t
                    color_b = v1.color.b * (1 - t) + v2.color.b * t
                    color = ColorType(color_r, color_g, color_b)
                # adding points to the dict
                if points_dict.get(y1) is None: #no points at the y value just yet
                    points_dict[y1] = [(x1, color)]
                    # points_dict[y1] = {x1: color}
                else:
                    points_dict[y1] += [(x1, color)]
                # Bresenham's Algorithm
                if dx == dy: # slope is 1, which means x and y both change by 1 for every new pixel
                    x1 += sx
                    y1 += sy
                elif dx == 0: # vertical line
                    y1 += sy
                elif dy == 0: # horizontal line
                    x1 += sx
                elif dx > dy: # abs(m) or abs(dy/dx) would be less than one, meaning each column contains a pixel
                # x coord always changes by 1, y coord will depend on decision parameter
                    x1 += sx
                    curr_p = prev_p
                    if sy == -1:
                        curr_p = curr_p - (2*dy) + (2*dx*(inc_factor))
                        if curr_p > 0:
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            y1 += sy
                    else:
                        curr_p = curr_p + (2*dy) - (2*dx*(inc_factor))
                        if curr_p < 0:
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            y1 += sy
                    prev_p = curr_p
                else: # dx slope is > 1, which means each row would contain a pixel
                    #y coord will always change, x is based on decision
                    y1 += sy
                    curr_p = prev_p
                    if sy == -1:
                        curr_p = curr_p - (2*dx) + (2*dy*(inc_factor))
                        if curr_p > 0:
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            x1 += sx
                    else:
                        curr_p = curr_p + (2*dx) - (2*dy*(inc_factor))
                        if curr_p < 0:
                            inc_factor = 0
                        else:
                            inc_factor = 1
                            x1 += sx
                    prev_p = curr_p
        # gathering all the points of the outline of the triangle
        getPoints(p1, p2, doSmooth, doAA, doAAlevel)
        getPoints(p1, p3, doSmooth, doAA, doAAlevel)
        getPoints(p2, p3, doSmooth, doAA, doAAlevel)
        # process all points and fill out the triangle row by row
        # part 2 of bilinear interpolation
        for y in points_dict:
            if len(points_dict[y]) >= 2:
                # takes only the furthest points on the row, to ensure whole row filled
                sorted_points = sorted(points_dict[y], key=lambda x: x[0])
                min_point = Point((sorted_points[0][0], y), sorted_points[0][1])
                max_point = Point((sorted_points[-1][0], y), sorted_points[-1][1])
                if min_point.coords != max_point.coords: # occasional duplicates can pop up
                    self.drawLine(buff, min_point, max_point, doSmooth, doAA, doAAlevel)
    # drawRectangle for lab 1
    def drawRectangle(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        x1, y1 = p1.coords
        x2, y2 = p2.coords
        for x in range(min(x1, x2), max(x1, x2)+1):
            for y in range(min(y1, y2), max(y1, y2)+1):
                self.drawPoint(buff, Point((x,y), p1.color))
    # test for lines lines in all directions
    def testCaseLine01(self, n_steps):
        center_x = int(self.buff.width / 2)
        center_y = int(self.buff.height / 2)
        radius = int(min(self.buff.width, self.buff.height) * 0.45)

        v0 = Point([center_x, center_y], ColorType(1, 1, 0))
        for step in range(0, n_steps):
            theta = math.pi * step / n_steps
            v1 = Point([center_x + int(math.sin(theta) * radius), center_y + int(math.cos(theta) * radius)],
                       ColorType(0, 0, (1 - step / n_steps)))
            v2 = Point([center_x - int(math.sin(theta) * radius), center_y - int(math.cos(theta) * radius)],
                       ColorType(0, (1 - step / n_steps), 0))
            self.drawLine(self.buff, v2, v0, doSmooth=True)
            self.drawLine(self.buff, v0, v1, doSmooth=True)

    # test for lines: drawing circle and petal 
    def testCaseLine02(self, n_steps):
        n_steps = 2 * n_steps
        d_theta = 2 * math.pi / n_steps
        d_petal = 12 * math.pi / n_steps
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        radius = (0.75 * min(cx, cy))
        p = radius * 0.25

        # Outer petals
        for i in range(n_steps + 2):
            self.drawLine(self.buff,
                          Point((math.floor(0.5 + radius * math.sin(d_theta * i) + p * math.sin(d_petal * i)) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * i) + p * math.cos(d_petal * i)) + cy),
                                ColorType(1, (128 + math.sin(d_theta * i * 5) * 127) / 255,
                                          (128 + math.cos(d_theta * i * 5) * 127) / 255)),
                          Point((math.floor(
                              0.5 + radius * math.sin(d_theta * (i + 1)) + p * math.sin(d_petal * (i + 1))) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * (i + 1)) + p * math.cos(
                                     d_petal * (i + 1))) + cy),
                                ColorType(1, (128 + math.sin(d_theta * 5 * (i + 1)) * 127) / 255,
                                          (128 + math.cos(d_theta * 5 * (i + 1)) * 127) / 255)),
                          doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

        # Draw circle
        for i in range(n_steps + 1):
            v0 = Point((math.floor(0.5 * radius * math.sin(d_theta * i)) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * i)) + cy), ColorType(1, 97. / 255, 0))
            v1 = Point((math.floor(0.5 * radius * math.sin(d_theta * (i + 1))) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * (i + 1))) + cy), ColorType(1, 97. / 255, 0))
            self.drawLine(self.buff, v0, v1, doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

    # test for smooth filling triangle
    def testCaseTri01(self, n_steps):
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v1, v0, v2, False, self.doAA, self.doAAlevel)

    def testCaseTri02(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v0, v1, v2, True, self.doAA, self.doAAlevel)

    def testCaseTriTexture01(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        triangleList = []
        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            triangleList.append([v0, v1, v2])

        for t in triangleList:
            self.drawTriangle(self.buff, *t, doTexture=True)


if __name__ == "__main__":
    def main():
        print("This is the main entry! ")
        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        canvas = Sketch(frame)
        canvas.debug = 0

        frame.Show()
        app.MainLoop()


    def codingDebug():
        """
        If you are still working on the assignment, we suggest to use this as the main call.
        There will be more strict type checking in this version, which might help in locating your bugs.
        """
        print("This is the debug entry! ")
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()

        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        canvas = Sketch(frame)
        canvas.debug = 2
        frame.Show()
        app.MainLoop()

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime').reverse_order()
        stats.print_stats()

    main()
    # codingDebug()
