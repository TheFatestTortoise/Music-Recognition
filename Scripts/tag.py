# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:22:32 2023

@author: Mason

THIS CODE MUST BE RUN FROM COMMAND LINE OR IT WILL BREAK DO NOT RUN IN SPYDER
"""
import cv2
import os
import copy
import numpy as np
import imutils
import pygetwindow as gw
import argparse

global img
global stored_img
global rects
global USER_PARAMS
global change
global more_info
global c_select
global R_N    
'''
User Parameters:
    Change based on machine properties and taste (Screen Resolution, Click Leeway, Running Interface)
    Should work for most modern machines except the window_title
    which will change based on where it's being run from
    
    Windows Default: Command Prompt
    
Dirs:
    Change based on filesystem, should be fairly plug and play
    
WaitkeyEx:
    The only one that is likely to change from machine to machine is arrowkeys
    If you are ok not using arrowkeys if they dont work then there is no need
    to change these.
    
    The other keycodes are ascii so they should remain constant between systems
'''
USER_PARAMS = {}
#USER PARAMETERS
USER_PARAMS['MOVE_SPEED'] = 3
USER_PARAMS['OFFSET_CLICK'] = 6
USER_PARAMS['DEFAULT_SHAPE'] = (20, 20)
USER_PARAMS['VIEWABLE_SHAPE'] = (1500, 800)
USER_PARAMS['WINDOW_TITLE'] = 'Anaconda Powershell Prompt'

#Dirs
USER_PARAMS['root'] = os.path.dirname(os.getcwd())
USER_PARAMS['dataset'] = os.path.join(USER_PARAMS['root'], "Staff_Dataset")
USER_PARAMS['imagedir'] = os.path.join(USER_PARAMS['dataset'], 'PreProcess')
USER_PARAMS['savedir'] = os.path.join(USER_PARAMS['dataset'], r'labels\un_split')

#waitKeyEx() Codes
USER_PARAMS['up_arrow'] = 2490368
USER_PARAMS['down_arrow'] = 2621440
USER_PARAMS['left_arrow'] = 2424832
USER_PARAMS['right_arrow'] = 2555904
USER_PARAMS['esc'] = 27
USER_PARAMS['q'] = 113
USER_PARAMS['i'] = 105
USER_PARAMS['r'] = 114
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
All 15 classIDs can easily be calculated (Natural has no corresponding characteristic)
(R_N + 1) * class_select = ClassIDs
'''
#Machine -> Human conversion for easy checking of results
R_N_cipher = ['Rest', 'Note']
notes = ['Natural', 'Whole Rest', '1/2 Rest', '1/4 Rest', '1/8 Rest', '1/16 Rest', 'Flat', 'Bass Clef',
         'Whole Note', '1/2 Note', '1/4 Note', '1/8 Note', '1/16 Note', 'Sharp', 'Treble Clef']

#Rest = False, Notes = True
#Event Flags / Parameters
R_N = False
c_select = 0
more_info = False
change = 'None'

#Cached Values for handling rect deletion and export
rects = []

#Makes storing ROIs cleaner and easier
class ROI:
    def __init__(self, pt1, pt2, classNUM):
        self.classID = classNUM
        self.pt1 = pt1
        self.pt2 = pt2
        self.calculate_properties()
    def print_info(self):
        self.calculate_properties()
        print('\n ________',
              '\n|  Class |', self.classID,
              '\n| Point1 |', self.pt1,
              '\n| Point2 |', self.pt2,
              '\n|   W    |', self.w,
              '\n|   H    |', self.h,
              '\n|  X_C   |', self.x_center,
              '\n|  Y_C   |', self.y_center,
              '\n ¯¯¯¯¯¯¯¯')
    def calculate_properties(self):
        try:
            self.w = abs(self._x2 - self._x1)
            self.h = abs(self._y2 - self._y1)
            self.x_center = int((self._x2 + self._x1)//2)
            self.y_center = int((self._y2 + self._y1)//2)
        except:
            print('Property calculation unsucessful, missing value')
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
    global USER_PARAMS
    global change
    global more_info
    global c_select
    global R_N    
    h, w, l = stored_img.shape
    prev_x, prev_y = USER_PARAMS['DEFAULT_SHAPE'] if len(rects) < 1 else (abs(rects[-1].x1 - rects[-1].x2), abs(rects[-1].y1 - rects[-1].y2))
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
        if x1 + USER_PARAMS['OFFSET_CLICK'] < x < x2 - USER_PARAMS['OFFSET_CLICK'] and y1 - USER_PARAMS['OFFSET_CLICK'] < y < y1 + USER_PARAMS['OFFSET_CLICK']:
            change = 'TOP'
        elif x1 + USER_PARAMS['OFFSET_CLICK'] < x < x2 - USER_PARAMS['OFFSET_CLICK'] and y2 - USER_PARAMS['OFFSET_CLICK'] < y < y2 + USER_PARAMS['OFFSET_CLICK']:
            change = 'BOT'
        #L/R
        elif x1 - USER_PARAMS['OFFSET_CLICK'] < x < x1 + USER_PARAMS['OFFSET_CLICK'] and y1 + USER_PARAMS['OFFSET_CLICK'] < y < y2 - USER_PARAMS['OFFSET_CLICK']:
            change = 'LEF'
        elif x2 - USER_PARAMS['OFFSET_CLICK'] < x < x2 + USER_PARAMS['OFFSET_CLICK'] and y1 + USER_PARAMS['OFFSET_CLICK'] < y < y2 - USER_PARAMS['OFFSET_CLICK']:
            change = 'RIG'
        #Corners
        elif x1 - USER_PARAMS['OFFSET_CLICK'] <= x <= x1 + USER_PARAMS['OFFSET_CLICK'] and y1 - USER_PARAMS['OFFSET_CLICK'] <= y <= y1 + USER_PARAMS['OFFSET_CLICK']:
            change = "TOP_LEF"
        elif x2 - USER_PARAMS['OFFSET_CLICK'] <= x <= x2 + USER_PARAMS['OFFSET_CLICK'] and y1 - USER_PARAMS['OFFSET_CLICK'] <= y <= y1 + USER_PARAMS['OFFSET_CLICK']:
            change = "TOP_RIG"
        elif x1 - USER_PARAMS['OFFSET_CLICK'] <= x <= x1 + USER_PARAMS['OFFSET_CLICK'] and y2 - USER_PARAMS['OFFSET_CLICK'] <= y <= y2 + USER_PARAMS['OFFSET_CLICK']:
            change = "BOT_LEF"  
        elif x2 - USER_PARAMS['OFFSET_CLICK'] <= x <= x2 + USER_PARAMS['OFFSET_CLICK'] and y2 - USER_PARAMS['OFFSET_CLICK'] <= y <= y2 + USER_PARAMS['OFFSET_CLICK']:
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





cmd_window = gw.getWindowsWithTitle(USER_PARAMS['WINDOW_TITLE'])
parser = argparse.ArgumentParser(description = "Use **kwargs to change dirs and runtime properties")
r'''
#USER PARAMETERS
MOVE_SPEED = 3
OFFSET_CLICK = 6
DEFAULT_SHAPE = (20, 20)
VIEWABLE_SHAPE = (1500, 800)
window_title = 'Anaconda Powershell Prompt'

#Dirs
root = os.path.dirname(os.getcwd())
dataset = os.path.join(root, "Staff_Dataset")
imagedir = os.path.join(dataset, 'PreProcess')
savedir = os.path.join(dataset, r'labels\un_split')

#waitKeyEx() Codes
up_arrow = 2490368
down_arrow = 2621440
left_arrow = 2424832
right_arrow = 2555904
esc = 27
key_q = 113
key_i = 105
key_r = 114
'''
parser.add_argument('--MOVE_SPEED', type=int)
parser.add_argument('--OFFSET_CLICK', type=int)
parser.add_argument('--DEFAULT_SHAPE', type=tuple)
parser.add_argument('--VIEWABLE_SHAPE', type=tuple)
parser.add_argument('--WINDOW_TITLE', type=str)

args = vars(parser.parse_args())

for kwarg in args:
    if args[kwarg]:
        print(USER_PARAMS[kwarg])
        USER_PARAMS[kwarg] = args[kwarg]
        print(USER_PARAMS[kwarg])


for image in os.listdir(USER_PARAMS['imagedir']):
    cor_txt = image.replace('png', 'txt')
    filename = os.path.join(USER_PARAMS['savedir'], cor_txt)
    if not os.path.isfile(filename):

        imagename = os.path.join(USER_PARAMS['imagedir'], image)
        img = cv2.imread(imagename)
        
        h, w, l = img.shape
        print('\n    IMAGE INFO',
              '\n| Image N |', image,
              '\n| Image W |', w,
              '\n| Image H |', h,
              '\n ¯¯¯¯¯¯¯¯¯')
        if np.argmax((w, h)) == 0:
            img = imutils.resize(img, width = USER_PARAMS['VIEWABLE_SHAPE'][0])
        else:
            img = imutils.resize(img, width = USER_PARAMS['VIEWABLE_SHAPE'][0])

        h, w, l = img.shape
        print('\n   RESIZED IMAGE',
              '\n| Image N |', image,
              '\n| Image W |', w,
              '\n| Image H |', h,
              '\n ¯¯¯¯¯¯¯¯¯')

        stored_img = img
        base_img = copy.deepcopy(img)
        
        cv2.imshow('img', img)
        cv2.setMouseCallback('img', mouse_clicks)
        k = cv2.waitKey(0)
        
        #q/ESC
        while k != USER_PARAMS['q'] and k != USER_PARAMS['esc']:
            k = cv2.waitKeyEx(0)
            if k == USER_PARAMS['i'] and rects:
                if not more_info:
                    print('\n _________'
                          '\n|Current R|', (R_N + 1),
                          '\n|Current S|', c_select,
                          '\n|Current N|', notes[c_select * (R_N + 1)],
                          '\n ¯¯¯¯¯¯¯¯¯')
                    rects[-1].print_info()
                    more_info = True
                else:
                    more_info = False
                    os.system('cls')
                    cmd_window[0].activate()
                    count = 0
                    print(' BOX INFO FOR', image)
                    for box in rects:
                        print('      BOX', count)
                        box.print_info()
                        count += 1
                    x = input('COMMAND: ')
                    if "del" in x:
                        split_in = x.split(' ')
                        
                        try:
                            rects.pop(int(split_in[-1]))
                            print('Box', split_in[-1], 'succesfully deleted')
                            img = copy.deepcopy(base_img)
                            
                            for box in rects:
                                cv2.rectangle(img, box.pt1, box.pt2, (0, 255, 0), 1)
                            cv2.imshow('img', img)
                            stored_img = copy.deepcopy(img)
                        except:
                            print('Invalid Box Deletion:', split_in[-1], 'is not a valid delete target')
                        
            #Arrow key box sliding
            elif k == USER_PARAMS['up_arrow']:
                img = copy.deepcopy(stored_img)
                rects[-1].y1 = rects[-1].y1 - USER_PARAMS['MOVE_SPEED']
                rects[-1].y2 = rects[-1].y2 - USER_PARAMS['MOVE_SPEED']
                
                cv2.rectangle(img, rects[-1].pt1, rects[-1].pt2, (0, 0, 255), 1)
                cv2.imshow('img', img)
                change = 'None'
            elif k == USER_PARAMS['down_arrow']:
                img = copy.deepcopy(stored_img)
                rects[-1].y1 = rects[-1].y1 + USER_PARAMS['MOVE_SPEED']
                rects[-1].y2 = rects[-1].y2 + USER_PARAMS['MOVE_SPEED']
                
                cv2.rectangle(img, rects[-1].pt1, rects[-1].pt2, (0, 0, 255), 1)
                cv2.imshow('img', img)
                change = 'None'
            elif k == USER_PARAMS['left_arrow']:
                img = copy.deepcopy(stored_img)
                rects[-1].x1 = rects[-1].x1 - USER_PARAMS['MOVE_SPEED']
                rects[-1].x2 = rects[-1].x2 - USER_PARAMS['MOVE_SPEED']
                
                cv2.rectangle(img, rects[-1].pt1, rects[-1].pt2, (0, 0, 255), 1)
                cv2.imshow('img', img)
                change = 'None'
            elif k == USER_PARAMS['right_arrow']:
                img = copy.deepcopy(stored_img)
                rects[-1].x1 = rects[-1].x1 + USER_PARAMS['MOVE_SPEED']
                rects[-1].x2 = rects[-1].x2 + USER_PARAMS['MOVE_SPEED']
                
                cv2.rectangle(img, rects[-1].pt1, rects[-1].pt2, (0, 0, 255), 1)
                cv2.imshow('img', img)
                change = 'None'
            elif k == USER_PARAMS['r']:
                R_N = not R_N
                
                print('\n| R_N |', R_N_cipher[R_N])
                more_info = False
            #number change class
            elif k <= 55 and k >= 48:
                c_select = k - 48
                more_info = False
        
        if k == USER_PARAMS['q']:
            count = 0
            print('\n BOX INFO FOR', image)
            if os.path.isdir(USER_PARAMS['savedir']):   
                with open(filename, 'w') as f:
                    for box in rects:
                        print('      BOX', count)
                        box.print_info()
                        count += 1
                        cor_txt = image.replace('png', 'txt')
                        if count < len(rects):
                            f.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(box.classID, box.x_center/w, box.y_center/h, box.w/w, box.h/h) + "\n")    
                        else:
                            f.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(box.classID, box.x_center/w, box.y_center/h, box.w/w, box.h/h))
        if k == USER_PARAMS['esc']:
            break
        cv2.destroyAllWindows()        
        rects = []
        more_info = False  
    else:
        print(image, 'Already Labeled')