from .docx_graphs import DocxGraphs

class DocxGoogleSearch:
    def _init__(self, doc=None, dimension_data=None, graph_folder=None):
        if doc is None or dimension_data is None:
            return

        self.doc = doc
        self.dimension_data = dimension_data
        self.graph_folder = self.graph_data_folder

        self.doc.add_heading('Prestatie rapport', 0)

        self.doc.add_paragraph("In het prestatierapport worden belangrijke statistieken weergegeven over hoe je site "
                               "presteert in de resultaten van Google Zoeken: hoe vaak je site wordt weergegeven, "
                               "gemiddelde positie in de zoekresultaten, klikfrequentie en eventuele speciale "
                               "functies (zoals uitgebreide resultaten) die zijn gekoppeld aan je resultaten. Gebruik "
                               "deze informatie om de zoekprestaties van je site te verbeteren. Zo kun je bijvoorbeeld:"
                               "bekijken hoe je zoekverkeer in de loop van de tijd verandert, waar het vandaan komt "
                               "en voor welke zoekopdrachten je website waarschijnlijk wordt weergegeven,"
                               "een beter beeld krijgen van welke zoekopdrachten via smartphones worden uitgevoerd en "
                               "deze informatie gebruiken voor betere targeting van mobiele apparaten,"
                               "bekijken welke pagina's de hoogste (en laagste) klikfrequentie hebben in de resultaten "
                               "van Google Zoeken.")

        self.doc.add_paragraph("Dit hoofstuk is opgedeeld in 4 "
                                  "onderdelen: zoekwoorden in het algemeen, zoekopdrachten per land, zoekopdrachten per "
                                  "apparaatsoort en zoekopdrachten met getoonde pagina's. De resultaten zijn over de "
                                  "afgelopen 30 dagen.")

        self.doc.add_paragraph()

        self.create_pie_graphs()

        self.countries()
        self.pages()
        self.searchwords()
        self.devices()

    def searchwords(self):
        self.doc.add_heading("Zoekwoorden", 1)
        self.doc.add_paragraph("")
        self.doc.add_paragraph()

        dimension = 'query'
        data = self.dimension_data[dimension][0]['row']
        self.create_table(data, 'Zoekwoord', 20)

    def countries(self):
        self.doc.add_heading('Zoek resultaten per land', 1)
        self.doc.add_paragraph("")
        self.doc.add_paragraph()
        dimension = 'country'

        data = self.dimension_data[dimension][0]['row']

        self.create_table(data, 'Land', 5)

    def pages(self):
        self.doc.add_heading("Zoek resultaten met getoonde pagina's", 1)
        self.doc.add_paragraph("")
        self.doc.add_paragraph()
        dimension = 'page'

        data = self.dimension_data[dimension][0]['row']
        self.create_table(data, 'Url', 5)

    def devices(self):
        self.doc.add_heading("Zoek resultaten per apparaat", 1)
        self.doc.add_paragraph("")
        self.doc.add_paragraph()
        dimension = 'device'

        data = self.dimension_data[dimension][0]['row']
        self.create_table(data, 'Apparaat', 5)

    def create_table(self, data=None, title=None, nr=5):
        if data is None or title is None:
            return

        self.doc.add_heading("Klikken, Vertoningen & Zoekresultaatpositie", 2)
        self.doc.add_paragraph("Het aantal klikken afkomstig van een zoekresultaat van Google search waarmee de gebruiker op je site is terechtgekomen.")
        self.doc.add_paragraph("Hoeveel links naar je site een gebruiker zag op de pagina met zoekresultaten van Google Zoeken. Vertoningen worden geteld wanneer de gebruiker die pagina met resultaten bezoekt, zelfs wanneer de gebruiker niet naar het resultaat is gescrold. Als een gebruiker echter alleen pagina 1 bekijkt en het resultaat op pagina 2 staat, telt die vertoning niet mee.")
        self.doc.add_paragraph("De gemiddelde positie van het hoogste resultaat van de site. Als je site bijvoorbeeld drie resultaten heeft op posities 2, 4 en 6, wordt de positie gerapporteerd als 2. Belangrijk is dat deze waarde zo laag mogelijk is, hoe lager hoe hoger in de zoek resultaten.")
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
            row_cells[1].text = r['clicks']
            row_cells[2].text = r['impressions']
            row_cells[3].text = r['position']

    def create_pie_graphs(self):
        g = DocxGraphs(self.graph_folder)

        dimension = 'device'
        data = self.dimension_data[dimension][0]['row']
        pie_data = self.get_pie_data(data, 'clicks')
        g.search_console_pie(pie_data, "Apparaat kliks", "apparaat_clicks.png")

        pie_data = self.get_pie_data(data, 'impressions')
        g.search_console_pie(pie_data, "Apparaat vertoningen", "apparaat_impressions.png")

    def get_pie_data(self, data, c_i="clicks"):
        pie_data = {}
        for d in data:
            pie_data[d['keys'][0]] = d[c_i]

        return pie_data
