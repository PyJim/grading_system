from helper import DATABASE_FILE, get_db, db_execute, db_query
from flask import Flask, render_template, request, g, redirect
from flask_bcrypt import Bcrypt
import os
from queries import signup_empty, PasswordCheck, EmailCheck, check_teacher, create_teacher, check_student, create_student
from queries import signin_empty, find_student, find_teacher, create_course_table, add_course
from queries import get_students_by_course, get_student_courses, create_student_courses
from queries import add_new_course_for_student, add_new_student_to_course
from queries import edit_student_grades, get_student_grades

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/teacher_signup', methods=['GET','POST'])
def teacher_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        course_code = request.form.get('course_code')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if signup_empty(name, course_code, email, password):
            message = 'please fill all available'
            return render_template('teacher_signup.html', message=message)

        user_password = PasswordCheck(password, confirm_password)
        user_email = EmailCheck(email)
        if user_password.mismatch():
            message = 'password mismatch'
            return render_template('teacher_signup.html', message=message)
        elif user_password.not_strong():
            message = 'weak password'
            return render_template('teacher_signup.html', message=message)
        elif user_email.invalid():
            message = 'invalid email'
            return render_template('teacher_signup.html', message=message)

    # checking if user exists already using email and username which are supposed to be unique

        result1 = check_teacher(email, course_code)[0]
        result2 = check_teacher(email, course_code)[1]

        if result1 and result2:
            message = f'{email} and {course_code} already exist'
            return render_template('teacher_signup.html', message=message)
        elif result1:
            message = f'{email} already exist'
            return render_template('teacher_signup.html', message=message)
        elif result2:
            message = f'{course_code} already exist'
            return render_template('teacher_signup.html', message=message)
        else:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            create_teacher(name.capitalize(), course_code, email, password)
            message = f'Account created successfully'
            create_course_table(course_code)
            add_course(course_code)
            return render_template('teacher_signin.html', message=message)
        
    return render_template('teacher_signup.html')


@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        index_number = request.form.get('index_number')
        student_id = request.form.get('student_id')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if signup_empty(name, student_id, index_number, password):
            message = 'please fill all available'
            return render_template('student_signup.html', message=message)

        user_password = PasswordCheck(password, confirm_password)
        
        if user_password.mismatch():
            message = 'password mismatch'
            return render_template('student_signup.html', message=message)
        elif user_password.not_strong():
            message = 'weak password'
            return render_template('student_signup.html', message=message)
        


        result1 = check_student(index_number, student_id)[0]
        result2 = check_student(index_number, student_id)[1]

        if result1 and result2:
            message = f'{index_number} and {student_id} already exist'
            return render_template('student_signup.html', message=message)
        elif result1:
            message = f'{index_number} already exist'
            return render_template('student_signup.html', message=message)
        elif result2:
            message = f'{student_id} already exist'
            return render_template('student_signup.html', message=message)
        else:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            create_student(name.capitalize(), student_id, index_number, password)
            message = f'Account created successfully'
            create_student_courses(student_id)
            return render_template('student_signin.html', message=message)

    return render_template('student_signup.html')



@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        password = request.form.get('password')
    # ensuring that only non empty passwords are allowed
        if signin_empty(course_code, password):
            message = 'please fill all available'
            return render_template('teacher_signin.html', message=message)

        global teacher
        teacher = find_teacher(course_code)
        if teacher:
            teacher = teacher[0]
            correct_password = bcrypt.check_password_hash(teacher[4], password)
            if correct_password:
                students = []
                all_students = get_students_by_course(course_code)
                for student in all_students:
                    students.append(list(student))
                return render_template('teacher.html', students=students, teacher=teacher)
            else:
                message = 'Invalid password'
                return render_template('teacher_signin.html', message=message)
        else:
            message = 'ID number does not exist'
            return render_template('teacher_signin.html', message=message)
    return render_template('teacher_signin.html')


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        password = request.form.get('password')
    # ensuring that only non empty passwords are allowed
        if signin_empty(student_id, password):
            message = 'please fill all available'
            return render_template('student_signin.html', message=message)

        global student
        student = find_student(student_id)
        if student:
            student = student[0]
            correct_password = bcrypt.check_password_hash(student[4], password)
            if correct_password:
                courses = []
                all_courses = get_student_courses(student_id)
                for course in all_courses:
                    courses.append(list(course))
                return render_template('student.html', student=student, courses=courses)
            else:
                message = 'Invalid index number'
                return render_template('student_signin.html', message=message)
        else:
            message = 'ID number does not exist'
            return render_template('student_signin.html', message=message)
    return render_template('student_signin.html')

@app.get('/logout')
def logout():
    global teacher
    global student
    teacher = None
    student = None
    return redirect('/')


@app.route('/teacher/<course_code>', methods=['GET', 'POST'])
def teacher(course_code):
    teacher = find_teacher(course_code)
    if teacher:
        teacher = teacher[0]
        return render_template('teacher.html', teacher=teacher[1])
    else:
        message = 'ID does not exist'
        return render_template('teacher_signin.html', message=message)


@app.route('/student/<id>', methods=['GET', 'POST'])
def student(id):
    if request.method == 'POST':
        return render_template('new_course.html') 
    
    student = find_student(id)
    if student:
        student = student[0]
        return render_template('student.html', student=student[1])
    else:
        message = 'ID does not exist'
        return render_template('student_signin.html', message=message)

@app.route('/add_course', methods=['GET','POST'])
def new_course():
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        student_id = student[2]
        add_new_student_to_course(student_id=student_id, course_code=course_code)
        add_new_course_for_student(student_id, course_code)
        courses = []
        all_courses = get_student_courses(student_id)
        for course in all_courses:
            courses.append(list(course))
        return render_template('student.html', student=student, courses=courses)

@app.route('/edit_grades/<id>', methods=['GET', 'POST'])
def edit_grades(id):
    if request.method == 'POST':
        ia_score = request.form.get('ia_score')
        exam_score = request.form.get('exam_score')
        course_code = teacher[2]
        student_id = id
        print(student_id)
        print(course_code)
        edit_student_grades(student_id, course_code, ia_score, exam_score)
        students = []
        all_students = get_students_by_course(course_code)
        for student in all_students:
            students.append(list(student))
        
        return render_template('teacher.html', students=students, teacher=teacher, course_code=course_code, student_id=student_id)
    course_code = teacher[2]
    student_id = id
    grades = get_student_grades(student_id, course_code)
    print(list(grades))
    return render_template('edit_student_grades.html', grades=grades)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
