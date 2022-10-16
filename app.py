from flask import Flask, request
import json
import os
import time

app = Flask(__name__)


@app.route("/")
def teste():
    with open(os.path.join('./json_data', 'books_science.json'), 'r') as json_account:
        body_books = json_account.read()
        print(body_books)
    return json.loads(body_books)


@app.route("/register_book", methods=["POST"])
def registerBook():
    # EXEMPLO DE OBJETO PARA ENVIAR {"id_book": 5, "name_book": "Leonardo Da Vinci", "author": "O mestre dos livros", "date_release": "01/10/1998", "description": "balblabla livro bom", "category": "history", "rates": []} 
    book_object = request.json

    with open(os.path.join('./json_data', 'books_'+book_object["category"]+'.json'), 'r') as json_books:
        body_books = json.loads(json_books.read())

    with open(os.path.join('./json_data', 'books_'+book_object["category"]+'.json'), 'w') as json_books:
        body_books[book_object["category"]].append(book_object)
        json_books.write(json.dumps(body_books, sort_keys=True, indent=4))
    
    return {"message": "Book added sucessfully!", "book": book_object}



@app.route("/rate_book", methods=["POST"])
def rateBook():
    rate_object = request.json
    # EXEMPLO DE OBJETO PARA ENVIAR {"id_book": 5, "category": "science", "rate": {"author_rate": "Juliano do Morro", "comment": "Livro muito loko meu", "stars": 4}}

    with open(os.path.join('./json_data', 'books_'+rate_object["category"]+'.json'), 'r') as json_books:
        body_books = json.loads(json_books.read())

    with open(os.path.join('./json_data', 'books_'+rate_object["category"]+'.json'), 'w') as json_books:

        for book in body_books[rate_object["category"]]:
            
            if book["id_book"] == rate_object["id_book"]:
                book["rates"].append(rate_object["rate"])       
                print(book["rates"])
        json_books.write(json.dumps(body_books, sort_keys=True, indent=4))
    
    return {"message": "Avaliação criada com sucesso!"}


@app.route("/create_account", methods=["POST"])
def createAccount():
    account_object = request.json
    # EXEMPLO DE OBJETO PARA ENVIAR {"name": "el usuario", "email": "fulano2@email.com", "password": "ahahahaha"}

    with open(os.path.join('./json_data', 'accounts.json'), 'r') as json_accounts:
        body_accounts = json.loads(json_accounts.read())

    with open(os.path.join('./json_data', 'accounts.json'), 'w') as json_accounts:

        body_accounts["data"].append(account_object)      

        json_accounts.write(json.dumps(body_accounts, sort_keys=True, indent=4))
    
    return {"message": "Conta criada com sucesso!"}


@app.route("/get_category")
def getCategory():

    # EXEMPLO DE OBJETO PARA ENVIAR {"category": "history"}
    search_body = request.json

    with open(os.path.join('./json_data', 'books_'+search_body["category"]+'.json'), 'r') as json_account:
        body_books = json_account.read()

    return json.loads(body_books)