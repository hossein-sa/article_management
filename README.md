# Article Management System

## Overview
This Article Management System is a Python-based application that allows users to create, manage, and publish articles. It provides a simple interface for user registration, login, and article manipulation.

## Features
- User Registration and Authentication
- Article Creation and Management
- Publication Status Control
- Article Viewing (for published articles)

## Technologies Used
- Python 3.x
- MySQL Database

## Setup and Installation

### Prerequisites
- Python 3.x
- MySQL Server
- mysql-connector-python library

### Installation Steps
1. Clone the repository:
   git clone https://github.com/hossein-sa/article-management.git

2. Navigate to the project directory:
   cd article-management

3. Install the required Python library:
   pip install mysql-connector-python

4. Set up your MySQL database:
   - Create a new database named `user_article_db` (or choose your own name)
   - Update the database connection details in `database_manager.py`

5. Run the main script:
   python main.py

## Usage
Upon running the application, you'll be presented with a menu:

1. Register: Create a new user account
2. Login: Access your account
3. View Articles: See all published articles
4. Manage Articles: Create, edit, and control publication of your articles (requires login)
5. Exit: Close the application

## File Structure
- `main.py`: Entry point of the application
- `database_manager.py`: Handles database connections and operations
- `user.py`: Defines the User class
- `article.py`: Defines the Article class
- `user_article_manager.py`: Contains the main logic for user and article management

## Contributing
Contributions to improve the Article Management System are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
Hossein Sadeghi - [GitHub](https://github.com/hossein-sa)

Project Link: https://github.com/hossein-sa/article-management
