import sqlite3

DB = None
CONN = None

# find student by github handle
def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

    # """\
    #     Student: %s %s
    #     Github account: %s""" % (row[0], row[1], row[2])

# add a student
def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

# query for projects by title
def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
        Project Title: %s
        Description: %s
        Maximum grade: %d""" % (row[0], row[1], row[2])

# add a project
def add_project(title, description, max_grade):
    query = """INSERT INTO Projects values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added Project: %s %s %s" % (title, description, max_grade)

# query for a student's grade given a project
def student_grade_project(project_title):
    query = """SELECT student_github, project_title, grade FROM Grades WHERE project_title = ?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    return rows

# give a grade to a student
def give_grade_to_student(student_github, project_title, grade):
    query = """INSERT INTO Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added: %s, %s, %s to Grades." % (student_github, project_title, grade)

# show all the grades for a student
def show_all_grades(student_github):
    query = """SELECT student_github, project_title, grade FROM Grades WHERE student_github = ?"""
    DB.execute(query, (student_github,))
    rows = DB.fetchall()

    return rows

# database connection
def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(' ', 1)
        command = tokens[0]
        args = tokens[1:]
        args = args[0].split(", ")
        print args

        if command == "student":
            get_student_by_github(*args)
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_title":
            get_project_by_title(*args)
        elif command == "add_project":
            add_project(*args)
        elif command == "give_project_name":
            student_grade_project(*args)
        elif command == "add_grade":
            give_grade_to_student(*args)
        elif command == "show_all_grades":
            show_all_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
