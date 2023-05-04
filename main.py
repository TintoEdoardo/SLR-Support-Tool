import json

import digital_libraries.ieee_digital_library
import digital_libraries.elsevier_digital_library
import digital_libraries.acm_digital_library
import digital_libraries.springer_digital_library
import search_string.search_string as ss
import analysis.screening_functions as sf


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    population   = []
    intervention = \
        ["\"cloud continuum\"", "\"continuum of computing\"",
         "\"osmotic computing\"", "\"edge continuum\"", "\"compute continuum\""]
    comparison   = []
    outcome      = ["\"code migration\"", "\"real-time\"", "\"predictability\"", "\"orchestration\""]
    context      = []

    search_str = ss.Search_String (population, intervention, comparison, outcome, context)

    path_to_bibliography = "bibliography/bibliography.json"
    path_to_pdfs         = "bibliography/PDFs"

    relevance_keys = [
        #  Continuum Edge/Cloud/Compute/Computing/Computation
        {'key': 'edge continuum',           'weight': '1', 'loc': 'full_body'},
        {'key': 'edgecontinuum',            'weight': '1', 'loc': 'full_body'},
        {'key': 'cloud continuum',          'weight': '1', 'loc': 'full_body'},
        {'key': 'cloudcontinuum',           'weight': '1', 'loc': 'full_body'},
        {'key': 'compute continuum',        'weight': '1', 'loc': 'full_body'},
        {'key': 'computecontinuum',         'weight': '1', 'loc': 'full_body'},
        {'key': 'computing continuum',      'weight': '1', 'loc': 'full_body'},
        {'key': 'computingcontinuum',       'weight': '1', 'loc': 'full_body'},
        {'key': 'continuum of computing',   'weight': '1', 'loc': 'full_body'},
        {'key': 'continuumofcomputing',     'weight': '1', 'loc': 'full_body'},
        {'key': 'continuum of computation', 'weight': '1', 'loc': 'full_body'},
        {'key': 'continuumofcomputation',   'weight': '1', 'loc': 'full_body'},

        #  Orchestration
        {'key': 'orchestration', 'weight': '0.5', 'loc': 'full_body'},
        {'key': 'orchestrator',  'weight': '0.5', 'loc': 'full_body'},
        {'key': 'choreography',  'weight': '0.5', 'loc': 'full_body'},

        #  Real-Time
        {'key': 'real-time', 'weight': '0.3', 'loc': 'full_body'},
        {'key': 'realtime',  'weight': '0.3', 'loc': 'full_body'},

        #  Predictable/Predictability
        {'key': 'predictable',    'weight': '0.5', 'loc': 'full_body'},
        {'key': 'predictability', 'weight': '0.5', 'loc': 'full_body'},

        #  Experiment/Experimental
        {'key': 'experiment',   'weight': '0.3', 'loc': 'full_body'},
        {'key': 'experiments',  'weight': '0.3', 'loc': 'full_body'},
        {'key': 'experimental', 'weight': '0.5', 'loc': 'full_body'},
        {'key': 'empirical',    'weight': '0.5', 'loc': 'full_body'},

        #  Secondary studies
        {'key': 'slr',                          'weight': '-1000', 'loc': 'title'},
        {'key': 'systematic review',            'weight': '-1000', 'loc': 'title'},
        {'key': 'systematicreview',             'weight': '-1000', 'loc': 'title'},
        {'key': 'systematic literature review', 'weight': '-1000', 'loc': 'title'},
        {'key': 'systematicliteraturereview',   'weight': '-1000', 'loc': 'title'},
        {'key': 'survey',                       'weight': '-1000', 'loc': 'title'}
    ]

    """
    IEEE = digital_libraries.ieee_digital_library.IEEE_Digital_Library ('digital_libraries/api_config.json')
    IEEE.search_references ("continuum of computing")
    IEEE.convert_to_articles ()
    print (IEEE.articles_list)
    """

    """
    Springer = digital_libraries.springer_digital_library.Springer_Digital_Library ('digital_libraries/api_config.json')
    Springer.search_references (search_str)
    # print (Springer.search_string.To_String())
    Springer.convert_to_articles ()
    print (len (Springer.articles_list))
    for a in Springer.articles_list:
        print (a.print())
    """

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

