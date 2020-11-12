from cv2 import cv2
import numpy as np
import os,glob
def find_border(img_file):
    im1 = cv2.imread(img_file, 0)
    #iml = cv2.resize(iml,(0,0),fx=fx*0.6.fy = fy*0.6)
    im = cv2.imread(img_file)

    ret,thresh_value = cv2.threshold(im1,212,255,cv2.THRESH_BINARY_INV)

    kernel = np.ones((5,5),np.uint8)
    dilated_value = cv2.dilate(thresh_value,kernel,iterations = 1)

    contours, hierarchy = cv2.findContours(dilated_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(contours)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:2]
    cordinates = []
    #for cnt in cnts:
    x,y,w,h = cv2.boundingRect(cnts[0])
    if y>300 and h<2000 and len(cnts)==2:
        x1,y1,w1,h1 = cv2.boundingRect(cnts[1])
        space = y-h1
        #print(x,y1,w,h+h1+space)
        cordinates.append((x,y1,w,h+h1+space))
        #cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)
        #cv2.imwrite(img_file,im)
    else:
        #print(x,y,w,h)
        cordinates.append((x,y,w,h))
        #bounding the images
        #if y< 50:
        #cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)
        #cv2.imwrite(img_file,im)
    return cordinates
path = os.getcwd()
print(path)
os.chdir(os.path.join(path,'temp'))
extension = 'png'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
for img_file in all_filenames:
    print(img_file.split('.')[0])

    im1 = cv2.imread(img_file, 0)
    #iml = cv2.resize(iml,(0,0),fx=fx*0.6.fy = fy*0.6)
    im = cv2.imread(img_file)

    ret,thresh_value = cv2.threshold(im1,212,255,cv2.THRESH_BINARY_INV)

    kernel = np.ones((5,5),np.uint8)
    dilated_value = cv2.dilate(thresh_value,kernel,iterations = 1)

    contours, hierarchy = cv2.findContours(dilated_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(contours)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:2]
    cordinates = []
    #for cnt in cnts:
    x,y,w,h = cv2.boundingRect(cnts[0])
    if y>300 and h<2000 and len(cnts)==2:
        x1,y1,w1,h1 = cv2.boundingRect(cnts[1])
        space = y-h1
        print(x,y1,w,h+h1+space)
        cordinates.append((x,y1,w,h+h1+space))
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)
        cv2.imwrite(img_file,im)
    else:
        print(x,y,w,h)
        cordinates.append((x,y,w,h))
        #bounding the images
        #if y< 50:
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)
        cv2.imwrite(img_file,im)
os.chdir(path)
ahmed0101@gmail.com
