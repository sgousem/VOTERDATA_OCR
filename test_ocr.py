from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
import os,glob,time
import numpy as np 
from PIL import Image
from cv2 import cv2
import io
from google.cloud import vision
import csv,re,sys
#from indictrans import Transliterator
from utils import stack_png_file,find_border,create_dir,convert_png_txt
#from google.cloud.vision import ImageAnnotatorClient
#from google.cloud.vision import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Administrator\\OCR\\Raylabsproject2019-0783fac75419.json"
client = vision.ImageAnnotatorClient() # pylint: disable=no-member
#trn = Transliterator(source='ben', target='eng', build_lookup=True)
#client = vision.ImageAnnotatorClient()
dists = ['Bongaigaon','Dhubri','Bilasipara West','Gauripur']
for ac in dists:
    #ac = sys.argv[1]
    ac_name = ac
    path = os.getcwd()
    os.chdir(os.path.join('pdf/{}'.format(ac)))
    path1 = os.getcwd()
    extension = 'pdf'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    for pdf_file in all_filenames:
        tos = time.time()
        #raw_text = []
        pbname = pdf_file.split('.')[0]
        try:
            pdf = PdfFileReader(open(pdf_file,'rb'))
            page_count = pdf.getNumPages()
            pages = convert_from_path(pdf_file, 300,first_page=3,last_page=page_count-1,poppler_path=r'C:\Users\Administrator\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin')
            os.chdir(os.path.join(path,'png'))
            create_dir(ac)
            os.chdir(os.path.join(ac))
            create_dir(pbname)
            os.chdir(os.path.join(pbname))
            #os.chdir(os.path.join(fname))
            for i,page in enumerate(pages):
                png_file = '{}_{}.png'.format(pbname,i)
                text_file = '{}.txt'.format(pbname)
                page.save(png_file, 'PNG')
                coords = find_border(png_file)
                stack_png_file(png_file,coords[0])
                text = convert_png_txt(png_file)
                #raw_text.append(text)
                with open(text_file, 'a',encoding='utf-8') as f:
                    f.write(text)
                    f.close
            #convert_txt_csv(text,pbname,ac_name)
            extension = 'png'
            all_pngnames = [i for i in glob.glob('*.{}'.format(extension))]
            for file_name1 in all_pngnames:
                os.remove(file_name1)
            toc = time.time()
            ptime = round(((toc-tos)/60),2)
            os.chdir(path1)
            print('pdftotxt conversion of pdf {} completed in {}'.format(pbname,ptime))
        except PyPDF2.utils.PdfReadError:
            os.chdir(path1)
            print('pdftotxt conversion of pdf {} not completed'.format(pbname))
    os.chdir(path)
    #extension = 'png'
    #all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


