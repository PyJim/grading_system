from helper import  db_execute, db_query
import sqlite3
from flask import render_template, redirect

def signup_empty(name, id_number, email, password):
    first = name == ''
    user = id_number == ''
    email = email == ''
    pwd = password == ''

    return first or user or email or pwd


class PasswordCheck:
    def __init__(self, password1, password2):
        self.password1 = password1
        self.password2 = password2

    def mismatch(self):
        return self.password1 != self.password2

    def not_strong(self):
        return len(self.password1) < 6


class EmailCheck:
    def __init__(self, email):
        self.email = email

    def invalid(self):
        return "@" not in self.email


def create_teacher(name, course_code, email, password):
    query = """INSERT INTO TEACHERS (Full_name, Course_Code, Email, PWD) VALUES (?, ?, ?, ?);"""
    return db_execute(query, [name, course_code, email, password])


def check_teacher(email, course_code):
    query1 = f"""SELECT * FROM TEACHERS WHERE email=?;"""
    query2 = f"""SELECT * FROM TEACHERS WHERE Course_Code=?;"""

    email_check = db_query(query1, [email])
    id_check = db_query(query2, [course_code])
    return [email_check, id_check]


def check_student(index_number, id_number):
    query1 = f"""SELECT * FROM STUDENTS WHERE Student_id=?;"""
    query2 = f"""SELECT * FROM STUDENTS WHERE Student_index=?;"""

    student_id_check = db_query(query1, [id_number])
    index_check = db_query(query2, [index_number])
    return [index_check, student_id_check]


def create_student(name, student_id, index_number, password):
    query = """INSERT INTO STUDENTS (Student_name, Student_id, Student_index, PWD) VALUES (?, ?, ?, ?);"""
    return db_execute(query, [name, student_id, index_number, password])


def find_teacher(course_code):
    query = 'SELECT * FROM TEACHERS WHERE Course_Code=?;'
    return db_query(query, [course_code])


def find_student(student_id):
    query = 'SELECT * FROM STUDENTS WHERE Student_id=?;'
    return db_query(query, [student_id])

def signin_empty(id_number, password):
    user = id_number == ''
    pwd = password == ''
    return user or pwd

def create_course_table(course_code):
    connection = sqlite3.connect('database.db')
    query = f"""CREATE TABLE IF NOT EXISTS {course_code}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Student_id INTEGER NOT NULL UNIQUE,
        IA_SCORE INTEGER,
        EXAM_SCORE INTEGER,
        TOTAL SCORE INTEGER,
        GRADE TEXT)"""
    connection.execute(query)
    connection.commit()
    connection.close()

def create_student_courses(student_id):
    connection = sqlite3.connect('database.db')
    query = f"""CREATE TABLE IF NOT EXISTS {student_id}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Course TEXT NOT NULL,
        IA_SCORE INTEGER,
        EXAM_SCORE INTEGER,
        TOTAL SCORE INTEGER,
        GRADE TEXT)"""
    connection.execute(query)
    connection.commit()
    connection.close()

def add_course(course_code):
    connection = sqlite3.connect('database.db')
    query = """INSERT INTO COURSES (code) VALUES (?);"""
    connection.execute(query, [course_code])
    connection.commit()
    connection.close()

def get_students_by_course(course_code):
    query = f"""SELECT * FROM {course_code};"""
    result = db_query(query)
    return result

def get_student_courses(student_id):
    query = f"""SELECT * FROM {student_id};"""
    result = db_query(query)
    return result

def add_new_course_for_student(student_id, course_code):
    query1 = f"""SELECT * FROM COURSES WHERE code =?;"""
    query2 = f"""SELECT * FROM {student_id} WHERE Course =?"""
    result1 = db_query(query1, [course_code])
    result2 = db_query(query2, [course_code])

    if result1 and not result2:
        connection = sqlite3.connect('database.db')
        query = f"""INSERT INTO {student_id} (Course) VALUES (?);"""
        connection.execute(query, [course_code])
        connection.commit()
        connection.close()
        return redirect(f'student/{student_id}')
    
    elif result1:
        message = 'Already enrolled in this course'
    else:
        message = 'Course does not exist. Please ask your instructor to add the course'
    
    return render_template('new_course.html', message=message)

def add_new_student_to_course(student_id, course_code):
    connection = sqlite3.connect('database.db')
    query = f"""INSERT INTO {course_code} (Student_id) VALUES (?);"""
    connection.execute(query, [student_id])
    connection.commit()
    connection.close()

def get_grade(score):
    if score is not None:
        if score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        elif score >= 40:
            return 'E'
        elif score <= 39:
            return 'F'
    return None

def edit_student_grades(student_id, course_code, IA, exam):
    try:
        total = float(IA) + float(exam)
    except:
        total = None

    grade = get_grade(total)

    #connection = sqlite3.connect('database.db')
    query = f"""UPDATE {course_code} SET IA_SCORE = ?, EXAM_SCORE = ?, TOTAL=?, GRADE=? WHERE Student_id=?;"""
    db_execute(query, [IA, exam, total, grade, student_id])
    #connection.commit()
    query2 = f"""UPDATE {student_id} SET IA_SCORE = ?, EXAM_SCORE = ?, TOTAL=?, GRADE=? WHERE Course=?;"""
    
    db_execute(query2, [IA, exam, total, grade, course_code])
    
    

    
def get_student_grades(student_id, course_id):
    query = f"""SELECT * FROM {course_id} WHERE Student_id =?"""
    result = db_query(query, [student_id])
    return result[0]
