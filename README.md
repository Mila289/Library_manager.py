# Library_manager.py
Описание функциональности приложения
Это приложение реализует систему управления библиотекой, позволяя пользователю выполнять следующие действия:

Добавление книги: Пользователь может вводить название, автора и год издания книги, которая будет добавлена в библиотеку.
Удаление книги: Позволяет удалять книгу из библиотеки по ее уникальному идентификатору (ID).
Поиск книг: Пользователь может найти книги по названию, автору или году издания.
Отображение всех книг: Приложение может вывести список всех книг в библиотеке с их основными атрибутами.
Изменение статуса книги: Позволяет изменять статус книги (например, "в наличии" или "выдана").
Хранение данных: Все данные о книгах сохраняются в формате JSON в файле, что позволяет сохранять информацию между запусками программы.
Комментарии и аннотации в коде
import json
import os


class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        
        Конструктор класса Book.

        :param id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги, по умолчанию "в наличии".
        
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        
        Преобразует объект Book в словарь для сериализации.

        :return: Словарь с данными книги.
        
        return {'id': self.id, 'title': self.title, 'author': self.author, 'year': self.year, 'status': self.status}


class Library:
    def __init__(self, filename: str = "library.json"):
        
        Конструктор класса Library.

        :param filename: Имя файла для сохранения и загрузки данных о книгах.
        
        self.books = []
        self.filename = filename
        self.load_books()  # Загрузка книг из файла при инициализации библиотеки

    def load_books(self):
        
        Загружает книги из JSON-файла, если файл существует.
        
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                # Создание объектов Book из загруженных данных
                self.books = [Book(**data) for data in json.load(f)]

    def save_books(self):
        
        Сохраняет текущий список книг в JSON-файл.
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            # Использует метод to_dict для сохранения данных
            json.dump([book.to_dict() for book in self.books], f)

    def add_book(self, title: str, author: str, year: int):
        
        Добавляет новую книгу в библиотеку.

        :param title: Название добавляемой книги.
        :param author: Автор добавляемой книги.
        :param year: Год издания добавляемой книги.
        
        book_id = len(self.books) + 1  # Уникальный ID для книги
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)  # Добавление книги в список
        self.save_books()  # Сохранение изменений в файл

    def remove_book(self, book_id: int):
        
        Удаляет книгу по её ID.

        :param book_id: Уникальный идентификатор книги для удаления.
        
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)  # Удаление книги из списка
                self.save_books()  # Сохранение изменений в файл
                return
        print(f"Книга с ID {book_id} не найдена.")  # Сообщение, если книга не найдена

    def find_books(self, title=None, author=None, year=None):
        
        Находит книги по указанным критериям.

        :param title: Название книги для поиска.
        :param author: Автор книги для поиска.
        :param year: Год издания книги для поиска.
        :return: Список найденных книг.
        
        result = self.books
        if title:
            result = [book for book in result if title.lower() in book.title.lower()]
        if author:
            result = [book for book in result if author.lower() in book.author.lower()]
        if year:
            result = [book for book in result if book.year == year]
        return result  # Возврат списка найденных книг

    def display_books(self):
        
        Отображает все книги в библиотеке с их атрибутами.
        
        for book in self.books:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

    def change_status(self, book_id: int, status: str):
        
        Изменяет статус книги по её ID.

        :param book_id: Уникальный идентификатор книги.
        :param status: Новый статус книги (в наличии / выдана).
        
        for book in self.books:
            if book.id == book_id:
                if status in ("в наличии", "выдана"):
                    book.status = status  # Изменение статуса
                    self.save_books()  # Сохранение изменений в файл
                else:
                    print("Недопустимый статус. Статус может быть 'в наличии' или 'выдана'.")
                return
        print(f"Книга с ID {book_id} не найдена.")  # Сообщение, если книга не найдена


def main():
    
    Главная функция, которая предоставляет интерфейс для пользователя.
    
    library = Library()  # Создание экземпляра библиотеки
    while True:
        print("\nВведите номер необходимого действия:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("0. Выйти")
        choice = input("Ваш выбор:")

        if choice == '1':
            title = input("Введите название книги:")
            author = input("Введите автора книги:")
            year = int(input("Введите год издания:"))
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления:"))
            library.remove_book(book_id)

        elif choice == '3':
            search_type = input("Введите, по какому параметру искать (title, author, year):")
            if search_type == 'title':
                title = input("Введите название книги:")
                results = library.find_books(title=title)
            elif search_type == 'author':
                author = input("Введите автора:")
                results = library.find_books(author=author)
            elif search_type == 'year':
                year = int(input("Введите год:"))
                results = library.find_books(year=year)
            else:
                print("Неверный параметр.")
                continue

            for book in results:
                print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса:"))
            new_status = input("Введите новый статус (в наличии / выдана):")
            library.change_status(book_id, new_status)

        elif choice == '0':
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
Общие замечания
Комментарии добавлены к каждой функции и методу, чтобы объяснить их назначение и параметры.
Использованы аннотации типов для указания типов параметров и возвращаемых значений, что делает код более понятным и удобным для сопровождения.
Добавлены детали по каждому действию в документации классов и методов, чтобы было легче ориентироваться в коде и понимать его логику.
Теперь код содержит подробные комментарии и аннотации, что делает его более читабельным и удобным для понимания.

# Добавление тестирования в использованием модуля "unittest".
Для добавления тестирования с использованием модуля `unittest`, мы создадим тестовый класс, который будет проверять каждую из функций в классе `Library`. Мы будем тестировать такие функции, как добавление книги, удаление книги, поиск книг, отображение книг и изменение статуса книги.

Вот как это может выглядеть:

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


# Объяснение тестов

1. "setUp и tearDown":
   - `setUp`: Этот метод вызывается перед каждым тестом. Он создаёт новую библиотеку и очищает список книг, чтобы каждый тест запускался в чистой среде.
   - `tearDown`: Этот метод вызывается после каждого теста. Он удаляет временные файлы, созданные во время тестирования.

2. "Тестирование функций":
   - `test_add_book`: Проверяет, что книга добавляется в библиотеку и что ее атрибуты соответствуют ожидаемым значениям.
   - `test_remove_book`: Проверяет, что книга успешно удаляется из библиотеки.
   - `test_find_books_by_title`, `test_find_books_by_author`, `test_find_books_by_year`: Проверяют, что поиск по соответствующим параметрам возвращает ожидаемые результаты.
   - `test_change_status`: Проверяет, что статус книги можно изменить в библиотеке.
   - `test_invalid_status`: Проверяет, что недопустимый статус не может изменить статус книги, и он остается прежним.

# Запуск тестов
Чтобы запустить тесты, вам нужно просто выполнить этот файл. Если вы используете консоль, можно выполнить команду:
python имя_файла.py

Тесты должны пройти, если вся функциональность написана корректно.
