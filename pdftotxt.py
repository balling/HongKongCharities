import urllib2
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from subprocess import call
from pdfminer.layout import LAParams
import os

url = 'http://www.ird.gov.hk/chi/pdf/c_s88list.pdf'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
pdfdata = opener.open(url).read()
file = open('document.pdf', 'wb')
file.write(pdfdata)
file.close()
call('qpdf --password= --decrypt {0}/document.pdf {0}/decrypted.pdf'.format(os.getcwd()).split())

outfp=open('modifiedla.txt', 'w')
parser = PDFParser(open('decrypted.pdf','rb'))
document = PDFDocument(parser)
rsrcmgr = PDFResourceManager()
laparams = LAParams(char_margin=10)
device = TextConverter(rsrcmgr, outfp, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)

outfp.close()
