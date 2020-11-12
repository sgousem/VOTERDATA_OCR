import os
import glob 
path = os.getcwd()
ac = 'Sivasagar_thowra'
os.chdir(os.path.join('pdf/{}/Mother_Roll'.format(ac)))
extension = 'pdf'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
os.chdir(path)
for file_name in all_filenames:
	pb = file_name.split('.')[0]
	os.chdir(os.path.join(path,'png/{}/{}'.format(ac,pb)))
	path1 = os.getcwd()
	extension = 'png'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
	for file_name1 in all_filenames:
		os.remove(file_name1)
		os.chdir(path1)
os.chdir(path)
print('all png files deletion completed')