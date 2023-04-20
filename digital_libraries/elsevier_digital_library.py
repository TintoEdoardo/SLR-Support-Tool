"""
Elsevier Digital Library
API example: # https://api.elsevier.com/content/search/scopus?query=KEY%28cloud%29&apiKey=7f59af901d2d86f78a1fd60c1bf9426a
"""

import json
import requests
from document import document


class Elsevier_Digital_Library:

    apy_key            = ''
    json_articles_list = []
    articles_list      = []
    search_string      = None
    #  path_to_config = 'digital_libraries/api_config.json'

    def __init__ (self, path_to_config):
        #  Load the API key
        con_file = open (path_to_config)
        conf     = json.load (con_file)
        con_file.close()
        self.api_key  = conf ["elsevier_apikey"]


    def search_references (self, search_string):
        """
        Search for the query string provided through the IEEE online digital library
        :param search_string: string
        """

        self.search_string = search_string
        query_string = Convert_to_String (search_string)

        #  Compute and search for the input query
        base_url      = "https://api.elsevier.com/content/search/scopus"
        query_text    = "?query=" + query_string
        api_key_label = "apiKey=" + self.api_key
        headers       = {'Accept' : 'application/json'}
        query         = base_url + query_text + "&" + api_key_label

        #  Issue the request
        results = requests.get (query, headers=headers)

        #  Select and return only a specific field
        articles = json.loads (results.text)
        articles = articles ["search-results"] ["entry"]

        #  Acquire the abstracts, the list of authors ant the keywords
        for art in articles:

            #  Abstract retrival
            doi             = art ["prism:doi"]
            abstract_query  = 'https://api.elsevier.com/content/abstract/doi/'
            abstract_query += doi + "?" + api_key_label
            abstract_re     = requests.get (abstract_query, headers=headers)
            abstract_json   = json.loads (abstract_re.text)
            abstract        = Acquire_if_Any \
                (["abstracts-retrieval-response", "coredata", "dc:description"], abstract_json)

            #  Authors retrival
            authors = Acquire_if_Any (["abstracts-retrieval-response", "authors", "author"], abstract_json)

            #  Keywords retrival
            keywords      = []
            keywords_json = Acquire_if_Any (["abstracts-retrieval-response", "idxterms", "mainterm"], abstract_json)
            if keywords_json != [""]:
                for kj in keywords_json:
                    keyword = kj ["$"]
                    keywords.append (keyword)

            #  Update the dict entity
            art.update ({"authors"  : authors})
            art.update ({"abstract" : abstract})
            art.update ({"keywords" : keywords})

        self.json_articles_list = articles


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
    search_query = search_query.\
        replace (" ", "+"). \
        replace ("(", "%28"). \
        replace (")", "%29")

    return search_query


def Convert_to_Article (dict_article):
    """
    :param dict_article:
    :return Article
    """

    #   Acquire the relevant fields
    identifier       = Acquire_if_Any (["dc:identifier"],         dict_article).pop ()
    creators         = Acquire_if_Any (["authors"],               dict_article)
    publication_name = Acquire_if_Any (["prism:publicationName"], dict_article).pop ()
    title            = Acquire_if_Any (["dc:title"],              dict_article).pop ()
    volume           = Acquire_if_Any (["prism:volume"],          dict_article).pop ()
    number           = Acquire_if_Any (["prism:issueIdentifier"], dict_article).pop ()
    pages            = Acquire_if_Any (["prism:pageRange"],       dict_article).pop ()
    abstract         = Acquire_if_Any (["abstract"],              dict_article).pop ()
    keywords         = Acquire_if_Any (["keywords"],              dict_article)
    doi              = Acquire_if_Any (["prism:doi"],             dict_article).pop ()
    issn             = Acquire_if_Any (["prism:issn"],            dict_article).pop ()
    pub_date         = Acquire_if_Any (["prism:coverDate"],       dict_article).pop ()
    content_type     = Acquire_if_Any (["subtypeDescription"],    dict_article).pop ()
    year, month, day = Acquire_Year_Month_Day (pub_date)

    #  Process the most complex results
    author = []
    for creator in creators:
        surname    = Acquire_if_Any (["preferred-name", "ce:surname"], creator).pop ()
        first_name = Acquire_if_Any (["preferred-name", "ce:initials"], creator).pop ()
        name       = surname + ", " + first_name
        author.append (name)
    author   = " and ".join (author)
    keywords = ", ".join (keywords)
    if pages is None:
        pages = ""

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

    return  ref


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
        if inner_dict is not None and key in inner_dict:
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

    year, month, day = publication_date.split ('-')

    for m in months:
        if month == m ['number']:
            month = m ['name']

    return year, month, day
