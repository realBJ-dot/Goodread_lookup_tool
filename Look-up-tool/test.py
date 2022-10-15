import unittest
import json
from book_scraping import find_book_info
from author_scraping import find_author_info
from database import insert_books, insert_authors

def is_correct_type(input, type):
    if isinstance(input, type):
        return True
    return False
##this is a sample test book url
book_url = "https://www.goodreads.com/book/show/9648068-the-first-days"
##this is a sample test author url
author_url = "https://www.goodreads.com/author/show/11783.Richard_Powers"

class TestScraping(unittest.TestCase):
    ##test if the output file is correctly converted to json file
    

    ##test if stuff in JSON is in correct format:string
    def test_json_file_string(self):
        with open("/Users/jinpeiyuan/Desktop/cs242Assignment2/fa21-cs242-assignment2/data.json") as f:
            data = json.loads(f.read()) 
            self.assertEqual(True, is_correct_type( data[0]['author name'], str))
    ##testif stuff in JSON is in correct format: int
    def test_json_file_int(self):
        with open("/Users/jinpeiyuan/Desktop/cs242Assignment2/fa21-cs242-assignment2/data.json") as f:
            data = json.loads(f.read()) 
            self.assertEqual(True, is_correct_type( data[0]['author id'], int))
    ##test the book scraper had scraped correct information
    def test_book_scraper(self):
        title, book_id, ISBN, author_url, author, rating, rating_count, review_count, image_url, similar_books = find_book_info(book_url)
        self.assertEqual("Rhiannon Frater", author)

    ##test books converting to JSON did not lose any parameters
    def test_convert_from_book(self):
        res = data_to_dic(book_url, False)
        self.assertEqual(10, len(res))

    ##test authors converting to JSON did not lose any parameters
    def test_convert_from_author(self):
        res = data_to_dic(author_url, True)
        self.assertEqual(9, len(res))

    ##test the author scraper had scraped correct information
    def test_author_scraper(self):
        author_name, author_url_, author_id, rating, rating_count, review_count, image_url, related_authors, author_books = find_author_info(author_url)
        self.assertEqual("Richard Powers", author_name)

    #test passing invalid url to find_author_info
    def test_invalid_url_author(self):
        res = find_author_info("http://abcdefghujkkjlfhsdvhsiuvhui")
        self.assertEqual("This is an invalid url!", res)

    ##test passing invalid url to find_book_info
    def test_invalid_url_author(self):
        res = find_book_info("fjewiofjeiofjoisndhchuiv")
        self.assertEqual("This is an invalid url!", res)
    
    #test invalid dict for book
    def test_invalid_dic_book(self):
        dic = {
            "1": "not right"
        }
        res = insert_books(dic)
        self.assertEqual("Please enter valid dic for books", res)
    #test invalid dict for author
    def test_invalid_dic_author(self):
        dic = {
            "2": "not right"
        }
        res = insert_authors(dic)
        self.assertEqual("Please enter valid dic for authors", res)


    

if __name__ == '__main__':
    unittest.main()


