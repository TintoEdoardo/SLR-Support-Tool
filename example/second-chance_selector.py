"""

"""

import json
from example.paths_and_constants import libraries, second_chance_working_directory

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for library in libraries:

        postfix           = "_title_eval"
        source            = second_chance_working_directory + library + "/"
        path_to_list_file = source + library + postfix + ".json"

        list_file     = open (path_to_list_file, 'r')
        document_list = json.load (list_file)
        list_file.close ()

        for document in document_list:
            title       = document ["title"].lower ()
            evaluation  = float (document ["evaluation"])

            if 5 > evaluation > 0:
                if ("cloud" in title and "edge" in title) or ("continuum" in title) or ("osmotic" in title):
                    print (document ["title"] + ", " + str(evaluation))
