"""

"""

import json
import os
from pypdf import PdfReader


class Content_Screener:

    def __init__ (self, path_to_pdfs, path_to_bibliography):

        self.path_to_pdfs         = path_to_pdfs
        self.path_to_bibliography = path_to_bibliography
        self.article_list         = []


    def read_article_from_bibliography (self):

        csl_json_file     = open (self.path_to_bibliography, 'r')
        self.article_list = json.loads (csl_json_file.read ())
        csl_json_file.close ()


    def assign_relevance (self, relevance_keys):
        """
        :param: relevance_keys: [ {key, weight, loc = <title/abstract/full_body> },  ]
        """

        #  Import the list of PDFs name
        pdf_name_list = os.listdir (self.path_to_pdfs)

        for article in self.article_list:

            #  Initial relevance score
            score = 0

            #  Search for the PDF corresponding to the article
            title    = article ["title"] [:30]
            pdf_name = None
            for name in pdf_name_list:
                if name.find (title) != -1:
                    pdf_name = name

            #  Read the PDF file
            path_to_pdf = os.path.join (self.path_to_pdfs, pdf_name)
            reader      = PdfReader (path_to_pdf)

            for page in reader.pages:

                target    = None
                full_body = page.extract_text ()

                for key in relevance_keys:

                    #  Choose the right target
                    if key['loc'] == 'title':
                        target = article['title']
                    elif key['loc'] == 'abstract':
                        target = article['abstract']
                    elif key['loc'] == 'full_body':
                        target = full_body

                    #  Compute the score
                    point  = target.lower ().count (key ['key'])
                    score += point * float (key ['weight'])

            number_of_pages = len (reader.pages)

            #  Finally divide the score on the number of pages
            score = score / number_of_pages

            if "note" in article:
                article ["note"] = score
            else:
                article.update ({'note' : score})
