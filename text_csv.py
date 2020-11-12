import os
import glob 
import utils1
path = os.getcwd()
#ac = sys.argv[1]
ac = 'Cachar_Katigora'
ac_name = ac.split('_')[1]
os.chdir(os.path.join(path,'test'))
path1 = os.getcwd()
#print(path1)
extension = 'txt'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
print(len(all_filenames))
for file_name in all_filenames:
    pb = file_name.split('.')[0]
    pbname,pbnum = pb.split('_')[:2]
    utils1.convert_txt_csv(file_name,pbname,pbnum,ac_name)
    print('{} file completed'.format(pb))
print('csv files processing completed')   