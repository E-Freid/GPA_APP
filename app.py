import os
from flask import render_template, request, Flask, session, redirect, url_for
from dotenv import load_dotenv
import requests


load_dotenv()
api_url = os.getenv("API_URL")


def handle_course_response(response):
    status_code = response.status_code
    if status_code == 401:
        session.clear()
        return redirect(url_for("login", _external=True))
    return redirect(url_for("courses", _external=True))


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SESSION_SECRET_KEY")


    """ HOME PAGE """
    @app.route("/")
    def index():
        return render_template("index.html")


    """ USER ENDPOINTS """
    @app.route("/login", methods=['POST', 'GET'])
    def login():
        method = request.method
        if method == 'GET':
            response = None
            if 'response' in session:
                response = session.pop('response')
            return render_template("login.html", response=response)
        elif method == 'POST':
            email = request.form["email"].lower()
            password = request.form["password"]
            data = {"email": email, "password": password}
            response = requests.post(f"{api_url}/login", json=data)
            if response.status_code == 200:
                session["logged_in"] = True
                session["access_token"] = response.json()["access_token"]
                return redirect(url_for("courses", _external=True))
            else:
                return render_template("login.html", response=response.json()["error"])


    @app.route("/register", methods=['GET', 'POST'])
    def register():
        method = request.method
        if method == 'GET':
            return render_template("register.html", response=None)
        elif method == 'POST':
            email = request.form["email"].lower()
            password = request.form["password"]
            data = {"email": email, "password": password}
            response = requests.post(f"{api_url}/register", json=data)
            if response.status_code == 201:
                return redirect(url_for("courses", _external=True))
            return render_template("register.html", response=response.json()["message"])


    @app.route("/logout")
    def logout():
        message = "Error while logging out."
        if "logged_in" in session:
            access_token = session["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(f"{api_url}/logout", headers=headers)
            session.clear()
            message = "Logged out successfully."
        session["response"] = message
        return redirect(url_for("login", _external=True))


    """ COURSES ENDPOINTS """
    @app.route("/courses")
    def courses():
        if "logged_in" in session:
            access_token = session["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            courses_response = requests.get(f"{api_url}/user/course", headers=headers)
            gpa_response = requests.get(f"{api_url}/user/gpa", headers=headers)
            if gpa_response.status_code == 200:
                gpa = gpa_response.json()["gpa"]
            else:
                gpa = None
            if courses_response.status_code == 200:
                if "edit_mode" in session:
                    edit_mode = True
                    course_id = session["edit_course_id"]
                    session.pop("edit_mode", None)
                    session.pop("edit_course_id", None)
                    return render_template(
                        "courses.html",
                        courses=courses_response.json(),
                        gpa=gpa,
                        edit_mode=edit_mode,
                        course_id=course_id
                    )
                return render_template("courses.html",
                                       courses=courses_response.json(),
                                       gpa=gpa
                                       )
            elif courses_response.status_code == 401:
                session.clear()
        if "edit_mode" in session:
            session.pop("edit_mode", None)
        return redirect(url_for("login", _external=True))



    @app.route("/add_course", methods=['POST'])
    def add_course():
        if "logged_in" in session:
            access_token = session["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            name = request.form["name"]
            grade = request.form["grade"]
            points = request.form["academic_points"]
            data = {"name": name, "grade": grade, "points": points}
            response = requests.post(f"{api_url}/user/course", headers=headers, json=data)
            return handle_course_response(response)
        return redirect(url_for("login", _external=True))


    @app.route("/delete_course/<int:course_id>", methods=['POST'])
    def delete_course(course_id):
        if "logged_in" in session:
            access_token = session["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(f"{api_url}/user/course/{course_id}", headers=headers)
            return handle_course_response(response)
        return redirect(url_for("login", _external=True))


    @app.route("/edit_course/<int:course_id>", methods=['POST'])
    def edit_course(course_id):
        if "logged_in" in session:
            session["edit_mode"] = True
            session["edit_course_id"] = course_id
            return redirect(url_for("courses", _external=True))
        return redirect(url_for("login", _external=True))


    @app.route("/update_course/<int:course_id>", methods=['POST'])
    def update_course(course_id):
        if "logged_in" in session:
            access_token = session["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            name = request.form["name"]
            grade = request.form["grade"]
            points = request.form["points"]
            data = {"name": name, "grade": grade, "points": points}
            response = requests.put(f"{api_url}/user/course/{course_id}", headers=headers, json=data)
            return handle_course_response(response)
        return redirect(url_for("login", _external=True))

    return app