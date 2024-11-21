import sqlite3 as sq
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования 
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат вывода сообщений
    filename="loger.log",  # Логирование в файл
    filemode="a",  # Добавление сообщений в файл
    encoding='utf-8',  # Кодировка для записи в файл
    datefmt='%Y-%m-%d %H:%M:%S',  # Формат времени в логах
)

class Database:
    """
    Класс для работы с базой данных SQLite.
    Позволяет подключаться к базе данных, выполнять CRUD операции с таблицей 'library'.
    """
    def __init__(self, db_path="bot_db.db"):
        """
        Инициализация объекта Database.

        :param db_path: Путь к базе данных (по умолчанию 'bot_db.db').
        """
        self.db_path = db_path  # Путь к базе данных

    def connect(self) -> sq.Connection:
        """
        Устанавливает подключение к базе данных.

        :return: объект подключения к базе данных.
        """
        logging.info("Connecting to the database...")
        conn = sq.connect(self.db_path)  # Подключение к базе данных
        conn.text_factory = str  # Установка текстовой фабрики для обработки строк
        return conn 

    def all_books(self) -> list:
        """
        Извлекает все книги из базы данных.

        :return: Список всех книг (или пустой список в случае ошибки).
        """
        try:
            with self.connect() as db:
                cur = db.cursor()
                cur.execute("SELECT * FROM library")  # Запрос на выбор всех книг
                books = cur.fetchall()  # Извлечение всех записей
                logging.info(f"Fetched all books: {books}")
                return books
        except sq.Error as e:
            logging.error(f"An error occurred while fetching all books: {e}")
            return []

    def add_book(self, book) -> str:
        """
        Добавляет новую книгу в базу данных.

        :param book: объект книги с аттрибутами title, author, year и status.
        :return: Сообщение о результате операции.
        """
        try:
            with self.connect() as db:
                cur = db.cursor()
                
                # Проверка на существование книги в базе данных
                cur.execute("SELECT * FROM library WHERE title = ? AND author = ? AND year = ?", 
                            (book.title, book.author, book.year))
                if cur.fetchone():
                    logging.warning(f"Book already exists in the database: {book.title} by {book.author}")
                    return "Book already exists in the database."
                
                # Вставка новой книги
                cur.execute("INSERT INTO library (title, author, year, status) VALUES (?, ?, ?, ?)", 
                            (book.title, book.author, book.year, book.status))
                db.commit()  # Сохранение изменений
                logging.info(f"Book added successfully: {book.title} by {book.author}")
                return "Книга успешно добавлена!"
        except sq.Error as e:
            logging.error(f"An error occurred while adding a book: {e}")
            return f"An error occurred: {e}"

    def del_book(self, book_id: int) -> str:
        """
        Удаляет книгу из базы данных по её идентификатору.

        :param book_id: ID книги, которую нужно удалить.
        :return: Сообщение о результате операции.
        """
        try:
            with self.connect() as db:
                cur = db.cursor()
                cur.execute("SELECT * FROM library WHERE id = ?", (book_id,))  # Проверка на наличие книги
                book = cur.fetchone()
                if not book:
                    logging.warning(f"Book with ID {book_id} not found.")
                    return "Книга не найдена"
                
                # Удаление книги из базы данных
                cur.execute("DELETE FROM library WHERE id = ?", (book_id,))
                db.commit()  # Сохранение изменений
                logging.info(f"Book with ID {book_id} deleted successfully.")
                return "Book deleted successfully."
        except sq.Error as e:
            logging.error(f"An error occurred while deleting a book: {e}")
            return f"An error occurred: {e}"

    def search_book(self, searching_data: str) -> list:
        """
        Выполняет поиск книги по title, author или year.

        :param searching_data: Строка для поиска в базе данных.
        :return: Список книг, которые соответствуют поисковому запросу.
        """
        try:
            with self.connect() as db:
                cur = db.cursor()
                cur.execute("SELECT * FROM library WHERE title LIKE ? OR author LIKE ? OR year=?", 
                            (f"%{searching_data}%", f"%{searching_data}%", searching_data))
                books = cur.fetchall()  # Извлечение всех книг, соответствующих поисковому запросу
                if not books:
                    logging.warning(f"No books found matching: {searching_data}")
                    return "Книги не найдены"
                
                logging.info(f"Books found: {books}")
                return books
        except sq.Error as e:
            logging.error(f"An error occurred while searching for books: {e}")
            return f"An error occurred: {e}"

    def updating_status(self, book_id: int, status: str) -> str:
        """
        Обновляет статус книги по её ID.

        :param book_id: ID книги, чей статус нужно обновить.
        :param status: Новый статус книги.
        :return: Сообщение о результате операции.
        """
        try:
            with self.connect() as db:
                cur = db.cursor()
                cur.execute("SELECT * FROM library WHERE id=?", (book_id,))  # Проверка на существование книги
                book = cur.fetchone()
                if not book:
                    logging.warning(f"Book with ID {book_id} not found for status update.")
                    return "Книга не найдена"
                
                # Обновление статуса книги
                cur.execute("UPDATE library SET status=? WHERE id=?", (status, book_id))
                db.commit()  # Сохранение изменений
                logging.info(f"Book with ID {book_id} status updated to {status}.")
                return f"Статус книги обновлен до {status}."
        except sq.Error as e:
            logging.error(f"An error occurred while updating book status: {e}")
            return f"An error occurred: {e}"
