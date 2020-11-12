import os,time
import requests
import csv,re
from indictrans import Transliterator
def transliterate(text, l1, l2):
    response = requests.get(
        "https://inputtools.google.com/request",
        params={
            "text": text,
            "ime": "_".join(['transliteration', l1, l2]),
            "ie": "utf-8",
            "oe": "utf-8",
            "app": "jsapi",
        }
    )
    if not response.ok:
        return False
    jc = response.json()
    if jc[0] != 'SUCCESS':
        return
    try:
        result = jc[-1][0][1][0]
    except:
        result = text
    return result

def transliterate_tel(eng_text):
    eng_text = eng_text.replace(':', '')
    return transliterate(eng_text, 'en', 'te')
def transliterate_ass(ass_text):
    ass_text = ass_text.replace(':', '')
    return transliterate(ass_text, 'bn', 'en')
print('process started at:',time.localtime())
def clean_line(element):
    element = element.replace(' :','')
    element = element.replace(':','')
    element = element.replace(';','')
    element = element.replace('.','')
    element = element.replace('-','')
    element = element.replace('|','') 
    element = element.replace('[','') 
    element = element.replace(']','') 
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
                ,'ং':'E','া':'A','ক':'a','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','i':''}
    try:
        hn = [num_dict[x] for x in hno]
        temp = ''
        for i in hn:
            temp+=i
        fhn = temp
    except KeyError:
        fhn = ''
    return fhn
bad_words = ['Photo is', 'Available','Photo is not','DELETED','DÉLETED','DECETED','DELEWED','DEČETED','DELETER'] 
trn = Transliterator(source='ben', target='eng', build_lookup=True)
fname = 'S03A15P1_text.txt'
nfname = fname.split('.')[0]+'_f'
with open(fname,'r',encoding='utf-8-') as oldfile, open('{}.txt'.format(nfname), 'w',encoding='utf-8') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)
with open('{}.txt'.format(nfname),'r',encoding = 'utf-8') as textfile:
        data = textfile.read()
data = data.split('\n')
try:
    start_index_list = [i for i ,x in enumerate(data) if re.search(r"[A-Z]{3}[0-9]{7}",x)]
except ValueError:
    pass
try:
    end_index_list = [i for i ,x in enumerate(data) if x[:4]=='বয়স'or x[:6]=='| বয়স' ]
except ValueError:
    pass    
sfile = '{}.csv'.format(fname.split('_')[0])
fields = ['sn','epic','Name','ENAME','gname','EGNAME','hno','EHNO','age','gender','EGEN']
#sfile = 'temp_text.csv'
with open(sfile, 'w',encoding='utf-8',newline='') as csvfile:
        csvwriter = csv.writer(csvfile) 
            # writing the fields 
        csvwriter.writerow(fields)
        for i in range(len(start_index_list)):
            s = end_index_list[i]-start_index_list[i]
            if s<5:
                sn = data[start_index_list[i]-1] 
                epic  = clean_line(data[start_index_list[i]])
                n_line = clean_line(data[start_index_list[i]+1])
                if 'নাম' in n_line:
                    name = re.findall("(?<=নাম)(.*)",n_line)[0]
                g_line = clean_line(data[start_index_list[i]+2])
                if 'নাম' in n_line:
                    gname = re.findall("(?<=নাম)(.*)",g_line)
                hno_line = clean_line(data[start_index_list[i]+3])
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
                ag_line = clean_line(data[start_index_list[i]+4]) 
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
                else:
                    EGEN = 'M'
                #print(sn,epic,name,gname,hno,age,gen)
                csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN])
            elif s>4 and s<6:
                test_line = data[start_index_list[i]+1]
                if len(test_line)<7:
                    sn = data[start_index_list[i]+1]
                    epic  = clean_line(data[start_index_list[i]])
                    n_line = clean_line(data[start_index_list[i]+2])
                    if 'নাম' in n_line:
                        name = re.findall("(?<=নাম)(.*)",n_line)[0]
                    g_line = clean_line(data[start_index_list[i]+3])
                    if 'নাম' in n_line:
                        gname = re.findall("(?<=নাম)(.*)",g_line)
                    hno_line = clean_line(data[start_index_list[i]+4])
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
                    ag_line = clean_line(data[start_index_list[i]+5]) 

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
                    else:
                        EGEN = 'M'
                    csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN])       
                else:
                    dblock = data[start_index_list[i]-1:end_index_list[i]+1]
                    result = ''
                    for element in dblock:
                        result+=element
                    with open('missed_data_log.txt','a',encoding = 'utf-8') as mfile:
                        mfile.write(result+'\n')
                        mfile.close
            if s>5:
                dblock = data[start_index_list[i]:end_index_list[i]+1]
                result = ''
                for element in dblock:
                    result+=element
                with open('missed_data_log.txt','a',encoding = 'utf-8') as mfile:
                    mfile.write(result+'\n')
                    mfile.close
            #csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN])
        csvfile.close()
print('processs completed')