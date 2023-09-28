# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:22:32 2023

@author: Mason
"""

import cv2
import os
import copy
global stored_img
global prev_size
global stored_rect
global img
global change
global OFFSET_CLICK

OFFSET_CLICK = 10
root = os.path.dirname(os.getcwd())
dataset = os.path.join(root, "Notes_Dataset")
filedir = os.path.join(dataset, r'labels\train')
imagedir = os.path.join(dataset, r'images\train')
stored_rect = (0, 0)
savedir = ''

prev_size = (100, 100)

change = 'None'
def mouse_clicks(event, x, y, flags, param):
    global img
    global stored_img
    global stored_rect
    global prev_size
    global OFFSET_CLICK
    global change
    h, w, l = stored_img.shape
    
    prev_x, prev_y = prev_size
    
    
    
    if event == cv2.EVENT_LBUTTONDOWN:
        stored_img = copy.deepcopy(img)
        pt1 = (int(x - (prev_x//2)), int(y - (prev_y//2)))
        pt2 = (int(x + (prev_x//2)), int(y + (prev_y//2)))
        stored_rect = (pt1, pt2)
        print(pt1, pt2)
        if all(x > 0 for x in pt1) and pt2 < (w, h):
            cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)
            cv2.imshow('img', img)
    elif event == cv2.EVENT_RBUTTONDOWN and stored_rect != (0, 0):
        pt1, pt2 = stored_rect

        #Means we are only looking at the T/B
        if x > pt1[0] + OFFSET_CLICK and x < pt2[0] - OFFSET_CLICK:
            if y > pt1[1] - OFFSET_CLICK and y < pt1[1] + OFFSET_CLICK:
                change = 'TOP'
            elif y > pt2[1] - OFFSET_CLICK and y < pt2[1] + OFFSET_CLICK:
                change = 'BOT'
        elif y > pt1[1] + OFFSET_CLICK and y < pt2[1] - OFFSET_CLICK:
            if x > pt1[0] - OFFSET_CLICK and x < pt1[0] + OFFSET_CLICK:
                change = 'LEF'
            elif x > pt2[0] - OFFSET_CLICK and x < pt2[0] + OFFSET_CLICK:
                change = 'RIG'
                    
    elif event == cv2.EVENT_RBUTTONUP:
        img = copy.deepcopy(stored_img)
        pt1, pt2 = stored_rect
        if change == 'TOP':
            print(y)
            x_pt = pt1[0]
            stored_rect = ((x_pt, y), pt2)
        elif change == 'BOT':
            print(y)
            x_pt = pt2[0]
            stored_rect = (pt1, (x_pt, y))
        elif change == 'LEF':
            print(y)
            y_pt = pt1[1]
            stored_rect = ((x, y_pt), pt2)
        elif change == 'RIG':
            print(y)
            y_pt = pt2[1]
            stored_rect = (pt1, (x, y_pt))
        
        cv2.rectangle(img, stored_rect[0], stored_rect[1], (0, 0, 255), 1)
        prev_size = (stored_rect[1][0] - stored_rect[0][0], stored_rect[1][1] - stored_rect[0][1])
        cv2.imshow('img', img)
        change = 'None'


for image in os.listdir(imagedir):
    cor_txt = image.replace('png', 'txt')
    filename = os.path.join(filedir, cor_txt)
    if not os.path.isfile(filename):

        imagename = os.path.join(imagedir, image)
        img = cv2.imread(imagename)
        
        h, w, l = img.shape
        print(w, h)
        stored_img = img
        prev_size = (w/10, h/10)
        
        if savedir != '':
            savename = os.path.join(savedir, image)
            cv2.imwrite(savename, img)
        else:
            cv2.imshow('img', img)
            cv2.setMouseCallback('img', mouse_clicks)
            k = cv2.waitKey(0)
            cv2.destroyAllWindows()
            if k == 27:
                break
                
    else:
        print('No corresponding txt')