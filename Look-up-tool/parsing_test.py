import unittest
from utility import get_book_info, get_author_info, check_if_valid_key
import json

class TestParsing(unittest.TestCase):
    ##test for getting correct book info
    def test_get_book_info(self):
        key = "title"
        content = "Bloody_Sunset"
        what_found = get_book_info(key, content)  ##what found is a json
        ##test if get the correct item
        data = json.loads(what_found)
        self.assertEqual("51285942", data[0]["book id"])

    def test_empty_book(self):
        key = "title"
        content = "i am sure it is not in the databse"
        what_found = get_book_info(key, content)
        ##test if it returns none when given a non-existant info
        self.assertEqual(None, what_found)
    
    ##same as above but with a non existant key
    def test_empty_book_output(self):
        key = "title_super_plus"
        content = "Instauration"
        what_found = get_book_info(key, content)
        self.assertEqual(None, what_found)
    
    ##test that if getting the correct info by entering this attribute
    def test_get_author_info(self):
        key = "author name"
        content = "Richard_Powers"
        what_found = get_author_info(key, content)
        data = json.loads(what_found)
        
        self.assertEqual(11783, data[0]["author id"])

    ##test if it returns none when given a non-existant info
    def test_empty_author(self):
        key = "author name"
        content = "hahaha there cant be me in database"
        what_found = get_author_info(key, content)
        self.assertEqual(None, what_found)

    ##same as above but with a non existant key
    def test_empty_author_output(self):
        key = "author's cat's name"
        content = "meow"
        what_found = get_author_info(key, content)
        self.assertEqual(None, what_found)

    ##check if this key is valid
    def check_check_if_valid_key_valid(self):
        key = "author_name"
        self.assertTrue(check_if_valid_key(key, True))
    #same as above but with a invalid key
    def check_check_if_valid_key_invalid(self):
        key = "author_namePlus"
        self.assertFalse(check_if_valid_key(key, True))

        




if __name__ == '__main__':
    unittest.main()