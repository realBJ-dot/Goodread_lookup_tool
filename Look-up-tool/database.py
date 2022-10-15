import pymongo
from author_scraping import find_author_info
from book_scraping import find_book_info
from bson.json_util import dumps


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
def connect():
    client = pymongo.MongoClient("mongodb+srv://BarneyJin:Jinpy20010817@goodreads.xlnx6.mongodb.net/")
    try:
        client.admin.command('ismaster')
        return client
    except pymongo.errors.ConnectionFailure:
        print("Could not connect to server")

def output_to_json(if_author): ##input a bool of whether is author or not
    client = connect()
    db = client['goodreads']
    collection = None
    if if_author:
        collection = db["authors"]
    else:
        collection = db['book']
    cursor = collection.find()
    Json = dumps(list(cursor), indent=2) 
    with open("data.json", "w") as file:
        file.write(Json)
    client.close()
    return file

def insert_books(to_insert):
    client = connect()
    if len(to_insert) != 10:
        return "Please enter valid dic for books"
    client.admin.command('ismaster')
    db = client['goodreads']
    collection = db['book']
    collection.insert_one(to_insert)
    client.close()
    

def insert_authors(to_insert):
    client = connect()
    if len(to_insert) != 9:
        return "Please enter valid dic for authors"
    client.admin.command('ismaster')
    db = client['goodreads']
    collection = db['authors']
    collection.insert_one(to_insert)
    client.close()
    


##this function converts the data scraped from url into dictionary
def data_to_dic(url, if_author):
    if if_author:
        author_name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books = find_author_info(url)
        dict = {
            "author name": author_name,
            "author url": author_url,
            "author id": author_id,
            "rating": rating,
            "rating count": rating_count,
            "review count": review_count,
            "image url": image_url,
            "related authors": related_authors,
            "author_books": author_books
        }
        return dict
    else: #if the user entered book url
        title, book_id, isbn, author_url, author, rating, rating_count, review_count, image_url, similar_books = find_book_info(url)
        dict = {
            "title": title,
            "book id": book_id,
            "ISBN": isbn,
            "author url": author_url,
            "author": author,
            "rating": rating,
            "rating count": rating_count,
            "review count": review_count,
            "image url": image_url,
            "similar books": similar_books
        }
        return dict





