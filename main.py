import json

import digital_libraries.ieee_digital_library
import digital_libraries.elsevier_digital_library
import digital_libraries.acm_digital_library
import digital_libraries.springer_digital_library
import search_string.search_string as ss


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    population   = []
    intervention = ["\"cloud continuum\"", "\"continuum of computing\"", "\"osmotic computing\""] # ["homogeneous AND \"cloud continuum\"", "cloud-edge", "\"cloud continuum\""]
    comparison   = []
    outcome      = ["\"SLR\"", "\"systematic literature review\"", "\"Systematic Literature Review\""] # ["\"code migration\""]
    context      = []

    search_str = ss.Search_String (population, intervention, comparison, outcome, context)

    """
    IEEE = digital_libraries.ieee_digital_library.IEEE_Digital_Library ('digital_libraries/api_config.json')
    IEEE.search_references ("continuum of computing")
    IEEE.convert_to_articles ()
    print (IEEE.articles_list)
    """


    Springer = digital_libraries.springer_digital_library.Springer_Digital_Library ('digital_libraries/api_config.json')
    Springer.search_references (search_str)
    # print (Springer.search_string.To_String())
    Springer.convert_to_articles ()
    # print (len (Springer.articles_list))
    for a in Springer.articles_list:
        print (a.print())


    """
    Elsevier = digital_libraries.elsevier_digital_library.Elsevier_Digital_Library ('digital_libraries/api_config.json')
    Elsevier.search_references (search_str)
    print (Elsevier.search_string.intervention)
    Elsevier.convert_to_articles ()
    print (Elsevier.articles_list)
    """

    """
    ACM = digital_libraries.acm_digital_library.ACM_Digital_library ()
    ACM.search_references (search_str)
    print (ACM.search_string.To_String())
    ACM.convert_to_articles ()
    print (ACM.articles_list)
    """

