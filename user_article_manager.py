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
        query = "SELECT id, title, summary, is_published FROM articles WHERE user_id = %s"
        self.db.cursor.execute(query, (self.current_user.id,))
        articles = self.db.cursor.fetchall()
        if not articles:
            print("You have no articles.")
        else:
            for i, (id, title, summary, is_published) in enumerate(articles, 1):
                print(f"{i}. Title: {title}")
                print(f"    Summary: {summary}")
                print(f"    Published: {'Yes' if is_published else 'No'}")
                print()
        return articles

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
            print("Note: The article is not published by default. You can publish it by editing its status.")
        except Error as e:
            print(f"Error creating article: {e}")

    def edit_article(self):
        articles = self.view_my_articles()
        if not articles:
            return

        article_id = int(input("Enter the number of the article you want to edit (or 0 to go back): "))

        if article_id == 0:
            return

        if 1 <= article_id <= len(articles):
            article = articles[article_id - 1]
            while True:
                print("\n1. Edit title")
                print("2. Edit summary")
                print("3. Edit content")
                print("4. Change publication status")
                print("5. Back to article management menu")
                edit_choice = input("Enter your choice: ")

                if edit_choice == "1":
                    new_title = input("Enter new article title: ")
                    update_query = "UPDATE articles SET title = %s WHERE id = %s"
                    self.db.cursor.execute(update_query, (new_title, article[0]))
                elif edit_choice == "2":
                    new_summary = input("Enter new article summary: ")
                    update_query = "UPDATE articles SET summary = %s WHERE id = %s"
                    self.db.cursor.execute(update_query, (new_summary, article[0]))
                elif edit_choice == "3":
                    new_content = input("Enter new article content: ")
                    update_query = "UPDATE articles SET content = %s WHERE id = %s"
                    self.db.cursor.execute(update_query, (new_content, article[0]))
                elif edit_choice == "4":
                    new_status = not article[3]  # Toggle the current status
                    update_query = "UPDATE articles SET is_published = %s WHERE id = %s"
                    self.db.cursor.execute(update_query, (new_status, article[0]))
                    print(f"Article is now {'published' if new_status else 'unpublished'}")
                elif edit_choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again")

                self.db.connection.commit()

            print("Returning to article management menu...")
        else:
            print("Invalid article number.")

