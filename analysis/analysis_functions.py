"""

"""

from document import document


class Analyzer:

    def __init__ (self, article_list):

        #  Validate the input list
        is_valid = Validate_Article_List (article_list)
        if not is_valid:
            raise AttributeError ("The input list is not empty or it contains objects other than articles")

        self.article_list = article_list


    def add_article_list (self, article_list):

        #  Validate the input list
        is_valid = Validate_Article_List(article_list)
        if not is_valid:
            raise AttributeError("The input list is not empty or it contains objects other than articles")

        #  Concat the two list
        self.article_list.concat (article_list)

        #  Erase any duplicates
        self.article_list = Remove_Duplicates (article_list)


def Remove_Duplicates (article_list):
    """
    Remove any duplicates in a list of article
    :param article_list:
    :return:
    """

    for i in range (len (article_list)):
        article_1  = article_list [i]
        title_1    = article_1.fields ["title"]
        doi_1      = article_1.fields ["doi"]
        abstract_1 = article_1.fields ["abstract"]

        for j in range(i + 1, len (article_list)):
            article_2  = article_list [j]
            title_2    = article_2.fields ["title"]
            doi_2      = article_2.fields ["doi"]
            abstract_2 = article_2.fields ["abstract"]

            remove = None

            if title_1 == title_2:
                if doi_1 != doi_2:
                    if doi_1 == "":
                        remove = 1
                    elif doi_2 == "":
                        remove = 2
                elif abstract_1 != abstract_2:
                    if abstract_1 == "":
                        remove = 1
                    elif abstract_2 == "":
                        remove = 2
                    elif len (abstract_1) < len (abstract_2):
                        remove = 2
                    else:
                        remove = 1

            if doi_1 == doi_2:
                if title_1 != title_2:
                    if title_1 == "":
                        remove = 1
                    elif title_2 == "":
                        remove = 2

            if remove == 1:
                article_list.remove (article_1)
            elif remove == 2:
                article_list.remove (article_2)

    return article_list


def Validate_Article_List (article_list):
    """
    Validate the input list, assuring that it contains just articles or nothing at all
    :param article_list:
    :return: is_valid: bool
    """

    is_valid = True
    if article_list:
        for a in article_list:
            if not isinstance (a, document.Document):
                is_valid = False

    return is_valid
