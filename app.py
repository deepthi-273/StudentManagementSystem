import webbrowser
from flask import Flask, render_template, request, redirect, session
import sqlite3


app = Flask(__name__)
app.secret_key = "student_management_secret"

@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")
    

    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE course='BCA'"
    )
    bca_students = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE course='BSc'"
    )
    bsc_students = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE course='BCom'"
    )
    bcom_students = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        bca_students=bca_students,
        bsc_students=bsc_students,
        bcom_students=bcom_students
    )

@app.route("/students")
def students():

    search = request.args.get("search", "")

    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    if search:

        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + search + '%',)
        )

    else:

        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )



@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        conn = sqlite3.connect("database/database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
            (name, age, course)
        )

        conn.commit()
        conn.close()

        return redirect("/students")

    return render_template("add_student.html")
@app.route("/edit-student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        cursor.execute(
            """
            UPDATE students
            SET name=?, age=?, course=?
            WHERE id=?
            """,
            (name, age, course, id)
        )

        conn.commit()
        conn.close()

        return redirect("/students")

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )

@app.route("/delete-student/<int:id>")
def delete_student(id):

    conn = sqlite3.connect("database/database.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect("/students")



@app.route("/student/<int:id>")
def student_details(id):

    conn = sqlite3.connect("database/database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "student_details.html",
        student=student
    )




@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        conn = sqlite3.connect("database/database.db")

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (username, password)
        )


        user = cursor.fetchone()


        conn.close()


        if user:

            session["username"] = username

            return redirect("/")


        else:

            return "Invalid Username or Password"


    return render_template("login.html")
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/login")

if __name__ == "__main__":
      webbrowser.open("http://127.0.0.1:5000")

      app.run(debug=True)