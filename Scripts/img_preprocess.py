# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 21:54:45 2023

@author: Mason
"""

import cv2
import numpy as np
import os
import imutils
import sys
page_dir = r"C:\Users\Mason\Desktop\Music Recognition\Staff_Dataset\Raw"
save_dir = r"C:\Users\Mason\Desktop\Music Recognition\Staff_Dataset\PreProcess"

for page in os.listdir(page_dir):
    page_path = os.path.join(page_dir, page)
    if os.path.isfile(page_path):
        scale_factor = 1
        img = cv2.imread(page_path,  cv2.IMREAD_GRAYSCALE)
        img = img
        
        h, w = img.shape
        
        
        #Shrinks image to a viewable size and displays for verification
        
        resized_img = imutils.resize(img, width = 980)
        
        blur = np.array([[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]])                                                                                    
        
        smoothed_img = cv2.filter2D(resized_img, -1, blur)
        binarized_img = cv2.adaptiveThreshold(resized_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 30)
        
        cv2.imshow('image', binarized_img)
        h, w = binarized_img.shape
        print(w, h)
        x = cv2.waitKey(0)
        if x == 32:
            savepath = os.path.join(save_dir, page)
            cv2.imwrite(savepath, binarized_img)
        
        elif x == 27:
            cv2.destroyAllWindows()
            sys.exit()
        cv2.destroyAllWindows()