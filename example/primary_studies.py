"""

"""

import analysis.screening_functions as sf
from example.paths_and_constants import libraries, primary_studies_working_directory, path_to_keywords

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for library in libraries:

        destination          = primary_studies_working_directory + library + "/"
        path_to_bibliography = primary_studies_working_directory + library + ".json"
        path_to_pdfs         = destination + "pdfs/"
        keywords             = path_to_keywords + "primary_studies.json"

        #  Initialize the screener
        Screener = sf.Content_Screener (path_to_bibliography, path_to_pdfs)
        Screener.read_article_from_bibliography ()

        #  Read the relevance keys (aka weighted keywords)
        Screener.read_relevance_keys_from (keywords)

        #  Assign a grade to each article w.r.t. the relevance keys
        Screener.assign_relevance ()

        #  Save the result
        Screener.save_result_in_file (destination, library)
