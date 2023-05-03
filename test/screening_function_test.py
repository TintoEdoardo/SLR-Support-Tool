import json
import unittest
import analysis.screening_functions


class MyTestCase (unittest.TestCase):

    path_to_bibliography = "test_file/bibliography.json"
    path_to_pdfs         = "test_file/PDFs"
    relevance_keys       = [
        {'key'    : 'continuum',
         'weight' : '100',
         'loc'    : 'full_body'},
        {'key'    : 'cloud',
         'weight' : '10',
         'loc'    : 'full_body'},
        {'key'    : 'survey',
         'weight' : '-1000',
         'loc'    : 'title'}
    ]

    def test_read_article_from_bibliography (self):
        Screener = analysis.screening_functions.Content_Screener (self.path_to_pdfs, self.path_to_bibliography)

        Screener.read_article_from_bibliography ()

        self.assertEqual (len (Screener.article_list), 12)


    def test_assign_relevance (self):
        Screener = analysis.screening_functions.Content_Screener(self.path_to_pdfs, self.path_to_bibliography)
        Screener.read_article_from_bibliography ()

        Screener.assign_relevance (self.relevance_keys)

        for article in Screener.article_list:
            self.assertIsInstance (article ["note"], float)


if __name__ == '__main__':
    unittest.main()
