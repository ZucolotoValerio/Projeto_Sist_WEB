from flask import Flask, request, redirect, render_template
import json
import os
import time

app = Flask(__name__)


@app.route("/home")
def home():
    with open(os.path.join('./json_data', 'books_science.json'), 'r') as json_books:
        body_books = json.loads(json_books.read())

        print(body_books)

    return render_template("home.html", body_books=body_books)


@app.route("/register_book", methods=["GET", "POST"])
def registerBook():

    if request.method == "GET":
        return render_template("register_book.html", message={})

    # EXEMPLO DE OBJETO PARA ENVIAR {"id_book": 5, "name_book": "Leonardo Da Vinci", "author": "O mestre dos livros", "date_release": "01/10/1998", "description": "balblabla livro bom", "category": "history", "rates": []} 
    book_object = request.form

    with open(os.path.join('./json_data', 'books_'+book_object["category"]+'.json'), 'r') as json_books:
        body_books = json.loads(json_books.read())

    id_book = len(body_books[book_object["category"]])+1
    
    book_object_json = {"id_book": id_book, "name_book": book_object["name_book"], "author": book_object["author"], "date_release": book_object["date_release"], "description": book_object["description"], "category": book_object["category"], "rates": []}

    with open(os.path.join('./json_data', 'books_'+book_object["category"]+'.json'), 'w') as json_books:
        body_books[book_object["category"]].append(book_object_json)
        json_books.write(json.dumps(body_books, sort_keys=True, indent=4))

    with open(os.path.join('./json_data', 'category.json'), 'r') as json_categories:
        body_categories = json.loads(json_categories.read())
        for category in body_categories["data"]:
            if category["name_category"] == book_object["category"]:
                category["number_books"] = len(body_books[book_object["category"]])

    with open(os.path.join('./json_data', 'category.json'), 'w') as json_categories:
        json_categories.write(json.dumps(body_categories, sort_keys=True, indent=4))
    
    return render_template("register_book.html", message={"message": "Livro adicionado!"})



@app.route("/get_book", methods=["GET", "POST"])
def getBook():

    book_search = request.form
    print(book_search)
    return book_search
    # book_obj = None
        
    # with open(os.path.join('./json_data', 'books_'+book_search["category"]+'.json'), 'r') as json_books:
    #     body_books = json.loads(json_books.read())

    #     for book in body_books["data"]:
    #         if book["name_book"] == book_search["name_book"]:
    #             book_obj = book

    # return render_template("book.html", book=book_obj)
                

@app.route("/rate_book", methods=["POST"])
def rateBook():
    # EXEMPLO DE OBJETO PARA ENVIAR {"id_book": 5, "category": "science", "rate": {"author_rate": "Juliano do Morro", "comment": "Livro muito loko meu", "stars": 4}}
    rate_object = request.form

    with open(os.path.join('./json_data', 'books_'+rate_object["category"]+'.json'), 'r') as json_books:
        body_books = json.loads(json_books.read())

    with open(os.path.join('./json_data', 'books_'+rate_object["category"]+'.json'), 'w') as json_books:

        for book in body_books[rate_object["category"]]:
            
            if book["id_book"] == rate_object["id_book"]:
                book["rates"].append(rate_object["rate"])       
                print(book["rates"])
        json_books.write(json.dumps(body_books, sort_keys=True, indent=4))
    
    return {"message": "Avaliação criada com sucesso!"}


@app.route("/create_account", methods=["GET", "POST"])
def createAccount():
    # EXEMPLO DE OBJETO PARA ENVIAR {"name": "el usuario", "email": "fulano2@email.com", "password": "ahahahaha"}

    if request.method == "GET":
        return render_template("register_account.html", message={})

    account_object = request.form
    print(account_object)
    with open(os.path.join('./json_data', 'accounts.json'), 'r') as json_accounts:
        body_accounts = json.loads(json_accounts.read())

    for account in body_accounts["data"]:
        if account_object["email"] == account["email"]:
            # print("caiu no if")
            return render_template("register_account.html", message={"message": "Uma conta já usa este email"})

    with open(os.path.join('./json_data', 'accounts.json'), 'w') as json_accounts:

        body_accounts["data"].append(account_object)      

        json_accounts.write(json.dumps(body_accounts, sort_keys=True, indent=4))
    
    return render_template("auth.html", message={"message": "Conta criada com sucesso!"})


@app.route("/get_category", methods=["GET", "POST"])
def getCategory():
    # EXEMPLO DE OBJETO PARA ENVIAR {"category": "history"}
    search_body = request.form

    with open(os.path.join('./json_data', 'books_'+search_body["category"]+'.json'), 'r') as json_category:
        body_books = json_category.read()

    return render_template("category_list.html", category=search_body["category"], list_category=json.loads(body_books))


@app.route("/auth", methods=["GET", "POST"])
def authentication():

    if request.method == "GET":
        return render_template("auth.html", message={})

    credentials_body = request.form
    print(credentials_body)
    with open(os.path.join('./json_data', 'accounts.json'), 'r') as json_account:
        accounts = json.loads(json_account.read())

    verifier = False

    for account in accounts["data"]:
        if account["email"] == credentials_body["email"] and account["password"] == credentials_body["password"]:
            verifier = True

    if verifier == False:
        return render_template("auth.html", message={"message": "Senha Incorreta"})
    
    return redirect("/home")


@app.route("/all_category")
def allCategory():

    with open(os.path.join('./json_data', 'category.json'), 'r') as books_history:
        categories_json = json.loads(books_history.read())

    print(categories_json)
    return render_template("categories.html", categories_json=categories_json)

if __name__ == "__main__":
    app.run()