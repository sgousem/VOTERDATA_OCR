from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
import os,glob
#ac = ''
os.chdir(os.path.join('pdf/Cachar_Katigora/Mother_Roll'))
extension = 'pdf'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
total_pages = 0
for pdf_file in all_filenames:
    pdf = PdfFileReader(open(pdf_file,'rb'))
    page_count = pdf.getNumPages()
    total_pages +=page_count
print(total_pages)