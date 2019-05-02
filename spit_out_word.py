# pip install python-docx

import os
from datetime import date
from time import time

from docx import Document
from docx.shared import RGBColor, Inches, Cm, Pt

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_COLOR_INDEX
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from functions.readConfig import readConfig
from functions.crawl_overview import CrawlOverview
from functions.docx_inleiding import inleiding
from functions.docx_eerste_pagina import EerstePagina
from functions.docx_algemeen_overzicht import AlgemeenOverzicht
from functions.docx_toc import toc
from functions.docx_pagespeed import DocxPageSpeed
from functions.docx_csv_files import CSV2Docx
from functions.screaming import Screaming

# import locale
# locale.setlocale(locale.LC_TIME, "nl_NL.utf8")

class CreateWord:
    def __init__(self, config=None):
        self.datum = '{:%d-%b-%Y}'.format(date.today())
        self.start_path = os.path.dirname(os.path.realpath(__file__))

        try:
            self.url = config['url']
            self.domain = config['domain']
            self.tempate_file = config['word_template']
            self.search_console_url = config['search_console_url']
        except KeyError as e:
            return "Config variables not found! {}".format(e)

        self.ps = None
        self.frog_files = {}
        self.document_fields = None
        self.doc = None
        self.data = {}
        self.co_table_headers = None
        self.co_readydata = None
        self.template = None

        cf = readConfig()
        self.config = cf.config
        self.ps_api = self.config['google_page_speed_api']

        self.word_output_file = self.set_doc_params()
        self.frog_data_folder = self.get_frog_folder()
        self.domain_folder = self.set_data_domain_path()
        self.get_frog_files()

        self.create_crawl_data()
        self.get_crawl_overview_data()

        self.ps_all_data = {}

        # self.crawl_data = self.get_crawl_data()
        
        self.open_document()
        self.set_document_styles()
        self.merge_document()
        self.write_document()
    
    def set_doc_params(self):
        if self.tempate_file is not None:
            self.template = os.path.join(self.start_path, "word_templates", self.tempate_file)
        
        return os.path.join(self.start_path, "word_output", "{}-{}.docx".format(self.datum, self.domain))

    def set_data_domain_path(self):
        return os.path.join(self.start_path, "../data", self.domain)

    def get_frog_folder(self):
        start_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(start_path, "data", self.domain, 'crawl')

    def get_frog_files(self):
        for r, d, f in os.walk(self.frog_data_folder):
            for file in f:
                if '.csv' in file:
                    self.frog_files[file] = os.path.join(r, file)

    def create_crawl_data(self):
        try:
            t = os.path.getmtime(self.frog_files['crawl_overview.csv'])
            if int(t) + 86400 <= int(time()):
                print('Creating Screaming Frog crawl data')
                s = Screaming(self.domain_folder, self.url, self.search_console_url)
                s.run_screamer()
            else:
                print('Using current Screaming Frog crawl data')
        except KeyError as e:
            print('error {}'.format(e))
            return {}

    def get_crawl_overview_data(self):
        try:
            co = CrawlOverview(self.frog_files['crawl_overview.csv'])
            self.co_table_headers = co.table_headers
            self.co_readydata = co.readydata
        except KeyError:
            print('error')
            return {}

    def open_document(self):
        self.doc = Document(self.template)

    def set_document_styles(self):
        obj_styles = self.doc.styles

        style = self.doc.styles['Title']
        font = style.font
        font.name = 'Font Awesome 5 Pro Light'
        font.size = Pt(20)

        style = self.doc.styles['Heading 1']
        font = style.font
        font.name = 'Font Awesome 5 Pro Light'
        font.size = Pt(16)

        style = self.doc.styles['Heading 2']
        font = style.font
        font.name = 'Font Awesome 5 Pro Light'
        font.size = Pt(14)

        style = self.doc.styles['Heading 3']
        font = style.font
        font.name = 'Font Awesome 5 Pro Light'
        font.size = Pt(12)

        obj_charstyle = obj_styles.add_style('FontAwesomeBrands', WD_STYLE_TYPE.CHARACTER)
        obj_font = obj_charstyle.font
        obj_font.size = Pt(13)
        obj_font.name = 'Font Awesome 5 Brands'

        obj_charstyle = obj_styles.add_style('FontAwesomeLight', WD_STYLE_TYPE.CHARACTER)
        obj_font = obj_charstyle.font
        obj_font.size = Pt(13)
        obj_font.name = 'Font Awesome 5 Pro Light'

        obj_charstyle = obj_styles.add_style('FontAwesomeRegular', WD_STYLE_TYPE.CHARACTER)
        obj_font = obj_charstyle.font
        obj_font.size = Pt(13)
        obj_font.name = 'Font Awesome 5 Pro Regular'

        obj_charstyle = obj_styles.add_style('FontAwesomeSolid', WD_STYLE_TYPE.CHARACTER)
        obj_font = obj_charstyle.font
        obj_font.size = Pt(13)
        obj_font.name = 'Font Awesome 5 Pro Solid'

    def print_paragraph_styles(self):
        styles = self.doc.styles
        paragraph_styles = [s for s in styles if s.type == WD_STYLE_TYPE.PARAGRAPH]
        for style in paragraph_styles:
            print(style.name)    

    def print_table_styles(self):
        styles = self.doc.styles
        paragraph_styles = [s for s in styles if s.type == WD_STYLE_TYPE.TABLE]
        for style in paragraph_styles:
            print(style.name)

    def print_list_styles(self):
        styles = self.doc.styles
        paragraph_styles = [s for s in styles if s.type == WD_STYLE_TYPE.LIST]
        for style in paragraph_styles:
            print(style.name)

    def merge_document(self):
        sc = 0
        EerstePagina(self.doc, sc, self.domain)
        inleiding(self.doc, self.domain)
        toc(self.doc)
        AlgemeenOverzicht(self.doc, self.config, self.co_readydata, self.co_table_headers)

        DocxPageSpeed(self.doc, self.config, self.url, self.domain, 'mobile')
        DocxPageSpeed(self.doc, self.config, self.url, self.domain, 'desktop')

        self.change_orientation()
        CSV2Docx(self.config, self.doc, self.frog_data_folder)

        # self.legenda()

    def auto_cell(self, table):
        for r in table.rows:
            for c in r._tr.tc_lst:
                tcW = c.tcPr.tcW
                tcW.type = 'auto'
                tcW.w = 0

    def legenda(self):
        self.change_orientation()
        self.doc.add_heading("Legenda & Uitleg", level=2)
        self.doc.add_paragraph()

        for key, val in self.ps_all_data['lighthouseResult']['audits'].items():
            self.doc.add_heading(val['title'], level=3)
            self.doc.add_paragraph(val['description'])
            self.doc.add_paragraph()
            
    def change_orientation(self):
        current_section = self.doc.sections[-1]
        new_width, new_height = current_section.page_height, current_section.page_width
        new_section = self.doc.add_section(WD_SECTION.NEW_PAGE)
        new_section.orientation = WD_ORIENT.LANDSCAPE
        new_section.page_width = new_width
        new_section.page_height = new_height
        return new_section            

    def set_repeat_table_header(self, row):
        """ set repeat table row on every new page
        """
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        tblHeader = OxmlElement('w:tblHeader')
        tblHeader.set(qn('w:val'), "true")
        trPr.append(tblHeader)
        return row

    def shade_cells(self, cells, shade):
        for cell in cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcVAlign = OxmlElement("w:shd")
            tcVAlign.set(qn("w:fill"), shade)
            tcPr.append(tcVAlign)

    def write_document(self):
        self.doc.save(self.word_output_file)


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    profiles = os.path.join(dir_path, "data")

    #
    # for domain in os.listdir(folder):
    #     domain_folder = os.path.join(folder, domain)
    #     if os.path.isdir(domain_folder) or os.path.islink(domain_folder):
    #         url = "https://{}".format(domain)
    #         t = None  # test_doc.docx   seo_doc.docx
    #         d = Domain(url)
    #         m = CreateWord(url, domain, t)

    profile = os.path.join(profiles, "oesterbaron.nl")
    config_file = os.path.join(profile, "config.yml")
    c = readConfig(config_file)
    m = CreateWord(c.config)
    m.print_table_styles()
    # m.print_paragraph_styles()
    # m.print_list_styles()
