from flask import Flask
from flask_cors import CORS

from routes.book_routes import book_bp
from routes.user_routes import user_bp
from routes.order_routes import order_bp

app = Flask(__name__)

# Enable CORS
CORS(app)

app.register_blueprint(book_bp)
app.register_blueprint(user_bp)
app.register_blueprint(order_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)