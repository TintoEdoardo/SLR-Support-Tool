import json

from crossref.restful import Works
import digital_libraries.ieee_digital_library
import digital_libraries.elsevier_digital_library
import digital_libraries.acm_digital_library
import digital_libraries.springer_digital_library

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    """
    IEEE = digital_libraries.ieee_digital_library.IEEE_Digital_Library ('digital_libraries/api_config.json')
    IEEE.search_references ("continuum of computing")
    IEEE.convert_to_articles ()
    print (IEEE.articles_list)
    """

    """
    Springer = digital_libraries.springer_digital_library.Springer_Digital_Library ('digital_libraries/api_config.json')
    Springer.search_references ("continuum%20computing")
    Springer.convert_to_articles ()
    print (Springer.articles_list)
    """

    """
    Elsevier = digital_libraries.elsevier_digital_library.Elsevier_Digital_Library ('digital_libraries/api_config.json')
    Elsevier.search_references ("ALL%28cloud+AND+computing%29")
    Elsevier.convert_to_articles ()
    print (Elsevier.articles_list)
    """

    """
    ACM = digital_libraries.acm_digital_library.ACM_Digital_library ()
    ACM.search_references ("computing+AND+contiuum")
    ACM.convert_to_articles ()
    print (ACM.articles_list)
    """
