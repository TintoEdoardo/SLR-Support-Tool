import unittest
import digital_libraries.ieee_digital_library


class MyTestCase (unittest.TestCase):

    def test_Acquire_Month (self):
        date  = "10-16 July 2022"
        month = digital_libraries.ieee_digital_library.Acquire_Month (date)
        self.assertEqual (month, "July")


if __name__ == '__main__':
    unittest.main()
