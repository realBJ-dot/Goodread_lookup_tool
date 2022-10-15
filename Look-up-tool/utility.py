from database import connect
from bson.json_util import dumps
"""
this helper function takes the stuff that user want to find
"""
def get_book_info(key, content):
    if key == "title":
        content = content.replace("_", " ")
        content = "\n      " + content + "\n"
    if key == "book_id":
        key = "book id"
    dict = {key : content}
    client = connect()
    db = client['goodreads']
    collection = db['book']
    print(dict)
    what_found = collection.find(dict)
    Json = dumps(list(what_found), indent=2) 
    if len(Json) < 10:
        
        print("the val you entered doesn't exist in the database")
        return
    with open("get_book_info:.json", "w") as file:
        file.write(Json)
    client.close()
    return Json ##this return is for testing purpose
    

"""
same as above but getting the author info
"""
def get_author_info(key, content):
    if key == "author name":
        content = content.replace("_", " ", 1)
    dict = {key : content}
    client = connect()
    db = client['goodreads']
    collection = db['authors']
    what_found = collection.find(dict)
    
    Json = dumps(list(what_found), indent=2) 
    if len(Json) < 10:
        print("the val you entered doesn't exist in the database")
        return 
    with open("get_author_info:.json", "w") as file:
        file.write(Json)
    client.close()
    return Json ##for testing purpose only
    

    ##this is the helper function for command line with NOT, OR, AND
def get_with_constraint(key1, val1, key2, val2, operator, is_author):
    key1 = key1.replace("_", " ", 1) ##trim it as it appears in the database
    key2 = key2.replace("_", " ", 1) ##trim it as it appears in the database 
    if key1 == "author name":
        val1 = val1.replace("_", " ", 1)
    if key2 == "author name":
        val2 = val2.replace("_", " ", 1)
        
    dict1 = {key1 : val1}
    dict2 = {key2 : val2}
        
    client = connect()
    db = client['goodreads']
    collection = db['authors']
    if is_author == False:
        collection = db['book']
        if key1 == "title":
            val1 = val1.replace("_", " ")
            val1 = "\n      " + val1 + "\n"
            dict1 = {key1 : val1}
        if key2 == "title":
            val2 = val2.replace("_", " ")
            val2 = "\n      " + val2 + "\n"
            dict2 = {key2 : val2}
    what_found = None
    if operator == "OR":
        what_found = collection.find({"$or" : [dict1, dict2]})
    elif operator == "AND":
        what_found = collection.find({"$and" : [dict1, dict2]})
    elif operator == "NOT":
        what_found = collection.find({"$not" : [dict1, dict2]})
    if what_found == None:
        print("the val you entered doesn't exist in the database")
        return 
    Json = dumps(list(what_found), indent=2) 
    with open("with_operator_data.json", "w") as file:
        file.write(Json)
    client.close()
    return Json ##for testing purpose only
    

def parsing_to_output(attribute, val, is_author):
    if is_author:
        if check_if_valid_key(attribute, True):
            get_author_info(attribute, val)
        else:
            print("this is not a valid attribute to look up")
    else:
        if check_if_valid_key(attribute, False):
            get_book_info(attribute, val)
        else:
            print("this is not a valid attribute to look up")
    
##this helper function determins if this is a valid key
def check_if_valid_key(key, is_author):
    if is_author:
        if key == "author_name" or "author_url" or "author_id" or "rating" or "rating_count" or "review_count" or "image_url": 
            return True
    else:
        if key == "title" or "book_id" or "ISBN" or "author_url" or "author" or "rating" or "rating_count" or "review_count" or "image_url":    
            return True
    return False

        


def parsing_to_output_constraint(key1, val1,  key2, val2, operator, is_author):
    if is_author:
        if check_if_valid_key(key1, True) and check_if_valid_key(key2, True):  
            get_with_constraint(key1, val1, key2, val2, operator, True)
        else:
            print("this is not a valid key to look up")
    else:
        if check_if_valid_key(key1, False) and check_if_valid_key(key2, False):  
            get_with_constraint(key1, val1, key2, val2, operator, False)
        else:
            print("this is not a valid key to look up")

#print(get_author_constraint("rating", "4.01", "author id", 11783, "AND"))

##this helper function is to check if the id exist in either book or author collections
#on success, this function returns the json data of that id
def if_id_exist(client, id, is_author):
    if is_author:
        db = client['goodreads']
        collection = db['authors']
        what_found = collection.find({"author id" : {"$eq" : int(id)}})
        data = dumps(list(what_found), indent=2)
        if len(list(what_found)) > -1:
            return data
        else:
            return False
    else:
        db = client['goodreads']
        collection = db['book']
        what_found = collection.find({"book id" : {"$eq" : str(id)}})
        data = dumps(list(what_found), indent=2)
        if len(list(what_found)) > -1:
            return data
        else:
            return False
#print(if_id_exist(connect(), 11783, True))

##this function returns true if successfully delete that book/author from db, false otherwise
def handle_delete_flag(author_or_book, key, val):
    client = connect()
    db = client['goodreads']
    if author_or_book == "book:":
        collection = db['book']
        if check_if_valid_key(key, False) == False:
            return False
        data = if_id_exist(client, val, False) ##only delete by id
        if data != False:
            key = key.replace("_", " ")
            dict = {key : val}
            
            collection.delete_one(dict)
            return True
    elif author_or_book == "authors:":
        collection = db['authors']
        if check_if_valid_key(key, True) == False:
            return False
        data = if_id_exist(client, val, True) ##only delete by id
        if data != False:
            key = key.replace("_", " ")
            dict = {key : val}
            collection.delete_one(dict)
            return True
    

