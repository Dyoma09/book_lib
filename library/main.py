import json
import os

class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self):
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"

class Library:
    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                return [Book(book_id=book['id'], title=book['title'], author=book['author'], year=book['year'], status=book['status']) for book in json.load(file)]
        return []

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {book_id}.")

    def remove_book(self, book_id: int):
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_books(self, **kwargs):
        results = self.books
        for key, value in kwargs.items():
            results = [book for book in results if getattr(book, key) == value]
        return results

    def display_books(self):
        if not self.books:
            print("Библиотека пуста.")
        else:
            for book in self.books:
                print(book)

    def change_status(self, book_id: int, new_status: str):
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            book.status = new_status
            self.save_books()
            print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)

        elif choice == '3':
            search_by = input("Искать по (title/author/year): ")
            search_value = input(f"Введите значение для поиска по {search_by}: ")
            if search_by == 'year':
                search_value = int(search_value)
            results = library.find_books(**{search_by: search_value})
            if results:
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_status(book_id, new_status)

        elif choice == '6':
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()