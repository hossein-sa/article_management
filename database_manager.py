import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='toor',
                database='user_article_db'
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.create_tables()
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def create_tables(self):
        create_user_table = """
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        national_code VARCHAR(20) UNIQUE NOT NULL,
        birthday DATE NOT NULL,
        password VARCHAR(100) NOT NULL
        )"""

        create_article_table="""
        CREATE TABLE IF NOT EXISTS articles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        summary TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        is_published BOOLEAN NOT NULL,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users (id)
        )"""

        self.cursor.execute(create_user_table)
        self.cursor.execute(create_article_table)
        self.connection.commit()

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

