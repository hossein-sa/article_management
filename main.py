from user_article_manager import UserArticleManager


def main():
    manager = UserArticleManager()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. View Articles")
        print("4. Manage Articles")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            national_code = input("Enter your national code: ")
            birthday = input("Enter your birthday (YYYY-MM-DD): ")
            password = input("Enter your password: ")
            manager.register(username, national_code, birthday, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            manager.login(username, password)
        elif choice == '3':
            manager.view_articles()
        elif choice == '4':
            if manager.current_user:
                manager.view_articles()
            else:
                print("Please login first.")
        elif choice == '5':
            print("Tank you for using the program. Goodbye!")
            manager.db.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
