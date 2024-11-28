import json
import os
class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str="в наличии"):
        self.id=id
        self.title=title
        self.author=author
        self.year=year
        self.status=status
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'author': self.author, 'year': self.year, 'status': self.status}
    class Library:
        def __init__(self, filename: str="library.json"):
            self.books = []
            self.filename = filename
            self.load_books()
        def load_books(self):
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.books=[Book(**data) for data in json.load(f)]
        def save_books(self):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([book.to_dict() for book in self.books], f)
        def add_book(self, title: str, author: str, year: int):
            book_id=len(self.books)+1
            new_book=Book(book_id, title, author, year)
            self.books.append(new_book)
            self.save_books()
        def remove_book(self, book_id: int):
            for book in self.books:
                if book.id==book_id:
                    self.books.remove(book)
                    self.save_books()
                    return
                print(f"Книга с ID {book_id} не найдена.")
        def find_books(self, title=None, author=None, year=None):
            result=self.books
            if title:
                result=[book for book in result if title.lower() in book.title.lower()]
            if author:
                result=[book for  book in result if author.lower() in book.author.lower()]
            if year:
                result=[book for book in result if book.year==year]
            return result
