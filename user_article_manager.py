from database_manager import DatabaseManager
from user import User
from article import Article
from mysql.connector import Error
import datetime


class UserArticleManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None

    def register(self, username, national_code, birthday, password):
        query = "INSERT INTO users (username, national_code, birthday, password) VALUES (%s, %s, %s, %s)"
        values = (username, national_code, birthday, password)
        try:
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("User registered successfully")
        except Error as e:
            print(f"Error registering user: {e}")

    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        self.db.cursor.execute(query, values)
        user_data = self.db.cursor.fetchone()
        if user_data:
            self.current_user = User(*user_data)
            print(f"Welcome {username}")
            return True
        else:
            print("Invalid username or password")
            return False

    def view_articles(self):
        query = "SELECT title, summary FROM articles WHERE is_published = TRUE"
        self.db.cursor.execute(query)
        articles = self.db.cursor.fetchall()
        if not articles:
            print("No published articles")
        else:
            for i, (title, summary) in enumerate(articles, 1):
                print(f"{i}. Title: {title}")
                print(f"    summary: {summary}")
                print()

    def manage_articles(self):
        while True:
            print("\n1. View my articles")
            print("2. Create new article")
            print("3. Edit article")
            print("4. Back to main menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_my_articles()
            elif choice == '2':
                self.create_article()
            elif choice == '3':
                self.edit_article()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def view_my_articles(self):
        query = "SELECT id, title, summary, content, created_at, is_published FROM articles WHERE user_id = %s"
        self.db.cursor.execute(query, (self.current_user.id,))
        articles = self.db.cursor.fetchall()
        if not articles:
            print("You have no articles.")
        else:
            for i, article_data in enumerate(articles, 1):
                article = Article(*article_data, self.current_user.id)
                print(f"{i}. Title: {article.title}")
                print(f"    summary: {article.summary}")
                print(f"    published: {'YES' if article.is_published else 'NO'}")
                print()

    def create_article(self):
        title = input("Enter article title: ")
        summary = input("Enter article summary: ")
        content = input("Enter article content: ")
        query = "INSERT INTO articles (title, summary, content, created_at, is_published, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (title, summary, content, datetime.datetime.now(), False, self.current_user.id)
        try:
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("Article created successfully")
        except Error as e:
            print(f"Error creating article: {e}")

    def edit_article(self):
        self.view_my_articles()
        article_id = int(input("Enter the number of the article you want to edit: "))
        query = "SELECT id, title, summary, content, created_at, is_published FROM articles WHERE user_id = %s"
        self.db.cursor.execute(query, (self.current_user.id,))
        articles = self.db.cursor.fetchall()

        if 1 < article_id <= len(articles):
            article = Article(*articles[article_id - 1], self.current_user.id)
            print("1. Edit title")
            print("2. Edit summary")
            print("3. Edit content")
            print("4. Change publication status")
            edit_choice = input("Enter your choice: ")

            if edit_choice == "1":
                new_title = input("Enter new article title: ")
                update_query = "UPDATE articles SET title = %s WHERE id = %s"
                self.db.cursor.execute(update_query, (new_title, article_id))
            elif edit_choice == "2":
                new_summary = input("Enter new article summary: ")
                update_query = "UPDATE articles SET summary = %s WHERE id = %s"
                self.db.cursor.execute(update_query, (new_summary, article_id))
            elif edit_choice == "3":
                new_content = input("Enter new article content: ")
                update_query = "UPDATE articles SET content = %s WHERE id = %s"
                self.db.cursor.execute(update_query, (new_content, article_id))
            elif edit_choice == "4":
                new_status = not article.is_published
                update_query = "UPDATE articles SET is_published = %s WHERE id = %s"
                self.db.cursor.execute(update_query, (new_status, article_id))
                print(f"Article is now {'published' if new_status else 'unpublished'}")
            else:
                print("Invalid choice. Please try again")

            self.db.connection.commit()
        else:
            print("Invalid article number.")

