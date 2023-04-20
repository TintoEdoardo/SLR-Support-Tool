"""
ACM Digital Library
Not any API available
"""

import json
import requests
import re
from document import document


class ACM_Digital_library:

    list_of_doi        = []
    json_articles_list = []
    articles_list      = []
    search_string      = None

    def acquire_list_of_doi (self, url):
        """
        :param url: string
        :return: list_of_doi: list (string)
        """
        page_number = 0
        page_size   = 50
        no_more_res = False
        list_of_doi = []
        start_tag   = "input name=\""
        end_tag     = "\" class="

        #  Iterate until the list of result is empty
        while not no_more_res:
            #  Compute the current page tag
            page_tag = '&startPage=' + str(page_number) \
                       + '&pageSize=' + str(page_size)
            query    = url + page_tag

            current_page      = requests.get (query)
            curr_page_content = current_page.text

            #  Check if the current page is empty
            if curr_page_content.count ("input name") == 0:
                #  If so, the iteration end here
                no_more_res = True
            else:
                page_number += 1

                #  Check for all the results in the page
                end_of_list = False
                while not end_of_list:
                    #  We search for the starting tag
                    index_start = curr_page_content.find (start_tag)
                    if index_start == -1:
                        #  If it can not be found, the list is over
                        end_of_list = True
                    else:
                        #  Otherwise, extract the DOI
                        index_start      += len (start_tag)
                        curr_page_content = curr_page_content [index_start:]
                        index_end         = curr_page_content.find (end_tag)
                        extracted_doi     = curr_page_content [0:index_end]
                        #  And clear the input string up to the current point
                        index_del         = index_end + len (end_tag)
                        curr_page_content = curr_page_content [index_del:]
                        #  Append the newly found doi
                        list_of_doi.append (extracted_doi)

        #  Finally, return the list of DOI
        self.list_of_doi = list_of_doi


    def search_references (self, search_string):
        """
        Search for the query string provided through the IEEE online digital library
        :param search_string: Search_String
        """

        self.search_string = search_string
        query_string = Convert_to_String (search_string)

        #  Compute the URL
        base_url     = "https://dl.acm.org/action/doSearch?AllField="
        expand_tag   = "&expand=all"
        url = base_url + query_string + expand_tag

        #  Acquire the list of doi
        self.acquire_list_of_doi (url)
        articles     = []

        for doi in self.list_of_doi:
            #  Acquire metadata and abstract
            article_metadata = Get_Data_From_Doi (doi)
            if "message" in article_metadata:
                articles.append (article_metadata ["message"])

        self.json_articles_list = articles


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

    #  Further elaboration is required
    search_query = search_query.replace (" ", "+")

    return search_query


def Get_Data_From_Doi (doi):
    """
    :param doi: string
    :return: metadata: string in JSON
    """
    #  Acquire the abstract of the document
    base_url     = "https://dl.acm.org/doi/"
    url          = base_url + doi
    article_page = requests.get (url) .text

    #  In some occasions, the ISBN is needed also
    #  (for example for doctoral thesis)
    start_tag_isbn = "ISBN:"
    end_tag_isbn   = "Order Number:"
    isbn_pattern   = start_tag_isbn + "(.*)" + end_tag_isbn
    isbn_match     = re.findall (isbn_pattern, article_page)
    isbn           = -1

    #  If the isbn_match is empty, simply discard the value.
    #  Hopefully, if no ISBN is available, the DOI will be
    if len (isbn_match) == 0:
        pass
    else:
        isbn = isbn_match [0]
        isbn = isbn\
            .replace ("<p>", "")\
            .replace ("</p>", "")\
            .replace ("<div>", "")\
            .replace ("</div>", "") \
            .replace ("\t", "") \
            .replace ("\n", "") \
            .replace("</span>", "") \
            .replace ("<span class=\"bold\">", "") \
            .replace ("<span class=\"space\">", "")

    #  Unfortunately, different tags are applied for abstracts.
    #  Hence, we should check for any of them

    #  1
    start_tag = "Abstract</h2>"
    end_tag = "<!-- /abstract content -->"
    pattern = start_tag + "(.*)" + end_tag
    abs_list = re.findall(pattern, article_page, flags=re.DOTALL)

    # 2
    if len (abs_list) == 0:
        start_tag = "<div class=\"abstractSection abstractInFull\">"
        end_tag   = "<!-- /abstract content -->"
        pattern   = start_tag + "(.*)" + end_tag
        abs_list  = re.findall (pattern, article_page, flags=re.DOTALL)

    # 3
    if len (abs_list) == 0:
        start_tag = "<div class=\"abstractSection\">Abstract"
        end_tag   = "<div id=\"tableOfContent\">"
        pattern = start_tag + "(.*)" + end_tag
        abs_list = re.findall(pattern, article_page, flags=re.DOTALL)

    #  Convert to a string and clean the output
    if len (abs_list) > 0:
        abstract = abs_list [0]
    else:
        abstract = ""
    abstract = abstract \
        .replace("<i>", "") \
        .replace("</i>", "") \
        .replace ("<p>", "") \
        .replace ("</p>", "") \
        .replace ("<div>", "") \
        .replace ("</div>", "") \
        .replace ("\t", "") \
        .replace ("\n", "") \
        .replace ("<div class=\"abstractSection abstractInFull\">", "")

    #  Remove any remaining tag
    abstract = re.sub ("<(.*)>", "", abstract, flags=re.DOTALL)

    #  Acquire metadata
    cross_ref_url = "https://api.crossref.org/works/"
    url_md        = cross_ref_url + doi
    response      = requests.get (url_md) .text

    #  Some publications might not be found through crossref;
    #  in this case, only the ISBN is saved
    if response == "Resource not found.":
        isbn_metadata = {"doi" : doi, "isbn" : isbn}
        metadata      = isbn_metadata
    else:
        metadata = json.loads (response)

    #  Add the abstract
    abs_metadata  = {"abstract" : abstract}
    doi_metadata  = {"doi"      : doi}
    metadata.update (abs_metadata)
    metadata.update (doi_metadata)

    return metadata


def Convert_to_Article (dict_article):
    """
    :param dict_article:
    :return Article
    """

    #   Acquire the relevant fields
    identifier     = dict_article ["DOI"]
    authors        = []
    for author in dict_article ["author"]:
        surname  = author ["family"]
        name     = author ["given"]
        surname_comma_init_name = surname + ', ' + name
        authors.append (surname_comma_init_name)

    publication_name     = Acquire_if_Any  ("container-title",       dict_article)
    title                = Acquire_if_Any  ("title",                 dict_article)
    volume               = Acquire_if_Any  ("volume",                dict_article)
    number               = Acquire_if_Any  ("number",                dict_article)
    pages                = Acquire_if_Any  ("page",                  dict_article)
    abstract             = Acquire_if_Any  ("abstract",              dict_article)
    keywords             = Acquire_if_Any  ("subject",               dict_article),
    doi                  = Acquire_if_Any  ("doi",                   dict_article)
    issn                 = Acquire_if_Any  ("ISSN",                  dict_article)
    pub_date             = Acquire_if_Any  ("published",            dict_article)
    content_type         = Acquire_if_Any  ("type",                 dict_article)
    year, month, day     = Acquire_Year_Month_Day (pub_date)

    #  Allocate a new object to group all the
    #  parameters of a reference
    ref = document.Document \
        (identifier,
         content_type,
         " and ".join (authors),
         title,
         Clear_the_Abstract (abstract),
         doi,
         publication_name,
         year,
         month,
         volume,
         number,
         pages,
         ", ".join (keywords),
         issn)

    return ref


def Clear_the_Abstract (abstract):
    """
    :param abstract: str
    :return: res: str
    """
    res = abstract \
        .replace ("<jats:p>",  "") \
        .replace ("</jats:p>", "") \
        .replace ("\n",       "")

    #  Remove trailing spaces
    res = re.sub ("  +", "", res)

    return res


def Acquire_if_Any (key, dictionary):
    """
    :param key: str
    :param dictionary: dict
    :return: str
    """
    if key in dictionary:
        result = dictionary [key]
        if isinstance (result, list):
            return result [0]
        else:
            return result
    else:
        return ""


def Acquire_Year_Month_Day (publication_date):
    """
    :param publication_date: list (int)
    :return: month: str
    """

    publication_date = publication_date ['date-parts'] [0]
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

    date_len = len (publication_date)
    if date_len == 3:
        [year, month, day] = publication_date
    elif date_len == 2:
        [year, month] = publication_date
        day           = ""
    elif date_len == 1:
        [year] = publication_date
        month  = ""
        day    = ""
    else:
        year  = ""
        month = ""
        day   = ""


    year  = str (year)
    month = str (month)
    day   = str (day)

    if month != "":
        for m in months:
            if month == m ['number']:
                month = m ['name']

    return year, month, day
