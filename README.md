# Flask Recipe Site

This is a web application that displays recipes. It uses Flask as the backend, SQLAlchemy to interact with a MySQL database, and connects to an external API from RapidAPI. The frontend is built using Bootstrap and CSS.

## Access the Deployed Site

Access the improved recipe site at the following URL:

[https://www.tastyexplorer.com/](https://www.tastyexplorer.com/)

## Table of Contents

- [Installation](#installation)
- [Author](#author)

## Installation

To install this project, follow these steps:

1. Clone the repository: `git clone https://github.com/AfoninSV/flask-recipe-site.git`
2. Navigate to the project directory: `cd <your_path>/flask-recipe-site`
3. Create a `.env` file and add the necessary configuration:
   - API_KEY and API_HOST for the RapidAPI.
   - DB_USERNAME, DB_PASSWORD, DB_HOST, and DB_NAME for the MySQL database.
4. Run the Flask server with the following command: `flask --app web_meal run --debug`

## Author
- Serhii Afonin
- GitHub: [Serhii's GitHub Profile](https://github.com/AfoninSV/)

## Last Updated
- September 2023
