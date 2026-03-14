from flask import Blueprint, request, jsonify
from database import db, cursor

order_bp = Blueprint("order", __name__)

# BUY BOOK
@order_bp.route("/buy_book", methods=["POST"])
def buy_book():

    data = request.json
    buyer_email = data["buyer_email"]
    book_id = data["book_id"]

    query = "INSERT INTO orders(buyer_email, book_id) VALUES(%s,%s)"
    cursor.execute(query, (buyer_email, book_id))
    db.commit()

    return jsonify({"message": "Book purchased successfully"})


# VIEW ORDERS
@order_bp.route("/orders", methods=["GET"])
def get_orders():

    query = """
    SELECT orders.id,
           orders.buyer_email,
           books.title,
           books.author,
           books.price,
           orders.order_date
    FROM orders
    JOIN books ON orders.book_id = books.id
    """

    cursor.execute(query)
    orders = cursor.fetchall()

    return jsonify(orders)