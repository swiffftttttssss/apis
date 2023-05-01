from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Book:
    def __init__(self, id, book_name, author, publisher):
        self.id = id
        self.book_name = book_name
        self.author = author
        self.publisher = publisher

    def to_dict(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher
        }


books = [
    Book(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Charles Scribner\'s Sons'),
    Book(2, 'To Kill a Mockingbird', 'Harper Lee', 'J. B. Lippincott & Co.'),
    Book(3, '1984', 'George Orwell', 'Secker & Warburg')
]


class BookResource(Resource):
    def get(self, book_id=None):
        if book_id:
            book = next((book for book in books if book.id == book_id), None)
            if book is None:
                return {'message': f'Book with id {book_id} not found'}, 404
            return book.to_dict(), 200
        else:
            return [book.to_dict() for book in books], 200

    def post(self):
        data = request.get_json()
        book_id = max([book.id for book in books]) + 1
        book = Book(book_id, data['book_name'], data['author'], data['publisher'])
        books.append(book)
        return book.to_dict(), 201

    def put(self, book_id):
        data = request.get_json()
        book = next((book for book in books if book.id == book_id), None)
        if book is None:
            return {'message': f'Book with id {book_id} not found'}, 404
        book.book_name = data['book_name']
        book.author = data['author']
        book.publisher = data['publisher']
        return book.to_dict(), 200

    def delete(self, book_id):
        global books
        books = [book for book in books if book.id != book_id]
        return '', 204


api.add_resource(BookResource, '/books', '/books/<int:book_id>')


if __name__ == '__main__':
    app.run(debug=True)