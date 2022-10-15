#from author_scraping import get_books_in_a_page
import requests, bs4
#from tkinter import *

##values retrieved: title, book_id, ISBN, author_url, author, rating, rating_count, review_count, image_url, similar_books
def find_book_info(book_url):
    if "book" not in book_url:
        return "This is an invalid url!"
    res = requests.get(book_url)
    if res == None:
        print("This is an invalid url!")
        return "This is an invalid url!"
    recipeSoup = bs4.BeautifulSoup(res.text, "html.parser")

    if check_validity(recipeSoup.find("span", itemprop="ratingValue")):
        rating = recipeSoup.find("span", itemprop="ratingValue").get_text()
    else:
        rating = None
    
    if check_validity(recipeSoup.find("meta", itemprop="ratingCount")):
        rating_count = recipeSoup.find("meta", itemprop="ratingCount")["content"]
    else: 
        rating_count = None

    if check_validity(recipeSoup.find("meta", itemprop="reviewCount")):
        review_count = recipeSoup.find("meta", itemprop="reviewCount")["content"]
    else:
        review_count = None

    if check_validity(recipeSoup.find("h1", id="bookTitle")):
        title = recipeSoup.find("h1", id="bookTitle").get_text()
    else:
        title = None
    if check_validity(recipeSoup.find("span", itemprop="name")):
        author_name = recipeSoup.find("span", itemprop="name").get_text()
    else:
        author_name = None
    if check_validity(recipeSoup.find("img", id="coverImage")):
        image_url = recipeSoup.find("img", id="coverImage")["src"]
    else:
        image_url = None
    if check_validity(recipeSoup.find("a", {"class": "authorName", "itemprop": "url"})):
        author_url = recipeSoup.find("a", {"class": "authorName", "itemprop": "url"})["href"]
    else:
        author_url = None

    book_data = recipeSoup.find("div", id="bookDataBox")
    isbn = ""
    if check_validity(book_data):
        clear_floats = book_data.find_all("div", class_ = "clearFloats")
        
        for one in clear_floats:
            if one.find("div", class_ = "infoBoxRowTitle").get_text() == "ISBN":
                isbn = one.find("div", class_ = "infoBoxRowItem").get_text().replace("\n", " ").replace(" ", "")
        
    urls = []
    if check_validity(recipeSoup.find("a", class_="actionLink right seeMoreLink")):
        similar_books_url = recipeSoup.find("a", class_="actionLink right seeMoreLink")["href"]
        new_res = requests.get(similar_books_url)
        another_soup = bs4.BeautifulSoup(new_res.text, "html.parser")

        
        if check_validity(another_soup.find_all("div", class_ = "listWithDividers")):
            similar_books_list = another_soup.find_all("div", class_ = "listWithDividers")
            for one_list in similar_books_list:
                some_url = one_list.find_all("a", itemprop = "url")
                for one_url in some_url:
                    if (one_url.find(("span"), itemprop = "name") != None):
                        urls.append("https://goodreads.com" + one_url["href"])
    book_id = get_id(book_url)

    return title, book_id, isbn, author_url, author_name, rating, rating_count, review_count, image_url, tuple(urls)

def get_id(url):
  everything_after_show = url.split("show/")[1]
  book_id = everything_after_show.split(".")[0]
  if (len(book_id) == len(everything_after_show)):
    book_id = everything_after_show.split("-")[0]
  return book_id


##this helper function returns a list of similar books related to the given url
def find_similar_book(url):
    title, book_id, ISBN, author_url, author, rating, rating_count, review_count, image_url, similar_books = find_book_info(url)
    return list(similar_books)

def check_validity(stuff):
    if stuff != None:
        return True
    else:
        return False


