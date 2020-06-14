import os
import sys
import logging


class EerstePagina:
    def __init__(self, doc=None, sc=0, domain=None):
        try:
            if doc is None:
                raise Exception("Doc is None")

            section = doc.sections[sc]  # 1e pagina
            doc.add_heading('Website-rapport voor', 0)
            doc.add_paragraph('{}'.format(domain))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.warning(str(e) + " | " + str(exc_type) + " | " + str(fname) + " | " + str(exc_tb.tb_lineno))
            return None
