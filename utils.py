from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
import os,glob,time
import numpy as np 
from PIL import Image
from cv2 import cv2
import io,re,csv
from google.cloud import vision
from indictrans import Transliterator
#from google.cloud.vision import ImageAnnotatorClient
#from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\USER\\Raylabsproject2019-0783fac75419.json"
client = vision.ImageAnnotatorClient() # pylint: disable=no-member
trn = Transliterator(source='ben', target='eng', build_lookup=True)
def convert_png_txt(png_file):
    fname = png_file.split('.')[0]
    text_file = '{}.txt'.format(fname)
    #client = vision.ImageAnnotatorClient()
    with open(text_file, 'w',encoding='utf-8') as _f:
        with io.open(png_file, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        image_context = vision.ImageContext(
            language_hints='as')

        response = client.document_text_detection(image=image,
                                                image_context=image_context)
        
        text = response.full_text_annotation.text
    
        _f.write(text)
    return text
def create_dir(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        pass
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
def pdftopng(pdf_file):
    fname = pdf_file.split('.')[0]
    pdf = PdfFileReader(open(pdf_file,'rb'))
    page_count = pdf.getNumPages()
    pages = convert_from_path(pdf_file, 300,first_page=3,last_page=page_count-1)
    #os.chdir(os.path.join(fname))
    for i,page in enumerate(pages):
        png_file = '{}_{}.png'.format(fname,i)
        page.save(png_file, 'PNG')
    return png_file
with open('names_m') as f:
	names_m = [f.replace('\n','') for f in f.readlines()]
with open('names_h') as f:
	names_h = [f.replace('\n','') for f in f.readlines()]
def religion(cname,fname):
    if isinstance(cname,str):
	    name_eng = re.sub(r'[^a-z ]+', ' ',cname.lower())
    else:
	    name_eng = 'NA'
    if isinstance(fname,str):
        name_gdn_eng = re.sub(r'[^a-z ]+', ' ',fname.lower())
    else:
        name_gdn_eng = 'NA'

    names = (name_eng+' '+name_gdn_eng).replace('  ',' ')
    match_h = re.findall(r'reddy|agarwal|purohit|goud|setty|setti|amma\b|anna\b|aiah\b|esh\b|kumar|reddy|\broy\b|gowda|gauda|appa|\bpatil\b|murthy|swamy|murty|murti|svami|natha\b|kumar|nadha\b|venkat|devi\b|rav\b|narayana|rava\b|raju\b|dakshit|sinha|nanda\b|avva\b|kant\b|kshi\b|ayya\b|vati\b|raja\b|esha\b|nadhan\b|nathan\b|ishvar|mati\b|ratna|nayar|jain|goyal|krshnana|ahuja|dran\b|reddi|veni\b|raj\b|nanda\b|shetti|singa\b|helavara|singha\b',names)
    match_m = re.findall(r'siddiq|ullah\b|ddin\b|khan\b|nnisa|abdul|abdus\b|begam|beg\b|\bvasha\b|\bshek\b|\bimam\b|saiyad|ahamad|shad\b|sultana|syed|\btaj\b|mahamad|ddan\b|ddana\b|ddina\b|unnina\b',names)

    if len(match_m) > 0:
        rel = 'M'
    elif len(match_h) > 0:
        rel = 'H'
    else:
        if not set(names.split(' ')).isdisjoint(names_m):
            rel = 'M'
        elif not set(names.split(' ')).isdisjoint(names_h):
            rel = 'H'
        else:
            rel = 'NA'
    return rel 
def clean_line(element):
    element = element.replace(' :','')
    element = element.replace(':','')
    element = element.replace(';','')
    element = element.replace('.','')
    element = element.replace('-','')
    element = element.replace('|','') 
    element = element.replace('[','') 
    element = element.replace(']','') 
    element = element.replace('#','') 
    element = element.replace('।','') 
    return element
def struct_data(rgname,rhno,rage,rgen):
    if rgname:
        gname = rgname[0]
    else:
        gname = ''
    
    if rhno:
        thno = rhno[0]
        thno = thno.replace(':','')
        thno = thno.replace('+','')
        thno = thno.replace('ন','')
        thno = thno.replace('ন:','')
        thno = thno.replace('না','')
        thno = thno.replace('নং','')
        thno = thno.replace(' ','')
        hno = thno
    else:
        hno = ''
    if rage:
        age = rage[0]
    else:
        age = ''
    if rgen:
        gen = rgen[0]
    else:
        gen = ''
        
    return  gname,hno,age,gen
def hno_en(hno):
    num_dict = {'১':'1','২':'2','৩':'3','৪':'4','৫':'5','৬':'6','৭':'7','৮':'8','৯':'9','০':'0','0':'0','ৰ':'','ু':'A','l':''
                ,'ং':'','া':'A','ক':'a','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','i':''}
    try:
        hn = [num_dict[x] for x in hno]
        temp = ''
        for i in hn:
            temp+=i
        fhn = temp
    except KeyError:
        fhn = ''
    return fhn
def convert_txt_csv(rawdata,pbname,ac_name): 
    sfile = '{}.csv'.format(pbname)
    pb_no = pbname.split('_')[1]
    ac = ac_name
    bad_words = ['Photo is', 'Available','Photo is not','DELETED','DÉLETED','DECETED','DELEWED','DEČETED']
    fields = ['sn','epic','Name','ENAME','gname','EGNAME','hno','EHNO','age','gender','EGEN','Rel','pb-no','AC']
    data = rawdata.split('\n')
    fdata = []
    for line in data:
        if not any(bad_word in line for bad_word in bad_words):
            fdata.append(line) 
    try:
        start_index_list = [i for i ,x in enumerate(fdata) if re.search(r"[A-Z]{3}.*[0-9]{3}",x)]
    except ValueError:
        pass
    with open(sfile, 'a',encoding='utf-8',newline='') as csvfile:
            csvwriter = csv.writer(csvfile) 
                # writing the fields 
            csvwriter.writerow(fields)
            for i in range(len(start_index_list)-1):
                s = start_index_list[i+1]-start_index_list[i]
                if s==5:
                    #test = fdata[start_index_list[i]-1]
                    if len(clean_line(fdata[start_index_list[i]-1]))==1 and i!=0:
                        if len(clean_line(fdata[start_index_list[i]-2]))>6:
                            sn = clean_line(fdata[start_index_list[i]-1])
                        else:
                            sn = clean_line(fdata[start_index_list[i]-2])
                    else:
                        sn = clean_line(fdata[start_index_list[i]-1])
                    epic  = clean_line(fdata[start_index_list[i]])
                    n_line = clean_line(fdata[start_index_list[i]+1])
                    if 'নাম' in n_line:
                        name = re.findall("(?<=নাম)(.*)",n_line)[0]
                    g_line = clean_line(fdata[start_index_list[i]+2])
                    if 'নাম' in n_line:
                        gname = re.findall("(?<=নাম)(.*)",g_line)
                    hno_line = clean_line(fdata[start_index_list[i]+3])
                    if 'বাড়ী' or 'ঘৰ' or 'মৰ' or 'ঘ' or 'ৰ' in hno_line:
                        try:
                            hno = re.findall("(?<=বাড়ী)(.*)",hno_line)
                        except IndexError:   
                            hno = re.findall("(?<=ঘৰ)(.*)",hno_line)
                        except IndexError:
                            hno = re.findall("(?<=মৰ)(.*)",hno_line)
                        except IndexError:
                            hno = re.findall("(?<=ঘ)(.*)",hno_line)
                        except IndexError:
                            hno = re.findall("(?<=ৰ)(.*)",hno_line)
                    ag_line = clean_line(fdata[start_index_list[i]+4]) 
                    if 'বয়স' or 'লিঙ্গ' in ag__line:   
                        age = re.findall("(?<=বয়স)(.*)(?=লিঙ্গ)",ag_line)
                        gen = re.findall("(?<=লিঙ্গ)(.*)",ag_line)
                    gname,hno,age,gen = struct_data(gname,hno,age,gen)
                    ENAME = trn.transform(name)
                    EGNAME = trn.transform(gname)
                    EHNO = hno_en(hno)
                    gens = gen.replace(' ','')
                    if gens=='মহিলা':
                        EGEN = 'F'
                    elif gens=='পুরুষ':
                        EGEN = 'M'
                    else:
                        EGEN = ''
                    #print(sn,epic,name,gname,hno,age,gen)
                    rel = religion(ENAME,EGNAME)
                    csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac])
                elif s==6:
                    test_line = fdata[start_index_list[i+1]-1]
                    if len(test_line)>6:
                        sn = clean_line(fdata[start_index_list[i]+1])
                        epic  = clean_line(fdata[start_index_list[i]])
                        n_line = clean_line(fdata[start_index_list[i]+2])
                        if 'নাম' in n_line:
                            name = re.findall("(?<=নাম)(.*)",n_line)[0]
                        g_line = clean_line(fdata[start_index_list[i]+3])
                        if 'নাম' in n_line:
                            gname = re.findall("(?<=নাম)(.*)",g_line)
                        hno_line = clean_line(fdata[start_index_list[i]+4])
                        if 'বাড়ী' or 'ঘৰ' or 'মৰ' or 'ঘ' or 'ৰ' in hno_line:
                            try:
                                hno = re.findall("(?<=বাড়ী)(.*)",hno_line)
                            except IndexError:   
                                hno = re.findall("(?<=ঘৰ)(.*)",hno_line)
                            except IndexError:
                                hno = re.findall("(?<=মৰ)(.*)",hno_line)
                            except IndexError:
                                hno = re.findall("(?<=ঘ)(.*)",hno_line)
                            except IndexError:
                                hno = re.findall("(?<=ৰ)(.*)",hno_line)
                        ag_line = clean_line(fdata[start_index_list[i]+5]) 
                        if 'বয়স' or 'লিঙ্গ' in n_line:   
                            age = re.findall("(?<=বয়স)(.*)(?=লিঙ্গ)",ag_line)
                            gen = re.findall("(?<=লিঙ্গ)(.*)",ag_line)

                        gname,hno,age,gen = struct_data(gname,hno,age,gen)
                        ENAME = trn.transform(name)
                        EGNAME = trn.transform(gname)
                        EHNO = hno_en(hno)
                        gens = gen.replace(' ','')
                        if gens=='মহিলা':
                            EGEN = 'F'
                        elif gens=='পুরুষ':
                            EGEN = 'M'
                        else:
                            EGEN = ''
                        #print(sn,epic,name,gname,hno,age,gen)
                        rel = religion(ENAME,EGNAME)
                        csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac])       
                    
                    else:
                        test_line = fdata[start_index_list[i]-1]
                        if len(test_line)==1 and len(fdata[start_index_list[i]-2])<6 and i!=0:
                            sn = clean_line(fdata[start_index_list[i]-2])
                        elif len(test_line)<6:
                            sn = clean_line(fdata[start_index_list[i]-1])
                        else:
                            sn = ''
                        epic  = clean_line(fdata[start_index_list[i]])
                        n_line = clean_line(fdata[start_index_list[i]+1])
                        if 'নাম' in n_line:
                            name = re.findall("(?<=নাম)(.*)",n_line)[0]
                        g_line = clean_line(fdata[start_index_list[i]+2])
                        if 'নাম' in n_line:
                            gname = re.findall("(?<=নাম)(.*)",g_line)
                        hno_line = clean_line(fdata[start_index_list[i]+3])
                        if 'বাড়ী' or 'ঘৰ' or 'মৰ' or 'ঘ' or 'ৰ' in hno_line:
                            try:
                                hno = re.findall("(?<=বাড়ী)(.*)",hno_line)
                            except IndexError:   
                                hno = re.findall("(?<=ঘৰ)(.*)",hno_line)
                            except IndexError:
                                hno = re.findall("(?<=মৰ)(.*)",hno_line)
                            except IndexError:
                                hno = re.findall("(?<=ঘ)(.*)",hno_line)
                            except IndexError:
                                hno = re.findall("(?<=ৰ)(.*)",hno_line)
                        ag_line = clean_line(fdata[start_index_list[i]+4]) 
                        if 'বয়স' or 'লিঙ্গ' in n_line:   
                            age = re.findall("(?<=বয়স)(.*)(?=লিঙ্গ)",ag_line)
                            gen = re.findall("(?<=লিঙ্গ)(.*)",ag_line)

                        gname,hno,age,gen = struct_data(gname,hno,age,gen)
                        ENAME = trn.transform(name)
                        EGNAME = trn.transform(gname)
                        EHNO = hno_en(hno)
                        gens = gen.replace(' ','')
                        if gens=='মহিলা':
                            EGEN = 'F'
                        elif gens=='পুরুষ':
                            EGEN = 'M'
                        else:
                            EGEN = ''
                        #print(sn,epic,name,gname,hno,age,gen)
                        rel = religion(ENAME,EGNAME)
                        csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac])       
                    
                elif s==7:
                    if start_index_list[i+1]-start_index_list[i]==7:
                        if len(fdata[start_index_list[i+1]-1])<6:
                            if len(clean_line(fdata[start_index_list[i]+1]))<5 and 'নাম' not in fdata[start_index_list[i]+1]:
                                sn = clean_line(fdata[start_index_list[i]+1])
                                epic = clean_line(fdata[start_index_list[i]])
                                nline = fdata[start_index_list[i]+2]
                                gline = fdata[start_index_list[i]+3]
                                hnline = fdata[start_index_list[i]+4]
                                agline = fdata[start_index_list[i]+5]
                                n_line = clean_line(nline)
                                if 'নাম' in n_line:
                                    name = re.findall("(?<=নাম)(.*)",n_line)[0]
                                g_line = clean_line(gline)
                                if 'নাম' in n_line:
                                    gname = re.findall("(?<=নাম)(.*)",g_line)
                                hno_line = clean_line(hnline)
                                if 'বাড়ী' or 'ঘৰ' or 'মৰ' or 'ঘ' or 'ৰ' in hno_line:
                                    try:
                                        hno = re.findall("(?<=বাড়ী)(.*)",hno_line)
                                    except IndexError:   
                                        hno = re.findall("(?<=ঘৰ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=মৰ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=ঘ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=ৰ)(.*)",hno_line)
                                ag_line = clean_line(agline) 
                                if 'বয়স' or 'লিঙ্গ' in ag__line:   
                                    age = re.findall("(?<=বয়স)(.*)(?=লিঙ্গ)",ag_line)
                                    gen = re.findall("(?<=লিঙ্গ)(.*)",ag_line)
                                gname,hno,age,gen = struct_data(gname,hno,age,gen)
                                ENAME = trn.transform(name)
                                EGNAME = trn.transform(gname)
                                EHNO = hno_en(hno)
                                gens = gen.replace(' ','')
                                if gens=='মহিলা':
                                    EGEN = 'F'
                                elif gens=='পুরুষ':
                                    EGEN = 'M'
                                else:
                                    EGEN = ''
                                #print(sn,epic,name,gname,hno,age,gen)
                                rel = religion(ENAME,EGNAME)
                                csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac]) 
                            elif  len(fdata[start_index_list[i+1]-2])<6:
                                if len(clean_line(fdata[start_index_list[i]-1]))==1:
                                    if len(clean_line(fdata[start_index_list[i]-2]))<5:
                                        sn = clean_line(fdata[start_index_list[i]-2])
                                    else:
                                        sn = clean_line(fdata[start_index_list[i]-1])                      
                                else:
                                    sn = clean_line(fdata[start_index_list[i]-1])
                                epic = clean_line(fdata[start_index_list[i]])
                                nline = fdata[start_index_list[i]+1]
                                gline = fdata[start_index_list[i]+2]
                                hnline = fdata[start_index_list[i]+3]
                                agline = fdata[start_index_list[i]+4]
                                n_line = clean_line(nline)
                                if 'নাম' in n_line:
                                    name = re.findall("(?<=নাম)(.*)",n_line)[0]
                                g_line = clean_line(gline)
                                if 'নাম' in n_line:
                                    gname = re.findall("(?<=নাম)(.*)",g_line)
                                hno_line = clean_line(hnline)
                                if 'বাড়ী' or 'ঘৰ' or 'মৰ' or 'ঘ' or 'ৰ' in hno_line:
                                    try:
                                        hno = re.findall("(?<=বাড়ী)(.*)",hno_line)
                                    except IndexError:   
                                        hno = re.findall("(?<=ঘৰ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=মৰ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=ঘ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=ৰ)(.*)",hno_line)
                                ag_line = clean_line(agline) 
                                if 'বয়স' or 'লিঙ্গ' in ag__line:   
                                    age = re.findall("(?<=বয়স)(.*)(?=লিঙ্গ)",ag_line)
                                    gen = re.findall("(?<=লিঙ্গ)(.*)",ag_line)
                                gname,hno,age,gen = struct_data(gname,hno,age,gen)
                                ENAME = trn.transform(name)
                                EGNAME = trn.transform(gname)
                                EHNO = hno_en(hno)
                                gens = gen.replace(' ','')
                                if gens=='মহিলা':
                                    EGEN = 'F'
                                elif gens=='পুরুষ':
                                    EGEN = 'M'
                                else:
                                    EGEN = ''
                                #print(sn,epic,name,gname,hno,age,gen)
                                rel = religion(ENAME,EGNAME)
                                csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac]) 

                            else:
                                if 'লিঙ্গ' and 'বয়স' not in fdata[start_index_list[i+1]-2]:
                                    #print(fdata[start_index_list[i]+1:start_index_list[i+1]-2])
                                    if 'লিঙ্গ' and 'বয়স'  in fdata[start_index_list[i+1]-3]:
                                        if len(fdata[start_index_list[i+1]-2])<4:
                                            hnline = fdata[start_index_list[i]+3]+fdata[start_index_list[i+1]-2]
                                        else:
                                            agline = fdata[start_index_list[i]+4]+' '+fdata[start_index_list[i+1]-2]
                                    if 'লিঙ্গ' and 'বয়স'  not in fdata[start_index_list[i+1]-3]:
                                        gline = fdata[start_index_list[i]+2]+fdata[start_index_list[i+1]-2]

                                else:
                                    if 'বাড়ী' in fdata[start_index_list[i+1]-3]:
                                        if 'নাম' in fdata[start_index_list[i+1]-4]:
                                            nline = fdata[start_index_list[i]+1]+fdata[start_index_list[i]+2]
                                        if 'নাম' not in fdata[start_index_list[i+1]-4]:
                                            gline = fdata[start_index_list[i]+2]+fdata[start_index_list[i]+3]
                                    else:
                                        hnline = fdata[start_index_list[i]+3]+fdata[start_index_list[i]+4]
                                test_line = fdata[start_index_list[i]-1]
                                if len(test_line)<6:
                                    sn = clean_line(fdata[start_index_list[i]-1])
                                else:
                                    sn = ''
                                epic = clean_line(fdata[start_index_list[i]])
                                n_line = clean_line(nline)
                                if 'নাম' in n_line:
                                    name = re.findall("(?<=নাম)(.*)",n_line)[0]
                                g_line = clean_line(gline)
                                if 'নাম' in g_line:
                                    gname = re.findall("(?<=নাম)(.*)",g_line)
                                hno_line = clean_line(hnline)
                                if 'বাড়ী' or 'ঘৰ' or 'মৰ' or 'ঘ' or 'ৰ' in hno_line:
                                    try:
                                        hno = re.findall("(?<=বাড়ী)(.*)",hno_line)
                                    except IndexError:   
                                        hno = re.findall("(?<=ঘৰ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=মৰ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=ঘ)(.*)",hno_line)
                                    except IndexError:
                                        hno = re.findall("(?<=ৰ)(.*)",hno_line)
                                ag_line = clean_line(agline) 
                                if 'বয়স' or 'লিঙ্গ' in ag__line:   
                                    age = re.findall("(?<=বয়স)(.*)(?=লিঙ্গ)",ag_line)
                                    gen = re.findall("(?<=লিঙ্গ)(.*)",ag_line)
                                gname,hno,age,gen = struct_data(gname,hno,age,gen)
                                ENAME = trn.transform(name)
                                EGNAME = trn.transform(gname)
                                EHNO = hno_en(hno)
                                gens = gen.replace(' ','')
                                if 'মহিলা' in gens:
                                    EGEN = 'F'
                                elif 'পুরুষ' in gens:
                                    EGEN = 'M'
                                elif gens=='মহিলা':
                                    EGEN = 'F'
                                elif gens=='পুরুষ':
                                    EGEN = 'M'
                                else:
                                    EGEN = ''
                                #print(sn,epic,name,gname,hno,age,gen)
                                rel = religion(ENAME,EGNAME)
                                csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac])
                        else:
                            try:
                                dblock = fdata[start_index_list[i]:start_index_list[i+1]]
                                result = ''
                                for element in dblock:
                                    result+=element+','
                                with open('missed_data_log.txt','a',encoding = 'utf-8') as mfile:
                                    mfile.write(ac+'--'+str(pb_no)+'-----'+result+'\n')
                                    mfile.close
                            except IndexError:
                                pass
                else:
                    dblock = fdata[start_index_list[i]:start_index_list[i+1]]
                    result = ''
                    for element in dblock:
                        result+=element+','
                    with open('missed_data_log.txt','a',encoding = 'utf-8') as mfile:
                        mfile.write(ac+'--'+str(pb_no)+'-----'+result+'\n')
                        mfile.close
            csvfile.close()
    return csvfile
