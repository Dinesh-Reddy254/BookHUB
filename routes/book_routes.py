from flask import Blueprint, request, jsonify
from database import db, cursor

book_bp = Blueprint("book", __name__)


# ADD BOOK
@book_bp.route("/add_book", methods=["POST"])
def add_book():

    data = request.json

    title = data["title"]
    author = data["author"]
    price = data["price"]
    seller_email = data["seller_email"]
    seller_phone = data["seller_phone"]

    query = """
    INSERT INTO books(title,author,price,seller_email,seller_phone)
    VALUES(%s,%s,%s,%s,%s)
    """

    cursor.execute(query,(title,author,price,seller_email,seller_phone))
    db.commit()

    return jsonify({"message":"Book added successfully"})


# GET BOOKS WITH PAGINATION
@book_bp.route("/books", methods=["GET"])
def get_books():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    offset = (page - 1) * limit

    query = "SELECT * FROM books LIMIT %s OFFSET %s"
    cursor.execute(query,(limit,offset))

    books = cursor.fetchall()

    return jsonify(books)


# SEARCH BOOKS
@book_bp.route("/search_books", methods=["GET"])
def search_books():

    title = request.args.get("title")
    author = request.args.get("author")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE %s"
        params.append(f"%{title}%")

    if author:
        query += " AND author LIKE %s"
        params.append(f"%{author}%")

    if min_price:
        query += " AND price >= %s"
        params.append(min_price)

    if max_price:
        query += " AND price <= %s"
        params.append(max_price)

    cursor.execute(query, params)
    books = cursor.fetchall()

    return jsonify(books)


# GET SINGLE BOOK (FOR BOOK DETAILS PAGE)
@book_bp.route("/book/<int:id>", methods=["GET"])
def get_book(id):

    query = "SELECT * FROM books WHERE id=%s"
    cursor.execute(query,(id,))
    book = cursor.fetchone()

    return jsonify(book)


# DELETE BOOK
@book_bp.route("/book/<int:id>", methods=["DELETE"])
def delete_book(id):

    query = "DELETE FROM books WHERE id=%s"
    cursor.execute(query,(id,))
    db.commit()

    return jsonify({"message":"Book deleted successfully"})


# UPDATE BOOK PRICE
@book_bp.route("/book/<int:id>", methods=["PUT"])
def update_book(id):

    data = request.json
    price = data["price"]

    query = "UPDATE books SET price=%s WHERE id=%s"
    cursor.execute(query,(price,id))
    db.commit()

    return jsonify({"message":"Book updated successfully"})


# GET BOOKS OF A PARTICULAR SELLER
@book_bp.route("/seller/books/<email>", methods=["GET"])
def get_seller_books(email):

    query = "SELECT * FROM books WHERE seller_email=%s"
    cursor.execute(query,(email,))
    books = cursor.fetchall()

    return jsonify(books)