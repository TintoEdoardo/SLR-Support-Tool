"""
Springer Digital Library
API example: http://api.springernature.com/meta/v2/json?q=%22cloud%20continuum%22&api_key=944137724f188cf771a90639370601b9
Documentation: https://dev.springernature.com/adding-constraints
"""

import requests
import json
from document import document


class Springer_Digital_Library:

    apy_key            = ''
    json_articles_list = []
    articles_list      = []
    search_string      = None

    def __init__ (self, path_to_config):
        #  Load the API key
        con_file = open (path_to_config)
        conf     = json.load(con_file)
        con_file.close()
        self.api_key  = conf ["springer_apikey"]


    def search_references (self, search_string):
        """
        Search for the query string provided through the IEEE online digital library
        :param search_string: string
        """

        self.search_string = search_string
        query_string = Convert_to_String (search_string)

        #  Compute and search for the input query
        base_url     = "http://api.springernature.com/meta/v2/json"
        query_text   = "?p=100&q=" + query_string # "?p=100&q=%22" + query_string + "%22"
        and_op       = "&"
        api_label    = "api_key="
        query        = base_url + query_text + and_op + api_label + self.api_key
        query_result = requests.get (query)

        #  Select and return only the 'articles' field
        articles = json.loads (query_result.text)

        self.json_articles_list = articles ["records"]


    def convert_to_articles (self):
        """
        Take the list of Json articles and convert them into a list of Article objects
        :return: list (list (str))
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

    #  Further elaboration is required
    # search_query = search_query. \
        # replace (" ", "%20"). \
        # replace ("(", "%28"). \
        # replace (")", "%29")

    return search_query


def Convert_to_Article (dict_article):
    """
    :param dict_article:
    :return Article
    """

    #   Acquire the relevant fields
    identifier       = Acquire_if_Any (["identifier"],      dict_article).pop ()
    creators         = Acquire_if_Any (["creators"],        dict_article)
    publication_name = Acquire_if_Any (["publicationName"], dict_article).pop ()
    title            = Acquire_if_Any (["title"],           dict_article).pop ()
    volume           = Acquire_if_Any (["volume"],          dict_article).pop ()
    number           = Acquire_if_Any (["number"],          dict_article).pop ()
    start_page       = Acquire_if_Any (["startingPage"],    dict_article).pop ()
    end_page         = Acquire_if_Any (["endingPage"],      dict_article).pop ()
    abstract         = Acquire_if_Any (["abstract"],        dict_article).pop ()
    keywords         = Acquire_if_Any (["keyword"],         dict_article)
    doi              = Acquire_if_Any (["doi"],             dict_article).pop ()
    issn             = Acquire_if_Any (["issn"],            dict_article).pop ()
    pub_date         = Acquire_if_Any (["publicationDate"], dict_article).pop ()
    content_type     = Acquire_if_Any(["contentType"],      dict_article).pop ()
    year, month, day = Acquire_Year_Month_Day (pub_date)

    #  Process the most complex results
    if creators != [""]:
        author = [c ["creator"] for c in creators]
    else:
        author = ""
    author   = ' and '.join (author)
    keywords = ", ".join (keywords)
    pages    = start_page + "-" + end_page

    #  Allocate a new object to group all the
    #  parameters of a reference
    ref = document.Document \
        (identifier,
         content_type,
         author,
         title,
         abstract,
         doi,
         publication_name,
         str (year),
         month,
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


def Acquire_Year_Month_Day (publication_date):
    """
    :param publication_date: str
    :return: month: str
    """
    months = [
        {'name' : 'January',   'number' : '1'},
        {'name' : 'February',  'number' : '2'},
        {'name' : 'March',     'number' : '3'},
        {'name' : 'April',     'number' : '4'},
        {'name' : 'May',       'number' : '5'},
        {'name' : 'June',      'number' : '6'},
        {'name' : 'July',      'number' : '7'},
        {'name' : 'August',    'number' : '8'},
        {'name' : 'September', 'number' : '9'},
        {'name' : 'October',   'number' : '10'},
        {'name' : 'November',  'number' : '11'},
        {'name' : 'December',  'number' : '12'}
    ]

    year, day, month = publication_date.split ('-')

    for m in months:
        if month == m ['number']:
            month = m ['name']

    return year, month, day
