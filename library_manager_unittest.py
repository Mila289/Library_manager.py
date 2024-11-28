import json
import os
import unittest

class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'author': self.author, 'year': self.year, 'status': self.status}


class Library:
    def __init__(self, filename: str = "library.json"):
        self.books = []
        self.filename = filename
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.books = [Book(**data) for data in json.load(f)]

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f)

    def add_book(self, title: str, author: str, year: int):
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: int):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return
        print(f"Книга с ID {book_id} не найдена.")

    def find_books(self, title=None, author=None, year=None):
        result = self.books
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        if author:
            result = [book for book in result if author.lower() in book.author.lower()]
        if year:
            result = [book for book in result if book.year == year]
        return result

    def display_books(self):
        for book in self.books:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

    def change_status(self, book_id: int, status: str):
        for book in self.books:
            if book.id == book_id:
                if status in ("в наличии", "выдана"):
                    book.status = status
                    self.save_books()
                else:
                    print("Недопустимый статус. Статус может быть 'в наличии' или 'выдана'.")
                return
        print(f"Книга с ID {book_id} не найдена.")


class TestLibrary(unittest.TestCase):
    def setUp(self):
        #Создаем временный файл и объект библиотеки.
        self.library = Library("test_library.json")
        self.library.books = []  # Очистим книги для тестов

    def tearDown(self):
        #Удаляем временный файл после тестов.
        if os.path.exists("test_library.json"):
            os.remove("test_library.json")

    def test_add_book(self):
        #Тестирование добавления книги.
        self.library.add_book("Test Book", "Test Author", 2021)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")

    def test_remove_book(self):
        #Тестирование удаления книги.
        self.library.add_book("Test Book", "Test Author", 2021)
        self.library.remove_book(1)  # Удаляем книгу с ID 1
        self.assertEqual(len(self.library.books), 0)

    def test_find_books_by_title(self):
        #Тестирование поиска книг по названию.
        self.library.add_book("Test Book", "Test Author", 2021)
        results = self.library.find_books(title="Test Book")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Book")

    def test_find_books_by_author(self):
        #Тестирование поиска книг по автору.
        self.library.add_book("Test Book", "Test Author", 2021)
        results = self.library.find_books(author="Test Author")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Test Author")

    def test_find_books_by_year(self):
        #Тестирование поиска книг по году.
        self.library.add_book("Test Book", "Test Author", 2021)
        results = self.library.find_books(year=2021)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2021)

    def test_change_status(self):
        #Тестирование изменения статуса книги.
        self.library.add_book("Test Book", "Test Author", 2021)
        self.library.change_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_invalid_status(self):
        #Тестирование недопустимого статуса.
        self.library.add_book("Test Book", "Test Author", 2021)
        self.library.change_status(1, "недопустимый статус")
        self.assertEqual(self.library.books[0].status, "в наличии")  # Статус не должен измениться


if __name__ == "__main__":
    unittest.main()

