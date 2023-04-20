"""

"""

fields_name = [
    "author",         # 0
    "title",          # 1
    "abstract",       # 2
    "doi",            # 3
    "book_title",     # 4
    "year",           # 5
    "month",          # 6
    "volume",         # 7
    "number",         # 8
    "pages",          # 9
    "keywords",       # 10
    "issn"            # 11
]


bibtex_tag = {
    fields_name[0]   : "author",    # "author"
    fields_name[1]   : "title",     # "title"
    fields_name[2]   : "abstract",  # "abstract"
    fields_name[3]   : "doi",       # "doi"
    fields_name[4]   : "booktitle", # "book_title"
    fields_name[5]   : "year",      # "year"
    fields_name[6]   : "month",     # "month"
    fields_name[7]   : "volume",    # "volume"
    fields_name[8]   : "number",    # "number"
    fields_name[9]   : "pages",     # "pages"
    fields_name[10]  : "keywords",  # "keywords"
    fields_name[11]  : "ISSN"       # "issn"
}


class Document:
    """
    article_number = ""
    content_type   = ""
    fields = {
    fields_name [0]   : "",  # "author"
    fields_name [1]   : "",  # "title"
    fields_name [2]   : "",  # "abstract"
    fields_name [3]   : "",  # "doi"
    fields_name [4]   : "",  # "book_title"
    fields_name [5]   : "",  # "year"
    fields_name [6]   : "",  # "month"
    fields_name [7]   : "",  # "volume"
    fields_name [8]   : "",  # "number"
    fields_name [9]   : "",  # "pages"
    fields_name [10]  : "",  # "keywords"
    fields_name [11]  : ""   #  "issn"
    }
    """

    def __init__ (self,
                 article_number,
                 content_type,
                 author,
                 title,
                 abstract,
                 doi,
                 book_title = "",
                 year       = "",
                 month      = "",
                 volume     = "",
                 number     = "",
                 pages      = "",
                 keywords   = "",
                 issn = ""):

        self.fields = {
            fields_name [0]   : "",  # "author"
            fields_name [1]   : "",  # "title"
            fields_name [2]   : "",  # "abstract"
            fields_name [3]   : "",  # "doi"
            fields_name [4]   : "",  # "book_title"
            fields_name [5]   : "",  # "year"
            fields_name [6]   : "",  # "month"
            fields_name [7]   : "",  # "volume"
            fields_name [8]   : "",  # "number"
            fields_name [9]   : "",  # "pages"
            fields_name [10]  : "",  # "keywords"
            fields_name [11]  : ""   #  "issn"
            }
        self.article_number  = article_number
        self.content_type    = content_type
        self.fields [fields_name [0]]  = author
        self.fields [fields_name [1]]  = title
        self.fields [fields_name [2]]  = abstract
        self.fields [fields_name [3]]  = doi
        self.fields [fields_name [4]]  = book_title
        self.fields [fields_name [5]]  = year
        self.fields [fields_name [6]]  = month
        self.fields [fields_name [7]]  = volume
        self.fields [fields_name [8]]  = number
        self.fields [fields_name [9]]  = pages
        self.fields [fields_name [10]] = keywords
        self.fields [fields_name [11]] = issn


    def article_type (self):
        """
        Output the Bibtex entity corresponding to the current content_type
        :return: article_type: str
        """
        content_type = self.content_type
        if content_type == "Conferences" \
                or content_type == "proceedings-article" \
                or content_type == "Chapter ConferencePaper":
            article_type = "@INPROCEEDINGS"

        elif content_type == "Article" \
                or content_type == "journal-article":
            article_type = "@ARTICLE"

        elif content_type == "book-chapter" \
                or content_type == "Chapter":
            article_type = "@INBOOK"

        else:
            article_type = "@MISC"
            #  raise AttributeError ("Content_type is unknown")

        return article_type


    def print (self):
        """
        Output the Bibtex field associated with the current article
        :return: output: str
        """
        article_type   = self.article_type ()
        article_number = self.article_number

        output = article_type + "{" + article_number
        for f_name in fields_name:
            if type (self.fields [f_name]) is not str:
                raise TypeError ("The future tag " + bibtex_tag [f_name] + "is not str")
            output += ",\n" + bibtex_tag [f_name] + "={" + self.fields [f_name] + "}"
        output += "}\n"

        return output

