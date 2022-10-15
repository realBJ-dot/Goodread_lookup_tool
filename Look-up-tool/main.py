import argparse
from book_scraping import find_similar_book
from author_scraping import find_similar_authors
from database import insert_authors, insert_books, data_to_dic
import random
from utility import handle_delete_flag, parsing_to_output, parsing_to_output_constraint

if __name__ == "__main__":
    ##this print usage for scraping
    def print_usage_scrap():
        print("python3 main.py -scrap [url to scrap] [num authors] [num books]")
    ##this print usage for reading from database
    def print_usage_r():
        print("python3 main.py -r [author/book].[key]:[val]")
    ##print usage for compare with operators
    def print_usage_c():
        print("python3 main.py -c [author/book]: [key1] [val1] [NOT/AND/OR] [key2] [val2]")
    def print_usage_delete():
        print("python3 main.py -delete [author/book]: [key] [val]")

    ##user input command line should be like: python3 main.py -scrap [url to scrap] [num authors] [num books]
    psr = argparse.ArgumentParser()
    psr.add_argument("-scrap", nargs=3)
    psr.add_argument("-r", nargs=1) ##requesting book info or author info
    psr.add_argument("-c", nargs=6) ##providing info with constraint (and, or, not)
    psr.add_argument("-delete", nargs=3) ##handling the delete case

    
    args = vars(psr.parse_args())

    """
    This is for user to input url to scrap information from the web
    """
    if args["scrap"] != None:
        stuff_scraping = args["scrap"]
        print(stuff_scraping)
        url = stuff_scraping[0]
        num_authors = int(stuff_scraping[1])
        num_books = int(stuff_scraping[2])

        if "goodreads" in url:
            print("this is a valid url")
            
        else:
            print("this is not a valid url")
            print_usage_scrap()

        if num_authors > 50 and num_books > 200:
            print("WARNING: TOO MANY AUTHORS AND BOOKS!")
        else:
            print("Number of authors: " + str(num_authors))
            print("Number of books: " + str(num_books))
            print("You are good to go!")
        
        if "book" in url:
            print("Yea, this is a url pointing to a book!")
            while num_books != 0:
                related_book_list = find_similar_book(url)
                rand_num = random.randint(1, len(related_book_list) - 1)
                get_rand_url = related_book_list[rand_num]
                url = get_rand_url
                print(url)
                insert_books(data_to_dic(get_rand_url, False))   
                num_books -= 1
        if "author" in url:
            print("This is a url pointing to authors!")
            while num_authors != 0:
                related_authors_list = find_similar_authors(url)
                if len(related_authors_list) == 0:
                    break
                ##to ensure not to rand to itself, it starts from 1
                rand_num = random.randint(1, len(related_authors_list) - 1)           
                
                get_rand_url = related_authors_list[rand_num]           
                
                url = get_rand_url
                print(url)
                insert_authors(data_to_dic(url, True)) 
                num_authors -= 1 
    
    """
    This is for parsing user input for requesting information in the database
    """
    ##
    if args["r"] != None:
        to_request = args["r"]  ##i.e. to_request = book.book_id:xxxxx
        to_request = to_request[0]
        if "." in to_request:
            splitted_list = to_request.split(".", 1) ##it should be something like: book.rating_count:xxxx
            info = splitted_list[1] ##rating_count:xxxx
            attribute_and_val = info.split(':')## rating_count, xxxx
            
            attribute, val = attribute_and_val
            book_or_author = splitted_list[0] 
            if book_or_author == "book":
                parsing_to_output(attribute, val, False)
            elif book_or_author == "author":
                parsing_to_output(attribute, val, True)
            else:
                print("What you are requesting is not in database!")
        else:
            print("Incorrect use of this function!")


    
    ##This is to provide information according to the given constraint
    ## command line: python3 main.py -c [author/book]: [key1] [val1] [NOT/AND/OR] [key2] [val2]
    
    if args["c"] != None:
        all_info = args["c"]
        author_or_book = all_info[0]
        key1 = all_info[1]
        val1 = all_info[2]
        operator = all_info[3]
        key2 = all_info[4]
        val2 = all_info[5]
        if author_or_book == "book:":
            parsing_to_output_constraint(key1, val1,  key2, val2, operator, False)
        elif author_or_book == "author:":
            parsing_to_output_constraint(key1, val1,  key2, val2, operator, True)
        else:
            print_usage_c()


    ##This is to provide info given user cmd like </>
    ## cmd line: python3 main.py -b [author/book] [key] [>/<] [val]
    """
    if args["b"] != None:
        all = args["b"]
        author_or_book = all[0]
        key = all[1]
        compare = all[2]
        val = all[3]
    """

    ##if a user wanna delete an element from db, (only by id)
    #usage: python3 main.py -delete [author/book]: [key] [val]

    if args["delete"] != None:
        author_or_book, key, val  = args["delete"]
        if handle_delete_flag(author_or_book, key, val) == True:
            print("you have successfully deleted this element by id!")
        else:
            print_usage_delete()



        






        
        
            
        
        
        


