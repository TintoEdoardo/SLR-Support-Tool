"""
IEEE XLibrary
API example: https://ieeexploreapi.ieee.org/api/v1/search/articles?querytext=(cloud%20AND%20continuum)&apiKey=cbmsq7mvf38hy9smvyybu24v
"""

import requests
import json
from document import document


class IEEE_Digital_Library:

    apy_key            = ''
    json_articles_list = []
    articles_list      = []
    search_string      = None
    #  path_to_config = 'digital_libraries/api_config.json'

    def __init__ (self, path_to_config):
        #  Load the API key
        con_file = open (path_to_config)
        conf     = json.load(con_file)
        con_file.close()
        self.api_key  = conf ["ieee_apikey"]


    def search_references (self, search_string):
        """
        Search for the query string provided through the IEEE online digital library
        :param search_string: string
        """

        self.search_string = search_string
        query_string = Convert_to_String (search_string)

        #  Compute and search for the input query
        base_url     = "https://ieeexploreapi.ieee.org/api/v1/search/articles?"
        query_text   = "querytext=(" + query_string + ")"
        and_op       = "&"
        api_label    = "apiKey="
        query        = base_url + query_text + and_op + api_label + self.api_key
        query_result = requests.get (query)

        #  Select and return only the 'articles' field
        articles = json.loads (query_result.text)

        self.json_articles_list = articles ["articles"]


    def convert_to_articles (self):
        """
        Take the list of Json articles and convert them into a list of Article objects
        :return: list (Article)
        """

        #  List of Article objects
        result = []

        for art in self.json_articles_list:
            #  Parse the input dictionary into ad Article
            ref = Convert_to_Article (art)

            #  Add the article into the result list
            result.append (ref)

        #  Store the result in the correct attribute
        self.articles_list = result


def Convert_to_String (search_string):
    """
    :param search_string: Search_String
    :return: search_query: string
    """

    #  Produce a general search query
    search_query = search_string.To_String ()

    #  No further elaboration is required
    return search_query


def Convert_to_Article (dict_article):
    """
    :param dict_article:
    :return Article
    """

    #   Acquire the article fields
    article_number = Acquire_if_Any (["article_number"],    dict_article).pop ()
    book_title     = Acquire_if_Any (["publication_title"], dict_article).pop ()
    title          = Acquire_if_Any (["title"],             dict_article).pop ()
    year           = Acquire_if_Any (["publication_year"],  dict_article).pop ()
    volume         = Acquire_if_Any (["volume"],            dict_article).pop ()
    number         = Acquire_if_Any (["number"],            dict_article).pop ()
    start_page     = Acquire_if_Any (["start_page"],        dict_article).pop ()
    end_page       = Acquire_if_Any (["end_page"],          dict_article).pop ()
    abstract       = Acquire_if_Any (["abstract"],          dict_article).pop ()
    doi            = Acquire_if_Any (["doi"],               dict_article).pop ()
    issn           = Acquire_if_Any (["issn"],              dict_article).pop ()
    pub_date       = Acquire_if_Any (["publication_date"],  dict_article).pop ()
    content_type   = Acquire_if_Any (["content_type"],      dict_article).pop ()
    authors        = Acquire_if_Any (["authors", "authors"],                 dict_article)
    keywords       = Acquire_if_Any (["index_terms", "ieee_terms", "terms"], dict_article)

    #  Process the most complex results
    author   = [auth ["full_name"] for auth in authors]
    keywords = ", ".join (keywords)
    pages    = start_page + "-" + end_page

    #  Allocate a new object to group all the
    #  parameters of a reference
    ref = document.Document \
        (article_number,
         content_type,
         Process_Authors (author),
         title,
         abstract,
         doi,
         book_title,
         str (year),
         Acquire_Month (pub_date),
         volume,
         number,
         pages,
         keywords,
         issn)

    return ref


def Acquire_if_Any (keys, dictionary):
    """
    If there is an element inside 'dictionary [keys [0]] [keys [1]] ... [keys [n]]'
    return its value, otherwise return an array containing an empty string
    :param keys: list (str)
    :param dictionary: dict
    :return: list (str)
    """
    inner_dict = dictionary
    keys_len   = len (keys)
    for i in range (keys_len):
        key = keys [i]
        if key in inner_dict:
            inner_dict = inner_dict [key]
            if i == keys_len - 1:
                if isinstance (inner_dict, list):
                    return inner_dict
                else:
                    return [inner_dict]
        else:
            return [""]


def Acquire_Month (publication_date):
    """
    :param publication_date: str
    :return: month: str
    """
    months = [
        {'name' : 'January',  'abbreviation' : 'Jan'},
        {'name' : 'February', 'abbreviation' : 'Feb'},
        {'name' : 'March',    'abbreviation' : 'Mar'},
        {'name' : 'April',    'abbreviation' : 'Apr'},
        {'name' : 'May',      'abbreviation' : 'May'},
        {'name' : 'June',     'abbreviation' : 'Jun'},
        {'name' : 'July',     'abbreviation' : 'Jul'},
        {'name' : 'August',   'abbreviation' : 'Aug'},
        {'name' : 'September', 'abbreviation' : 'Sep'},
        {'name' : 'October',   'abbreviation' : 'Oct'},
        {'name' : 'November',  'abbreviation' : 'Nov'},
        {'name' : 'December',  'abbreviation' : 'Dec'}
    ]

    month = ""
    for m in months:
        if publication_date.find (m ['name']) != -1:
            month = m ['name']

    return month


def Process_Authors (authors):
    """
    :param authors: list (str)
    :return: names_list: str
    """
    number_of_authors = len (authors)
    names_list = ""
    for i in range (number_of_authors):
        #  Split each full name into words (token)
        tokens = authors[i].split()

        #  Transform the name, compatibly with the
        #  target format (Bibtex)
        name   = tokens.pop() + ", " + ", ".join(tokens)

        #  Add ' and ' if other authors should
        #  be added
        if i < number_of_authors - 1:
            name += " and "
        names_list += name
    return names_list
