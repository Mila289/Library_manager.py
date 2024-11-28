import json
import os
from random import choice


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
        def display_book(self):
            for book in self.books:
                print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")
        def change_status(self, book_id: int, status: str):
            for book in self.books:
                if book.id==book_id:
                    if status in ("в наличии", "выдана"):
                        book.status=status
                        self.save_books()
                    else:
                        print("Недопустимый статус. Статус может быть 'в наличии' или 'выдана'.")
                    return
                print(f"Книга с ID {book_id} не найдена.")
    def main():
        library=Library()
        while True:
            print("\nВведите номер необходимого действия:")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Найти книгу")
            print("4. Отобразить все книги")
            print("5. Изменить статус книги")
            print("0. Выйти")
            choice=input("Ваш выбор:")
            if choice=='1':
                title=input("Введите название книги:")
                author=input("Введите автора книги:")
                year=int(input("Введите год издания:"))
                library.add_book(title, author, year)


