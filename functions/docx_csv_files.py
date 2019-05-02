import os

from docx import Document
from docx.shared import RGBColor, Inches, Cm, Pt

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_COLOR_INDEX
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL

from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from functions.csv_files import ParceCSV

class CSV2Docx:
    def __init__(self, config=None, doc=None, frog_data_folder=None):
        if config is None:
            return
        if doc is None:
            return
        if frog_data_folder is None:
            return

        crawl_files = [i for i in config['crawl_files'] if not (i['active'] == 0)]

        doc.add_heading('Crawl overzichten', 0)
        doc.add_paragraph("Hier vind u alle informatie behorende bij het algemene overzicht. "
                               "Deze informatie geeft u meer inzicht in wat u inhoudelijk aan uw "
                               "pagina's dient te wijzigen om betere SEO resultaten te krijgen.")

        for cf in crawl_files:

            doc.add_paragraph()

            file = os.path.join(frog_data_folder, cf['file'])
            c = ParceCSV(file)

            for key, val in c.ready_data.items():
                if len(val['data']) == 0:
                    continue

                if cf['name'] == "":
                    doc.add_heading(key, 1)
                else:
                    doc.add_heading(cf['name'], 1)

                doc.add_paragraph(cf['description'])

                kolommen = len(cf['columns'])
                table = doc.add_table(rows=1, cols=kolommen)
                hdr_cells = table.rows[0].cells
                self.set_repeat_table_header(table.rows[0])
                i = 0
                for h in cf['columns']:
                    cell = hdr_cells[i]
                    paragraph = cell.paragraphs[0]
                    runner = paragraph.add_run(h)
                    runner.font.size = Pt(9)
                    i += 1

                for d in val['data']:
                    row_cells = table.add_row().cells
                    i = 0
                    for h in cf['columns']:
                        cell = row_cells[i]
                        paragraph = cell.paragraphs[0]
                        runner = paragraph.add_run(str(d[h]))
                        runner.font.size = Pt(9)
                        i += 1

                self.auto_cell(table)

    def auto_cell(self, table):
        for r in table.rows:
            for c in r._tr.tc_lst:
                tcW = c.tcPr.tcW
                tcW.type = 'auto'
                tcW.w = 0

    def set_repeat_table_header(self, row):
        """ set repeat table row on every new page
        """
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        tblHeader = OxmlElement('w:tblHeader')
        tblHeader.set(qn('w:val'), "true")
        trPr.append(tblHeader)
        return row
