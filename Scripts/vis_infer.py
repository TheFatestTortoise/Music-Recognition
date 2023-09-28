# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:22:32 2023

@author: Mason
"""

import cv2
import os
'''
filedir = r"F:\LAM\processed_data"
imagedir= r"F:\LAM\processed_img"
savedir = r"F:\LAM\LABELED_IMGS"
'''
root = os.path.dirname(os.getcwd())
dataset = os.path.join(root, "Notes_Dataset")
filedir = os.path.join(dataset, r'labels\train')
imagedir = os.path.join(dataset, r'images\train')

savedir = ''

for image in os.listdir(imagedir)[:100]:
    cor_txt = image.replace('png', 'txt')
    filename = os.path.join(filedir, cor_txt)
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            boxes = f.readlines()
            imagename = os.path.join(imagedir, image)
            img = cv2.imread(imagename)
            
            h, w, l = img.shape
            print(w, h)
            for box in boxes:
                if box != '':
                    class_id, x_center, y_center, width, height = box.split(' ')
                    
                    class_id = int(class_id)
                    x_center = float(x_center)
                    y_center = float(y_center)
                    width = float(width)
                    height = float(height)
                    
                    x1 = int((x_center - width / 2) * w)
                    x2 = int((x_center + width / 2) * w)
                    y1 = int((y_center - height / 2) * h)
                    y2 = int((y_center + height / 2) * h)
                    
                    print( x1, y1, x2, y2)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            if savedir != '':
                savename = os.path.join(savedir, image)
                cv2.imwrite(savename, img)
            else:
                cv2.imshow('img', img)
                k = cv2.waitKey(0)
                cv2.destroyAllWindows()
                if k == 27:
                    break
                
    else:
        print('No corresponding txt')