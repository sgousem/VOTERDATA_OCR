from indictrans import Transliterator
import re,csv
trn = Transliterator(source='ben', target='eng', build_lookup=True)



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
    element = element.replace('(','')
    element = element.replace('।','')
    element = element.replace(')','')
    return element
def struct_data(rgname,rhno,rage,rgen):
    if rgname:
        gname = rgname[0]
    else:
        gname = 'NA'
    
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
        hno = 'NA'
    if rage:
        age = rage[0]
    else:
        age = 'NA'
    if rgen:
        gen = rgen[0]
    else:
        gen = 'NA'
        
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
        fhn = 'NA'
    return fhn
def convert_txt_csv(text_file,pbname,pbnum,ac_name): 
    sfile = '{}_{}.csv'.format(pbname,pbnum)
    pb_no = pbnum
    ac = ac_name
    bad_words = ['Photo is', 'Available','Photo is not','DELETED','DÉLETED','DECETED','DELEWED','DEČETED']
    fields = ['sn','epic','Name','ENAME','gname','EGNAME','hno','EHNO','age','gender','EGEN','Rel','pb-no','AC']
    with open(text_file,'r',encoding = 'utf-8') as textfile:
        data = textfile.read()
    data = data.split('\n')
    #data = rawdata.split('\n')
    fdata = []
    for line in data:
        if not any(bad_word in line for bad_word in bad_words):
            fdata.append(line) 
    try:
        start_index_list = [i for i ,x in enumerate(fdata) if re.search(r"[A-Z]{3}.*[0-9]{3}",x)]
    except ValueError:
        pass
    start_index_list.append(len(fdata))   
    with open(sfile, 'w',encoding='utf-8',newline='') as csvfile:
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
                        sgname,shno,sage,sgen = struct_data(gname,hno,age,gen)
                        ENAME = trn.transform(name)
                        EGNAME = trn.transform(sgname)
                        EHNO = hno_en(shno)
                        gens = sgen.replace(' ','')
                        if gens=='মহিলা':
                            EGEN = 'F'
                        elif gens=='পুরুষ':
                            EGEN = 'M'
                        else:
                            EGEN = ''
                        #print(sn,epic,name,gname,hno,age,gen)
                        rel = religion(ENAME,EGNAME)
                        #csvwriter.writerow([sn,epic,name,ENAME,sgname,EGNAME,hno,EHNO,sage,sgen,EGEN,rel,pb_no,ac])
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

                        sgname,shno,sage,sgen = struct_data(gname,hno,age,gen)
                        ENAME = trn.transform(name)
                        EGNAME = trn.transform(sgname)
                        EHNO = hno_en(shno)
                        gens = sgen.replace(' ','')
                        if gens=='মহিলা':
                            EGEN = 'F'
                        elif gens=='পুরুষ':
                            EGEN = 'M'
                        else:
                            EGEN = ''
                        #print(sn,epic,name,gname,hno,age,gen)
                        rel = religion(ENAME,EGNAME)
                        #csvwriter.writerow([sn,epic,name,ENAME,sgname,EGNAME,hno,EHNO,sage,sgen,EGEN,rel,pb_no,ac])
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
                                sgname,shno,sage,sgen = struct_data(gname,hno,age,gen)
                                ENAME = trn.transform(name)
                                EGNAME = trn.transform(sgname)
                                EHNO = hno_en(shno)
                                gens = sgen.replace(' ','')
                                if gens=='মহিলা':
                                    EGEN = 'F'
                                elif gens=='পুরুষ':
                                    EGEN = 'M'
                                else:
                                    EGEN = ''
                                #print(sn,epic,name,gname,hno,age,gen)
                                rel = religion(ENAME,EGNAME)
                                #csvwriter.writerow([sn,epic,name,ENAME,sgname,EGNAME,hno,EHNO,sage,sgen,EGEN,rel,pb_no,ac])
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
                                sgname,shno,sage,sgen = struct_data(gname,hno,age,gen)
                                ENAME = trn.transform(name)
                                EGNAME = trn.transform(sgname)
                                EHNO = hno_en(shno)
                                gens = sgen.replace(' ','')
                                if gens=='মহিলা':
                                    EGEN = 'F'
                                elif gens=='পুরুষ':
                                    EGEN = 'M'
                                else:
                                    EGEN = ''
                                #print(sn,epic,name,gname,hno,age,gen)
                                rel = religion(ENAME,EGNAME)
                                #csvwriter.writerow([sn,epic,name,ENAME,sgname,EGNAME,hno,EHNO,sage,sgen,EGEN,rel,pb_no,ac])
                                csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac])

                            else:
                                if 'লিঙ্গ' and 'বয়স' not in fdata[start_index_list[i+1]-2]:
                                    #print(fdata[start_index_list[i]+1:start_index_list[i+1]-2])
                                    if 'লিঙ্গ' and 'বয়স'  in fdata[start_index_list[i+1]-3]:
                                        if len(fdata[start_index_list[i+1]-2])<4:
                                            hnline = fdata[start_index_list[i]+3]+fdata[start_index_list[i+1]-2]
                                        else:
                                            agline = fdata[start_index_list[i]+4]+' '+fdata[start_index_list[i+1]-2]
                                    else:
                                        gline = fdata[start_index_list[i]+2]+fdata[start_index_list[i+1]-2]

                                else:
                                    if 'বাড়ী' in fdata[start_index_list[i+1]-3]:
                                        if 'নাম' in fdata[start_index_list[i+1]-4]:
                                            nline = fdata[start_index_list[i]+1]+fdata[start_index_list[i]+2]
                                        else:
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
                                sgname,shno,sage,sgen = struct_data(gname,hno,age,gen)
                                ENAME = trn.transform(name)
                                EGNAME = trn.transform(sgname)
                                EHNO = hno_en(shno)
                                gens = sgen.replace(' ','')
                                if gens=='মহিলা':
                                    EGEN = 'F'
                                elif gens=='পুরুষ':
                                    EGEN = 'M'
                                else:
                                    EGEN = ''
                                #print(sn,epic,name,gname,hno,age,gen)
                                rel = religion(ENAME,EGNAME)
                                #csvwriter.writerow([sn,epic,name,ENAME,sgname,EGNAME,hno,EHNO,sage,sgen,EGEN,rel,pb_no,ac])
                                csvwriter.writerow([sn,epic,name,ENAME,gname,EGNAME,hno,EHNO,age,gen,EGEN,rel,pb_no,ac])
                                
                        else:
                            try:
                                dblock = fdata[start_index_list[i]:start_index_list[i+1]]
                                result = ''
                                for element in dblock:
                                    result+=element+','
                                with open('{}_data_log.txt'.format(ac),'a',encoding = 'utf-8') as mfile:
                                    mfile.write(ac+'--'+str(pb_no)+'-----'+result+'\n')
                                    mfile.close
                            except IndexError:
                                pass
                else:
                    dblock = fdata[start_index_list[i]:start_index_list[i+1]]
                    result = ''
                    for element in dblock:
                        result+=element+','
                    with open('{}_data_log.txt'.format(ac),'a',encoding = 'utf-8') as mfile:
                        mfile.write(ac+'--'+str(pb_no)+'-----'+result+'\n')
                        mfile.close
            csvfile.close()
    return csvfile
