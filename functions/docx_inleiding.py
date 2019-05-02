
class inleiding:
    def __init__(self, doc=None, domain=""):
        if doc is None:
            return False

        doc.add_page_break()
        doc.add_heading("Uw website-rapport voor {}".format(domain), level=1)
        doc.add_paragraph()
        doc.add_paragraph("Een trage niet-presterende (mobiele) site kan de "
                           "klanttevredenheid en uw inkomsten beïnvloeden. "
                           "Dit rapport beoordeelt de prestaties van {} "
                           "en biedt oplossingen om u te helpen uw site te verbeteren.".format(domain))

        doc.add_paragraph()

        doc.add_paragraph("Dit rapport helpt u de volgende vragen te beantwoorden:")

        doc.add_paragraph()

        doc.add_paragraph(
            'Hoe is mobiele ervaring van uw site?', style='List Bullet'
        ).bold = True
        doc.add_paragraph(
            'Hoe is de SEO-gesteldheid van uw site?', style='List Bullet'
        ).bold = True
        doc.add_paragraph(
            'Hoe is de technische gesteldheid van uw site?', style='List Bullet'
        ).bold = True
        doc.add_paragraph(
            'Hoe is de snelheid van uw site?', style='List Bullet'
        ).bold = True
