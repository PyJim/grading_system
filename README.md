# Online Grading System Documentation (GradeWise)
## Introduction
The Online Grading System is a web-based application that allows users to register for courses and track their academic progress. The application is built using Python Flask framework and SQLite3 database.

## Features
### User Authentication
Users can sign up as a teacher or a student.
Passwords are encrypted using the Werkzeug security library.
Users can log in and log out of the system.
Course Registration
Students can register for courses that are already in the system (Have teachers registered for it).
Each course has a unique course code.
Students can view the list of courses they are currently registered for.

### Grading System
Teachers can assign grades to each student in a course.
Students can view their grades for each course they are registered for.
Teachers can update grades as deemed fit.

## Installation process
### Prerequisites
Python 3.x installed
Flask library installed
SQLite3 database installed

### Setup
Clone the repository to your local machine
Navigate to the grading system directory in your terminal
Run the following command to install the required packages:

#### pip install -r requirements.txt

### Usage
To start the server, run the following command in your terminal:
#### python app.py
Open your browser and navigate to http://localhost:5000/ to access the login page.

### Web Version
This app will soon be hosted and made accessible for all.

## Conclusion
The Online Grading System is an easy-to-use, efficient tool for tracking academic progress. It provides a platform for both teachers and students to manage grades and courses.

### Image description of the workflow

1. ![](image/Screenshot%20(174).png)
2. ![](image/Screenshot%20(175).png)
3. ![](image/Screenshot%20(176).png)
4. ![](image/Screenshot%20(177).png)
5. ![](image/Screenshot%20(178).png)
6. ![](image/Screenshot%20(179).png)
7. ![](image/Screenshot%20(180).png)
8. ![](image/Screenshot%20(181).png)

### Future Updates
1. Student verification and acceptance or rejection by course intructors.
2. Regrade requests.
3. Hosting the platform on an actual hosting site.

###
Here is a video demo of the project
[link]