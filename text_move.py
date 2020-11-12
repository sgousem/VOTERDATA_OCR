import os
import glob 
path = os.getcwd()
#ac = sys.argv[1]
ac = 'Sivasagar_thowra'
ac_name = ac.split('_')[1]
os.chdir(os.path.join('pdf/{}/Mother_Roll'.format(ac)))
extension = 'pdf'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
os.chdir(path)
for file_name in all_filenames:
	pb = file_name.split('.')[0]
	os.chdir(os.path.join(path,'png/{}/{}'.format(ac,pb)))
	path1 = os.getcwd()
	try:
		with open('{}.txt'.format(pb),'r',encoding = 'utf-8') as textfile:
			data = textfile.read()
			os.chdir(os.path.join(path,'text'))
			with open('{}_text.txt'.format(pb),'w',encoding = 'utf-8') as newfile:
				newfile.write(data)
				newfile.close
			os.chdir(path1)
			textfile.close()
	except FileNotFoundError:
		pass
os.chdir(path)
print('text files transfer completed')