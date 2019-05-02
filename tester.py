import os
from datetime import datetime
from time import time
from functions.docx2pdf import docx2pdf
#
# dir_path = os.path.dirname(os.path.realpath(__file__))
# word_doc = os.path.join(dir_path, "word_output", "29-Apr-2019-oesterbaron.nl.docx")
# pdf_files = os.path.join(dir_path, "pdf_files")
# d = docx2pdf(pdf_files, word_doc)
# print('Converted to ' + d.convert_to())

dir_path = os.path.dirname(os.path.realpath(__file__))
path = "data/www.bouwbedrijfjari.nl/crawl/crawl_overview.csv"
t = os.path.getmtime(path)

if int(t)+86400 <= int(time()):
    print("ouder dan 24 uur")
else:
    print("nog jong genoeg")

