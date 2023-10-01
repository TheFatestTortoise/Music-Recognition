# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:22:32 2023

@author: Mason
"""

import cv2
import os
import copy
global stored_img
global img
global change
global OFFSET_CLICK
global DEFAULT_SHAPE
global more_info
global classID
global R_N
global c_select

#Distance for clicks to render
OFFSET_CLICK = 10
DEFAULT_SHAPE = (20, 20)
'''
R_N:
    0 Rests
    1 Notes
Classes:
    0 Natural
    1 Whole
    2 Half
    3 Quarter
    4 Eigth
    5 Sixteenth
    6 Flat/Sharp
    7 Trebble/Bass
All 15 classIDs can easily be calculated
(R_N + 1) * class_select = ClassIDs
'''
notes = ['Natural', 'Whole Rest', '1/2 Rest', '1/4 Rest', '1/8 Rest', '1/16 Rest', 'Flat', 'Bass Clef',
         'Whole Note', '1/2 Note', '1/4 Note', '1/8 Note', '1/16 Note', 'Sharp', 'Treble Clef']
#Rest = False, Notes = True
R_N = False
c_select = 0

CLASS_ID = 0

more_info = False


#Dirs
root = os.path.dirname(os.getcwd())
dataset = os.path.join(root, "Notes_Dataset")
filedir = os.path.join(dataset, r'labels\train')
imagedir = os.path.join(dataset, r'images\train')
savedir = os.path.join(dataset, r'labels\un_split')

#Cached Values for handling rect deletion
rects = []

change = 'None'

class ROI:
    def __init__(self, pt1, pt2, classNUM):
        self.classID = classNUM
        self.pt1 = pt1
        self.pt2 = pt2
        self.calculate_properties()
    def print_info(self):
        self.calculate_properties()
        print('|  Class |', self.classID,
              '\n| Point1 |', self.pt1,
              '\n| Point2 |', self.pt2,
              '\n|   W    |', self.w,
              '\n|   H    |', self.h,
              '\n|  X_C   |', self.x_center,
              '\n|  Y_C   |', self.y_center)
    def calculate_properties(self):
        self.w = abs(self.x2 - self.x1)
        self.h = abs(self.y2 - self.y1)
        self.x_center = int((self.x2 + self.x1)//2)
        self.y_center = int((self.y2 + self.y1)//2)
        
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
        return(self._y1)
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
    
def mouse_clicks(event, x, y, flags, param):
    global img
    global stored_img
    global rects
    global OFFSET_CLICK
    global change
    global more_info
    global c_select
    global R_N    
    h, w, l = stored_img.shape
    prev_x, prev_y = DEFAULT_SHAPE if len(rects) < 1 else (abs(rects[-1].x1 - rects[-1].x2), abs(rects[-1].y1 - rects[-1].y2))
    if event == cv2.EVENT_LBUTTONDOWN:
        more_info = False
        if len(rects) > 0:
            img = stored_img
            cv2.rectangle(img, rects[-1].pt1, rects[-1].pt2, (0, 255, 0), 1)
        stored_img = copy.deepcopy(img)
        
        pt1 = (int(x - (prev_x//2)), int(y - (prev_y//2)))
        pt2 = (int(x + (prev_x//2)), int(y + (prev_y//2)))
        
        n_b = ROI(pt1, pt2, c_select * (R_N + 1))
        if n_b.x1 > 0 and n_b.x2 < w and n_b.y1 > 0 and n_b.y2 < h:
            cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)
            cv2.imshow('img', img)

            rects.append(n_b)
            n_b.print_info()
    elif event == cv2.EVENT_RBUTTONDOWN and len(rects) > 0:
        more_info = False
        x1 = rects[-1].x1
        x2 = rects[-1].x2
        y1 = rects[-1].y1
        y2 = rects[-1].y2

        #T/B
        if x1 + OFFSET_CLICK < x < x2 - OFFSET_CLICK and y1 - OFFSET_CLICK < y < y1 + OFFSET_CLICK:
            change = 'TOP'
        elif x1 + OFFSET_CLICK < x < x2 - OFFSET_CLICK and y2 - OFFSET_CLICK < y < y2 + OFFSET_CLICK:
            change = 'BOT'
        #L/R
        elif x1 - OFFSET_CLICK < x < x1 + OFFSET_CLICK and y1 + OFFSET_CLICK < y < y2 - OFFSET_CLICK:
            change = 'LEF'
        elif x2 - OFFSET_CLICK < x < x2 + OFFSET_CLICK and y1 + OFFSET_CLICK < y < y2 - OFFSET_CLICK:
            change = 'RIG'
        #Corners
        elif x1 - OFFSET_CLICK <= x <= x1 + OFFSET_CLICK and y1 - OFFSET_CLICK <= y <= y1 + OFFSET_CLICK:
            change = "TOP_LEF"
        elif x2 - OFFSET_CLICK <= x <= x2 + OFFSET_CLICK and y1 - OFFSET_CLICK <= y <= y1 + OFFSET_CLICK:
            change = "TOP_RIG"
        elif x1 - OFFSET_CLICK <= x <= x1 + OFFSET_CLICK and y2 - OFFSET_CLICK <= y <= y2 + OFFSET_CLICK:
            change = "BOT_LEF"  
        elif x2 - OFFSET_CLICK <= x <= x2 + OFFSET_CLICK and y2 - OFFSET_CLICK <= y <= y2 + OFFSET_CLICK:
            change = "BOT_RIG"  
    elif event == cv2.EVENT_RBUTTONUP:
        more_info = False
        img = copy.deepcopy(stored_img)
        pt1 = rects[-1].pt1
        pt2 = rects[-1].pt2
        x1, y1 = pt1
        x2, y2 = pt2
        if change == 'TOP' and y < y2:
            rects[-1].y1 = max(0, y)
        elif change == 'BOT' and y > y1:
            rects[-1].y2 = min(y, h)
        elif change == 'LEF' and x < x2:
            rects[-1].x1 = max(0, x)
        elif change == 'RIG' and x > x1:
            rects[-1].x2 = min(x, w)
        elif change == 'TOP_LEF' and all(i < j for i, j in zip((x, y), pt2)):
            rects[-1].pt1 = (max(0, x), max(0, y))
        elif change == 'TOP_RIG' and all(i < j for i, j in zip((x1, y), (x, y2))):
            rects[-1].y1 = max(0, y)
            rects[-1].x2 = min(x, w)
        elif change == 'BOT_LEF' and all(i < j for i, j in zip((x, y1), (x2, y))):
            rects[-1].y2 = min(y, h)
            rects[-1].x1 = max(0, x)
        elif change == 'BOT_RIG' and all(i < j for i, j in zip(pt1, (x, y))):
            rects[-1].pt2 = (min(x, w), min(y, h))
        
        cv2.rectangle(img, rects[-1].pt1, rects[-1].pt2, (0, 0, 255), 1)
        cv2.imshow('img', img)
        change = 'None'

for image in os.listdir(imagedir):
    cor_txt = image.replace('png', 'txt')
    filename = os.path.join(savedir, cor_txt)
    if not os.path.isfile(filename):

        imagename = os.path.join(imagedir, image)
        img = cv2.imread(imagename)
        
        h, w, l = img.shape
        print('\n| Image N |', image,
              '\n| Image W |', w,
              '\n| Image H |', h)
        
        if w > 1300 or h > 800:
            img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
            h, w, l = img.shape
            print('\nAdjusted Image Size')
            print('\n| Image N |', image,
                  '\n| Image W |', w,
                  '\n| Image H |', h)
        
        stored_img = img
        
        cv2.imshow('img', img)
        cv2.setMouseCallback('img', mouse_clicks)
        k = cv2.waitKey(0)

        #q/ESC
        while k != 113 and k != 27:
            k = cv2.waitKey(0)
            #i
            if k == 105 and len(rects) > 0:
                if not more_info:
                    print('\n|Current R|', (R_N + 1),
                          '\n|Current S|', c_select,
                          '\n|Current N|', notes[c_select * (R_N + 1)])
                    rects[-1].print_info()
                    more_info = True
                else:
                    more_info = False
                    os.system('cls')
                    count = 0
                    print(' BOX INFO FOR', image)
                    for box in rects:
                        print('      BOX', count)
                        box.print_info()
                        count += 1
            #r
            elif k == 114:
                print(R_N, not R_N)
                R_N = not R_N
                more_info = False
            #number change class
            elif k <= 55 and k >= 48:
                c_select = k - 48
                more_info = False
        #q
        if k == 113:
            count = 0
            print('\n BOX INFO FOR', image)
            if os.path.isdir(savedir):
                print(filename)
    
                with open(filename, 'w') as w:
                    for box in rects:
                        print('      BOX', count)
                        box.print_info()
                        count += 1
                        cor_txt = image.replace('png', 'txt')
                        if count < len(rects):
                            w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(box.classID, box.x_center, box.y_center, box.w, box.h) + "\n")    
                        else:
                            w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(box.classID, box.x_center, box.y_center, box.w, box.h))
            cv2.destroyAllWindows()
            rects = []
            more_info = False

            
        #Esc
        if k == 27:
            break
    else:
        print('No corresponding txt')