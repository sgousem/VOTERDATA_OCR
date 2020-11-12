import os
import glob 
path = os.getcwd()
ac = 'Cachar_Katigora'
os.chdir(os.path.join('pdf/test'))
extension = 'pdf'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
os.chdir(path)
for file_name in all_filenames:
	pb = file_name.split('.')[0]
	os.chdir(os.path.join(path,'png/{}/{}'.format(ac,pb)))
	path1 = os.getcwd()
	extension = 'txt'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
	for file_name1 in all_filenames:
		with open(file_name1,'r',encoding = 'utf-8') as textfile:
			data = textfile.read()
			with open('{}.txt'.format(pb),'a',encoding = 'utf-8') as newfile:
				newfile.write(data)
				newfile.close
			os.chdir(path1)
			textfile.close()
os.chdir(path)
print('text files transfer completed')