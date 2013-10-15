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


@app.route("/create_student")
def create_student():
    hackbright_app.connect_to_db()

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")

    exists = hackbright_app.get_student_by_github(github)

    if not exists:
        exists = hackbright_app.make_new_student(
            first_name,
            last_name,
            github,
        )

    return "Success: %s %s %s" % exists


@app.route("/create_project")
def create_project():
    hackbright_app.connect_to_db()

    project_title = request.args.get('project_title')
    project_description = request.args.get('project_description')
    project_max_grade = request.args.get('project_max_grade')

    exists = hackbright_app.get_project_by_title(project_title)

    if not exists:
        exists = hackbright_app.add_project(
            project_title,
            project_description,
            project_max_grade,
        )

    return "Success: %s %s %s" % exists


@app.route("/create_grade")
def create_grade():
    hackbright_app.connect_to_db()

    student_github = request.args.get('student_github')
    project_title = request.args.get('project_title')
    grade = request.args.get('grade')

    grades = hackbright_app.student_grade_project(project_title)

    does_exist = False

    for grade in grades:
        if grade[0] == student_github:
            does_exist = True
            break

    if not does_exist:
        grade = hackbright_app.give_grade_to_student(
            student_github,
            project_title,
            grade,
        )
        return "Success: %s %s %s" % grade
    else:
        return "Student %s already has a grade for this project" % student_github


@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")

    grades = hackbright_app.student_grade_project(project_title)

    html = render_template(
        "project_info.html",
        project_title=project_title,
        grades=grades,
    )

    return html


if __name__ == "__main__":
    app.run(debug=True)
