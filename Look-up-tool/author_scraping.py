import requests, bs4
import re
import time
##author url to start with


##value retrieved: author_name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books
def find_author_info(author_url):
    if "author" not in author_url:
        return "This is an invalid url!"
    author_URL = author_url
    res = requests.get(author_URL)
    if res == None:
        print("This is an invalid url!")
        return "This is an invalid url!"
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    ##author name
    author_name = None
    if check_validity(soup.find("span", itemprop="name")):
        author_name = soup.find("span", itemprop="name").get_text()

    #author id
    author_id = int(re.search(r'\d+', author_URL).group())

    author_rating = None
    ##author ratings
    if check_validity(soup.find("span", class_="average", itemprop="ratingValue")):
        author_rating = soup.find("span", class_="average", itemprop="ratingValue").get_text()
    


    rating_count = None
    ##overall rating count
    if check_validity(soup.find("span", class_="value-title", itemprop="ratingCount")):
        rating_count = soup.find("span", class_="value-title", itemprop="ratingCount")["title"]
    
    image_url = None
    ##image url get
    if check_validity(soup.find("img", alt=author_name, itemprop="image")):
        image_url = soup.find("img", alt=author_name, itemprop="image")["src"]
    


    ##find related authors
    urls = []
    related_authors_url = None
    
    related = list(soup.find("div", class_="hreview-aggregate", itemprop="aggregateRating").find_all("a"))[1]
    
    
    related_authors_url = "https://goodreads.com" + related["href"]
    redirected_related_authors = requests.get(related_authors_url)


    soup_redirected_related_authors = bs4.BeautifulSoup(redirected_related_authors.text, "html.parser")

    related_authors_list = soup_redirected_related_authors.find_all("a", itemprop="url")
    for i in related_authors_list:
        if "book" not in i["href"] and "list" not in i["href"]:
            urls.append(i["href"])
            


    ##redirected to more book page
    books_url = []
    if check_validity(soup.find_all("a", class_="actionLink", style="float: right")):
        more_book_url = None
        if len(soup.find_all("a", class_="actionLink", style="float: right")) >= 2:
            more_book_url = "https://www.goodreads.com" + soup.find_all("a", class_="actionLink", style="float: right")[1]["href"]
        if len(soup.find_all("a", class_="actionLink", style="float: right")) == 1:
            more_book_url = "https://www.goodreads.com" + soup.find_all("a", class_="actionLink", style="float: right")[0]["href"]
        redirected_more_book = None
        if more_book_url:
            redirected_more_book = requests.get(more_book_url)
        soup_redirected = bs4.BeautifulSoup(redirected_more_book.text, "html.parser")
        
        get_books_in_a_page(soup_redirected, books_url)
        while (soup_redirected.find("a", class_ = "next_page") != None):
            next = soup_redirected.find("a", class_ = "next_page")
            redirected_more_book = requests.get("https://goodreads.com" + next["href"])
            soup_redirected = bs4.BeautifulSoup(redirected_more_book.text, "html.parser")
            time.sleep(5)
            get_books_in_a_page(soup_redirected, books_url)

    review_count = None
    if check_validity(soup.find("span", class_="value-title", itemprop="reviewCount")):
        review_count = soup.find("span", class_="value-title", itemprop="reviewCount")["title"]
    return author_name, author_url, author_id, author_rating, rating_count, review_count, image_url, tuple(urls), tuple(books_url)


def get_books_in_a_page(soup_redirected, books_url):
    books_url_table = soup_redirected.find_all("a", {"class":"bookTitle", "itemprop":"url"})
    for url in books_url_table:
        books_url.append("https://goodreads.com" + url["href"])

def find_similar_authors(url):
    author_name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books = find_author_info(url)
    return list(related_authors)

def check_validity(stuff):
    if stuff != None:
        return True
    else:
        return False