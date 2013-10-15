from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    github_name = request.args.get("github")

    student = hackbright_app.get_student_by_github(github_name)
    grades = hackbright_app.show_all_grades(github_name)

    html = render_template("student_info.html",
        first_name=student[0],
        last_name=student[1],
        github=student[2],
        grades=grades,
    )
    return html

@app.route("/grade")
def get_grades():
    raise TypeError
    hackbright_app.connect_to_db()
    github = request.args.get("github")

    student = hackbright_app.get_student_by_github(github)
    projects = hackbright_app.show_all_grades(github)

    html = render_template("student_info.html",
        first_name=student[0],
        last_name=student[1],
        github=student[2],
        projects=projects,
    )
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
