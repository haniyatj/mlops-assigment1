import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 3

def test_get_book(client):
    response = client.get('/books/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert response.json['title'] == '1984'
    assert response.json['author'] == 'George Orwell'

def test_get_nonexistent_book(client):
    response = client.get('/books/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Book not found'

def test_add_book(client):
    new_book = {"title": "Brave New World", "author": "Aldous Huxley"}
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    assert response.json['id'] == 4
    assert response.json['title'] == 'Brave New World'
    assert response.json['author'] == 'Aldous Huxley'

def test_add_book_invalid_input(client):
    invalid_book = {"title": "Missing Author"}
    response = client.post('/books', json=invalid_book)
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid input'

def test_update_book(client):
    updated_data = {"title": "1984 Updated", "author": "George Orwell Updated"}
    response = client.put('/books/1', json=updated_data)
    assert response.status_code == 200
    assert response.json['title'] == '1984 Updated'
    assert response.json['author'] == 'George Orwell Updated'

def test_update_nonexistent_book(client):
    updated_data = {"title": "Nonexistent Book", "author": "Unknown"}
    response = client.put('/books/999', json=updated_data)
    assert response.status_code == 404
    assert response.json['error'] == 'Book not found'

def test_delete_book(client):
    response = client.delete('/books/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Book deleted successfully'

def test_delete_nonexistent_book(client):
    response = client.delete('/books/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Book not found'

#New test cases for the search feature

def test_search_books_by_title(client):
    response = client.get('/books/search?title=1984')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert response.json[0]['title'] == '1984'

def test_search_books_by_author(client):
    response = client.get('/books/search?author=Harper Lee')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert response.json[0]['author'] == 'Harper Lee'

def test_search_books_no_match(client):
    response = client.get('/books/search?title=Unknown Book')
    assert response.status_code == 404
    assert response.json['message'] == 'No books found matching the criteria'

def test_search_books_partial_match(client):
    response = client.get('/books/search?title=Gatsby')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert 'gatsby' in response.json[0]['title'].lower()
