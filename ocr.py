import io
import glob
import os
from google.cloud import vision
#from google.cloud.vision import ImageAnnotatorClient
#from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\USER\\Raylabsproject2019-0783fac75419.json"
client = vision.ImageAnnotatorClient() # pylint: disable=no-member
#client = vision.ImageAnnotatorClient()
def convert_png_txt(dir_name):
    fname = dir_name.split('/')[1]
    os.chdir(dir_name)
    extension = 'png'
    text_file = '{}_text.txt'.format(fname)
    #client = vision.ImageAnnotatorClient()
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    with open(text_file, 'a',encoding='utf-8') as _f:
        for png_file in all_filenames:
        # Instantiates a client
            with io.open(png_file, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            image_context = vision.ImageContext(
                language_hints='as')

            response = client.document_text_detection(image=image,
                                                    image_context=image_context)
            
            text = response.full_text_annotation.text
        
            _f.write(text)
    return 'process completed'
convert_png_txt('png/S03A15P5')