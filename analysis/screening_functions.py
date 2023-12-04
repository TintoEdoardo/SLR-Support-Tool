"""

"""

import json
import os
from pypdf import PdfReader


class Content_Screener:

    def __init__ (self, path_to_bibliography, path_to_pdfs=None):

        self.path_to_pdfs         = path_to_pdfs
        self.path_to_bibliography = path_to_bibliography
        self.article_list         = []
        self.relevance_keys       = []


    def read_article_from_bibliography (self):

        csl_json_file     = open (self.path_to_bibliography, 'r')
        self.article_list = json.loads (csl_json_file.read ())
        csl_json_file.close ()


    def read_relevance_keys_from (self, path_to_file):
        """
        :param: path_to_file: str
        """
        file                = open (path_to_file, 'r')
        self.relevance_keys = json.load (file)
        file.close ()

    def read_relevance_keys (self, relevance_keys):
        self.relevance_keys = relevance_keys
    def write_relevance_keys_to (self, path_to_file):
        """
        :param: path_to_file: str
        """
        file                 = open (path_to_file, 'w')
        relevance_key_to_str = json.dumps (self.relevance_keys, indent=1)
        file.write (relevance_key_to_str)
        file.close ()

    def assign_relevance (self, relevance_keys = None):
        """
        :param: relevance_keys: [ {key, weight, loc = <title/abstract/full_body> },  ]
        """

        if relevance_keys is None:
            relevance_keys = self.relevance_keys

        #  Import the list of PDFs name
        pdf_name_list = os.listdir (self.path_to_pdfs)

        for article in self.article_list:

            #  Initial relevance score
            score = 0

            #  Search for the PDF corresponding to the article
            title    = article ["title"] [:30]
            title    = title.replace (":", "")
            title    = title.replace ("?", "")
            title    = title.replace ("*", "")
            title    = title.replace ("/", "")
            pdf_name = None
            for name in pdf_name_list:
                if name.find (title) != -1:
                    pdf_name = name

            if pdf_name is None:
                score = -1
            else:
                #  Read the PDF file
                path_to_pdf = os.path.join (self.path_to_pdfs, pdf_name)
                reader      = PdfReader (path_to_pdf)

                for page in reader.pages:

                    target    = None
                    full_body = page.extract_text ()

                    for key in relevance_keys:

                        #  Choose the right target
                        if key ['loc'] == 'title':
                            target = article ['title']
                        elif key ['loc'] == 'abstract' and 'abstract' in article:
                            target = article ['abstract']
                        elif key ['loc'] == 'full_body':
                            target = full_body

                        #  Compute the score
                        point  = target.lower ().count (key ['key'])
                        score += point * float (key ['weight'])

                number_of_pages = len (reader.pages)

                #  Finally divide the score on the number of pages
                score     = score / number_of_pages

            #  Convert score to string
            score_str = "{0:.3f}".format (score)

            if "note" in article:
                article ["note"] = score_str
            else:
                article.update ({'note' : score_str})

    def assign_relevance_without_pdfs (self, relevance_keys = None):
        """
        :param: relevance_keys: [ {key, weight, loc = <title/abstract>},  ]
        """

        if relevance_keys is None:
            relevance_keys = self.relevance_keys

        for article in self.article_list:

            #  Initial relevance score
            score  = 0
            target = None

            for key in relevance_keys:

                #  Choose the right target
                if key ['loc'] == 'title':
                    if "title" in article:
                        target = article ['title']
                    else:
                        target = ""
                        score  = -1000
                elif key ['loc'] == 'abstract':
                    if "abstract" in article:
                        target = article ['abstract']
                    else:
                        target = ""
                        score  = -1000
                else:
                    if "title" in article and "abstract" in article:
                        target = article ['title'] + article ['abstract']
                    else:
                        continue

                #  Compute the score
                point = target.lower ().count (key ['key'])
                score += point * float (key ['weight'])

            #  Finally format the score
            score_str = "{0:.3f}".format (score)

            if "note" in article:
                article ["note"] = score_str
            else:
                article.update ({'note' : score_str})

    def save_result_in_file (self, destination, name):
        file = open (destination + name + '_csl_json.json', 'w')
        json.dump (self.article_list, file, indent=4)
        file.close ()

        title_eval_list = []
        for article in self.article_list:
            if not "title" in article:
                continue
            title_eval_list.append ({"title"      : article ["title"],
                                     "evaluation" : article ["note"]})
        sorted_title_eval_list = sorted (title_eval_list, key= lambda a : float (a ["evaluation"]), reverse=True)

        file = open (destination + name + '_title_eval.json', 'w')
        file.writelines (json.dumps (sorted_title_eval_list, indent=2))
        file.close ()
