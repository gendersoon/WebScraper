import unittest
from Menu import Main


class Testscraper(unittest.TestCase):

    def setUp(self):
       self.m = Main

     
    def test_scraper(self):
        self.assertIsNone(self.m.main(self,"https://stackoverflow.com/questions/16840409/how-to-list-containers-in-docker"))


    
    def test_attr_error(self):
        with self.assertRaises(AttributeError):
            self.m.main(self, "https://docs.python.org/3/library/unittest.html")

if __name__ == '__main__':
    unittest.main()
