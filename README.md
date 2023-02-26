# GPA Tracker Web Application

This is a web application that allows users to track their academic courses and calculate their GPA. The app is built using Flask, SQLAlchemy, and JWT authentication.

link for the web app : https://academic-tracker.onrender.com

## Getting Started

To get started with the GPA Tracker web application, follow these steps:

1. Clone this repository to your local machine.
2. Clone the REST API I have created as the backend here: https://github.com/E-Freid/GPA_REST_API
3. Install the necessary Python packages using `pip install -r requirements.txt`.
4. Create a new PostgreSQL database for the app.
5. Create a `.env` file with the following environment variables:
   - `DATABASE_URL`: the URL of your PostgreSQL database.
   - `SESSION_SECRET_KEY`: a secret key used for session encrypting.
6. Run the app using `python app.py`.

## Features - Using the REST API I have created

- User authentication and authorization using JWT tokens.
- CRUD operations for academic courses.
- Calculation of GPA based on course grades.
- Responsive design that works on desktop and mobile devices.

## Technologies Used

- Flask: a lightweight web framework for Python.
- SQLAlchemy: an ORM that allows us to interact with databases using Python.
- PostgreSQL: a powerful open-source relational database system.
- JWT authentication: a stateless authentication mechanism using JSON Web Tokens.

## Future Improvements

- Add support for multiple semesters.
- Allow users to set their own grading scales.
- Implement data visualization of course grades and GPA.

## Credits

- ChatGPT for help with the html and css files.
