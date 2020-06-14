import sys
import os
import logging

from .docx_graphs import DocxGraphs

class DocxGoogleSearch:

    def __init__(self, doc=None, dimension_data=None, graph_folder=None):
        try:
            if doc is None or dimension_data is None:
                raise Exception("Doc is None")

            self.doc = doc
            self.dimension_data = dimension_data
            self.graph_folder = graph_folder

            self.doc.add_page_break()
            self.doc.add_heading('Prestatie rapport', level=1)

            self.doc.add_paragraph("In het prestatierapport worden belangrijke statistieken weergegeven over hoe je "
                                   "site presteert in de resultaten van Google Zoeken: hoe vaak je site wordt "
                                   "weergegeven, gemiddelde positie in de zoekresultaten, klikfrequentie en eventuele "
                                   "speciale functies (zoals uitgebreide resultaten) die zijn gekoppeld aan je "
                                   "resultaten. Gebruik deze informatie om de zoekprestaties van je site te "
                                   "verbeteren. Zo kun je bijvoorbeeld:")

            self.doc.add_paragraph(
                'bekijken hoe je zoekverkeer in de loop van de tijd verandert, waar het vandaan komt en voor welke '
                'zoekopdrachten je website waarschijnlijk wordt weergegeven,', style='List Bullet'
            ).bold = True
            self.doc.add_paragraph(
                'een beter beeld krijgen van welke zoekopdrachten via smartphones worden uitgevoerd en deze informatie '
                'gebruiken voor betere targeting van mobiele apparaten,', style='List Bullet'
            ).bold = True
            self.doc.add_paragraph(
                'bekijken welke pagina\'s de hoogste (en laagste) klikfrequentie hebben in de resultaten van '
                'Google Zoeken.', style='List Bullet'
            ).bold = True

            self.doc.add_paragraph("Dit hoofstuk is opgedeeld in 4 "
                                      "onderdelen: zoekwoorden in het algemeen, zoekopdrachten per land, zoekopdrachten per "
                                      "apparaatsoort en zoekopdrachten met getoonde pagina's. De resultaten zijn over de "
                                      "afgelopen 30 dagen.")

            self.doc.add_paragraph()

            self.create_pie_graphs()

            try:
                self.dimension_data['country']
                self.countries()
            except KeyError:
                raise Exception("No google search console country data")

            try:
                self.dimension_data['page']
                self.pages()
            except KeyError:
                raise Exception("No google search console page data")

            try:
                self.dimension_data['query']
                self.searchwords()
            except KeyError:
                raise Exception("No google search console searchwords data")

            try:
                self.dimension_data['device']
                self.devices()
            except KeyError:
                raise Exception("No google search console deivce data")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def searchwords(self):
        try:
            self.doc.add_heading("Zoekwoorden", 1)
            self.doc.add_paragraph("Vertegenwoordigt de zoekopdrachten/woorden waarnaar gebruikers op Google hebben "
                                   "gezocht. Alleen zoekopdrachten die je site hebben geretourneerd, worden "
                                   "weergegeven.")
            self.doc.add_paragraph()

            dimension = 'query'
            data = self.dimension_data[dimension][0]['rows']
            self.create_table(data, 'Zoekwoord', 20)
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def countries(self):
        try:
            self.doc.add_heading('Zoek resultaten per land', 1)
            self.doc.add_paragraph("Het land waar de zoekopdracht vandaan kwam; bijvoorbeeld Nederland of België.")
            self.doc.add_paragraph()
            dimension = 'country'

            data = self.dimension_data[dimension][0]['rows']

            self.create_table(data, 'Land', 5)
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def pages(self):
        try:
            self.doc.add_heading("Zoek resultaten met getoonde pagina's", 1)
            self.doc.add_paragraph("De uiteindelijke URL/pagaina die is gekoppeld aan een Google zoekresultaat.")
            self.doc.add_paragraph()
            dimension = 'page'
            data = self.dimension_data[dimension][0]['rows']
            self.create_table(data, 'Url', 5)
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def devices(self):
        try:
            self.doc.add_heading("Zoek resultaten per apparaat", 1)
            self.doc.add_paragraph("Het type apparaat waarop de gebruiker zoekt: computer, tablet of mobiel.")
            self.doc.add_paragraph()
            dimension = 'device'

            data = self.dimension_data[dimension][0]['rows']
            self.create_table(data, 'Apparaat', 5)
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None

    def create_table(self, data=None, title=None, nr=5):
        try:
            if data == title is None:
                raise Exception("Data or Title is None")

            self.doc.add_heading("Klikken, Vertoningen & Zoekresultaatpositie", 2)
            self.doc.add_paragraph()
            table = self.doc.add_table(rows=1, cols=4, style="Grid Table 4 Accent 5")
            heading_cells = table.rows[0].cells
            heading_cells[0].text = title
            heading_cells[1].text = "Klikken"
            heading_cells[2].text = "Vertoningen"
            heading_cells[3].text = "Positie"

            for r in data[:nr]:
                row_cells = table.add_row().cells
                row_cells[0].text = r['keys'][0]
                row_cells[1].text = str(round(r['clicks']))
                row_cells[2].text = str(round(r['impressions']))
                row_cells[3].text = str(round(r['position']))

            self.auto_cell(table)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False

    def auto_cell(self, table):
        for r in table.rows:
            for c in r._tr.tc_lst:
                tcW = c.tcPr.tcW
                tcW.type = 'auto'
                tcW.w = 0

    def create_pie_graphs(self):
        try:
            g = DocxGraphs(self.graph_folder)

            dimension = 'device'
            data = self.dimension_data[dimension][0]['rows']
            pie_data = self.get_pie_data(data, 'clicks')
            if pie_data is not None:
                g.search_console_pie(pie_data, "Apparaat kliks", "apparaat_clicks.png")

            pie_data = self.get_pie_data(data, 'impressions')
            if pie_data is not None:
                g.search_console_pie(pie_data, "Apparaat vertoningen", "apparaat_impressions.png")

        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return False

    def get_pie_data(self, data, c_i="clicks"):
        pie_data = {}
        for d in data:
            pie_data[d['keys'][0]] = d[c_i]

        return pie_data
