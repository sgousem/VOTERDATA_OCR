from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
import os,glob,time
import subprocess
import numpy as np 
from PIL import Image
from cv2 import cv2
tos = time.time()
def create_dir(name):
    path = os.getcwd()
    os.chdir(os.path.join(path,'png'))
    try:
        os.mkdir(name)
    except FileExistsError:
        pass
    os.chdir(os.path.join(path,'stack_png'))
    try:
        os.mkdir(name)
    except FileExistsError:
        pass
    os.chdir(path)

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

def get_pad(h, w):
    pad0 = np.zeros((h, w), dtype=np.uint8)
    pad1 = np.ones((h, w), dtype=np.uint8) * 255
    pad = np.stack([pad1.T, pad0.T]).T
    return pad

def stack_png_file(file_path,coord):
    global pad 

    img = Image.open(file_path)
    x,y,w,h = coord
    f = w%3
    width = int((w-f)/3)
    #w = 706
    x1 = x
    x2 = x+width
    x3 = x+(width*2)

    #header = (100, 0, 850, 200)
    col1 = (x1, y, x1 + width, h+y)
    col2 = (x2, y, x2 + width, h+y)
    col3 = (x3, y, x3 + width, h+y)

    #img_header = img.crop((header))
    img_col1 = img.crop((col1))
    img_col2 = img.crop((col2))
    img_col3 = img.crop((col3))

    try:
        #simg = np.vstack((np.asarray(i) for i in [img_col1, img_col2, img_col3]))
        simg = np.vstack([img_col1, img_col2, img_col3])
        #img_body = np.hstack([simg, get_pad(simg.shape[0], img_header.size[0]-simg.shape[1])])
        #img = np.vstack([img_header, img_body])
        img = Image.fromarray(simg)
        img.save(file_path)
    except:
        pass
    
    return file_path
path = os.getcwd()
pdf_file = 'S03A15P5.pdf'
fname = pdf_file.split('.')[0]
pb_num = int(fname.split('P')[1])
create_dir(fname)
#os.path.join('pdf')
os.chdir(os.path.join(path,'pdf'))
pdf = PdfFileReader(open(pdf_file,'rb'))
page_count = pdf.getNumPages()
pages = convert_from_path(pdf_file, 300,first_page=3,last_page=page_count-1)
os.chdir(os.path.join(path,'png/{}'.format(fname)))
#os.chdir(os.path.join(fname))
tem_path = os.getcwd()
for i,page in enumerate(pages):
    page.save('{}_{}.png'.format(fname,i), 'PNG')
#stack_png_file('out.png')
extension = 'png'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#os.chdir(os.path.join(path,'png'))
for png_file in all_filenames:
    coord = find_border(png_file)
    #os.chdir(os.path.join(path,'stack_png/{}'.format(fname)))
    stack_png_file(png_file,coord[0])
    os.chdir(tem_path)
os.chdir(path)
print('png conversion completed')
toc = time.time()
print((toc-tos)/60)