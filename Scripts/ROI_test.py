# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 11:10:40 2023

@author: Mason
"""

class ROI:
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        
        self.calculate_properties()
    def print_info(self):
        print(self.pt1, self.pt2, self.w, self.h, self.x_center, self.y_center)
    def calculate_properties(self):
        self.w = abs(self.x2 - self.x1)
        self.h = abs(self.y2 - self.y1)
        self.x_center = int(max(self.x2, self.x1) - (self.w)//2)
        self.y_center = int(max(self.y2, self.y1) - (self.h)//2)
        
    @property
    def x1(self):
        return(self._x1)
    
    @x1.setter
    def x1(self, x):
        self._x1 = x
    
    @property
    def x2(self):
        return(self._x2)
    
    @x2.setter
    def x2(self, x):
        self._x2 = x

    @property
    def y1(self):
        return(self._x1)
    @y1.setter
    def y1(self, y):
        self._y1 = y

    @property
    def y2(self):
        return(self._y2)
    
    @y2.setter
    def y2(self, y):
        self._y2 = y

    @property
    def pt1(self):
        return(self._x1, self._y1)
    
    @pt1.setter
    def pt1(self, pt1):
        self._x1, self._y1 = pt1
    
    @property
    def pt2(self):
        return(self._x2, self._y2)
    
    @pt2.setter
    def pt2(self, pt2):
        self._x2, self._y2 = pt2
    
pt1 = (10, 10)
pt2 = (100, 100)
new_box = ROI(pt1, pt2)
new_box.print_info()

new_box.x1 = 25
new_box.calculate_properties()
new_box.print_info()