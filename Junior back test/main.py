import sys
from db import Database

# Очищает файл логов
open('loger.log', 'w').close()

class Book:
    """
    Класс для представления книги.
    
    Атрибуты:
        id: Идентификатор книги (по умолчанию None).
        title: Название книги.
        author: Автор книги.
        year: Год издания книги.
        status: Статус книги (по умолчанию "В наличии").
    """
    def __init__(self, title: str, author: str, year: int, status: str = "В наличии", id: int = None):
        """
        Инициализация объекта книги.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги (по умолчанию "В наличии").
        :param id: Идентификатор книги (по умолчанию None).
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self) -> str:
        """
        Возвращает строковое представление книги.

        :return: Строка с представлением книги.
        """
        return (
            f"Book(title='{self.title}', author='{self.author}', "
            f"year={self.year}, status='{self.status}')"
        )

    def __str__(self) -> str:
        """
        Возвращает строку с информацией о книге.

        :return: Строка с деталями о книге.
        """
        return f"Book({self.title}, {self.author}, {self.year}, {self.status}, {self.id})"


# Список доступных команд
COMMAND_POOL = [
    'Добавить книгу',
    'Удалить книгу',
    'Поиск книги',
    'Все книги',
    'Изменить статус книги',
    'Выйти'
]

console_input = " "
db = Database()


def print_welcome_message() -> None:
    """
    Выводит приветственное сообщение и описание доступных команд.
    """
    print(""" 
Добро пожаловать в приложение для управления библиотекой! 
Выберите одну из 6 команд:
1. Добавить книгу
2. Удалить книгу
3. Поиск книги
4. Все книги
5. Изменить статус книги
6. Выйти
""")


def format_output(func):
    """
    Декоратор для форматирования вывода результатов запросов.
    
    :param func: Функция, результат которой нужно отформатировать.
    :return: Форматированный вывод.
    """
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)

        if not data:
            return "Нет данных для отображения."

        formatted_output = []
        for book in data:
            formatted_output.append(
                f"ID: {book[0]}\n"
                f"Название: {book[1]}\n"
                f"Автор: {book[2]}\n"
                f"Год издания: {book[3]}\n"
                f"Статус: {book[4] or 'Не указан'}\n"
                f"{'-' * 30}"
            )
        return "\n".join(formatted_output)

    return wrapper


def add_book() -> str:
    """
    Добавляет книгу в базу данных.

    :return: Сообщение о результате добавления книги.
    """
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = int(input("Введите год издания книги: "))
    
    # Дополнительный ввод для статуса, если потребуется
    status = input("Введите статус книги (по умолчанию 'В наличии') или оставьте пустым: ") or "В наличии"
    
    # Создаем экземпляр класса Book
    book = Book(title=title, author=author, year=year, status=status)
    
    return db.add_book(book)


def del_book() -> str:
    """
    Удаляет книгу из базы данных по ID.

    :return: Сообщение о результате удаления книги.
    """
    book_id = int(input("Введите id книги "))
    return db.del_book(book_id)


@format_output
def search_books() -> list:
    """
    Выполняет поиск книг по названию, автору или году издания.

    :return: Список книг, найденных по запросу.
    """
    searching_data = input("Введите название книги или автора, или год издания ")
    return db.search_book(searching_data)


@format_output
def all_books() -> list:
    """
    Получает список всех книг в базе данных.

    :return: Список всех книг.
    """
    return db.all_books()


def update_status() -> str:
    """
    Обновляет статус книги по её ID.

    :return: Сообщение о результате изменения статуса.
    """
    try:
        id = int(input("Введите id книги "))
        status = input("Введите статус книги (в наличии/выдано) ")
        
        if status == "в наличии" or status == "выдано":
            return db.updating_status(id, status)
        else:
            return "Неверный статус"
    except ValueError:
        return "Ошибка: Введено неверное значение для ID."


def main() -> None:
    """
    Главная функция для взаимодействия с пользователем через консоль.
    Обрабатывает команды и выполняет соответствующие функции.
    """
    while True:
        print_welcome_message()
        console_input = input("Введите команду: ").strip()

        if console_input not in COMMAND_POOL:
            print("Неверная команда. Пожалуйста, выберите одну из доступных команд.")
            continue

        if console_input == "Добавить книгу":
            print(add_book())
        elif console_input == "Удалить книгу":
            print(del_book())
        elif console_input == "Поиск книги":
            print(search_books())
        elif console_input == "Все книги":
            print(all_books())
        elif console_input == "Изменить статус книги":
            print(update_status())
        elif console_input == "Выйти":
            print("Программа закрыта.")
            sys.exit()


if __name__ == "__main__":
    main()
