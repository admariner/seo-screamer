class EerstePagina:
    def __init__(self, doc=None, sc=0, domain=None):
        if doc is None:
            return False

        section = doc.sections[sc]  # 1e pagina
        doc.add_heading('Website-rapport voor', 0)
        doc.add_paragraph('{}'.format(domain))
