from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    html = render_template("student_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2])

    return html

@app.route("/grade")
def get_grades():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    rows = hackbright_app.show_all_grades(student_github)
    html = render_template("student_info.html", student_github=student_github,
                                                grades=rows)
    return html

@app.route("/show_grades") #This one doesn't work yet
def show_grades():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    rows = hackbright_app.student_grade_project(project_title)
    html = render_template("grades_handler.html", project_title=project_title,
                                                grade=rows)

    return html

if __name__ == "__main__":
    app.run(debug=True)
