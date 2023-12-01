from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import socket

app = Flask(__name__)
uri = "mongodb+srv://ernesto202110469:QGBkL89AKUx1Oa62@cluster0.tftjf8o.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# use a database named "myDatabase"
db = client.myDatabase

# use a collection named "recipes"
my_collection = db["books"]

BOOK_DB = my_collection.books

@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to books app!"
    )


@app.route("/books")
def get_all_books():
    books = BOOK_DB.find()
    data = []
    for book in books:
        item = {
            "id": str(book["_id"]),
            "book": book["book"]
        }
        data.append(item)
    return jsonify(
        data=data
    )


@app.route("/book", methods=["POST"])
def create_book():
    data = request.get_json(force=True)
    BOOK_DB.insert_one({"book": data})
    return jsonify(
        message="book saved successfully!"
    )


@app.route("/book/<id>", methods=["PUT"])
def update_book(id):
    data = request.get_json(force=True)["book"]
    response = BOOK_DB.update_one({"_id": ObjectId(id)}, {"$set": {"book": data}})
    if response.matched_count:
        message = "Book updated successfully!"
    else:
        message = "No book found!"
    return jsonify(
        message=message
    )


@app.route("/book/<id>", methods=["DELETE"])
def delete_book(id):
    response = BOOK_DB.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Book deleted successfully!"
    else:
        message = "No book found!"
    return jsonify(
        message=message
    )


@app.route("/books/delete", methods=["POST"])
def delete_all_books():
    BOOK_DB.remove()
    return jsonify(
        message="All books deleted!"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)