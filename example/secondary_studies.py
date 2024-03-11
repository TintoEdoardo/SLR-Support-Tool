"""

"""

import analysis.screening_functions as sf
from example.paths_and_constants import libraries, secondary_studies_working_directory, path_to_keywords

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for library in libraries:

        postfix              = "_title_eval"
        path_to_bibliography = secondary_studies_working_directory + library + ".json"
        keywords             = path_to_keywords + "secondary_studies.json"

        #  Initialize the screener
        Screener = sf.Content_Screener (path_to_bibliography)
        Screener.read_article_from_bibliography ()

        #  Read the relevance keys (aka weighted keywords)
        Screener.read_relevance_keys_from (keywords)

        #  Assign a grade to each article w.r.t. the relevance keys
        Screener.assign_relevance_without_pdfs ()

        #  Save the result
        Screener.save_result_in_file (secondary_studies_working_directory, library)
