from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
]


# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


# Route to get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404


# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    if not new_book or 'title' not in new_book or 'author' not in new_book:
        return jsonify({"error": "Invalid input"}), 400


    new_book['id'] = len(books) + 1
    books.append(new_book)
    return jsonify(new_book), 201


# Route to update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404


    updated_data = request.get_json()
    if not updated_data or not 'title' in updated_data or not 'author' in updated_data:
        return jsonify({"error": "Invalid input"}), 400


    book['title'] = updated_data['title']
    book['author'] = updated_data['author']


    return jsonify(book)


# Route to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404


    books = [book for book in books if book['id'] != book_id]
    return jsonify({"message": "Book deleted successfully"}), 200


# Route to search for books by title or author
@app.route('/books/search', methods=['GET'])
def search_books():
    title_query = request.args.get('title', '').lower()
    author_query = request.args.get('author', '').lower()

    filtered_books = [
        book for book in books
        if (title_query in book['title'].lower() if title_query else True) and
           (author_query in book['author'].lower() if author_query else True)
    ]


    if not filtered_books:
        return jsonify({"message": "No books found matching the criteria"}), 404


    return jsonify(filtered_books)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    