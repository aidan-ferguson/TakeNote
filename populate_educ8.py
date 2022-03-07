import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_group_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from django.core.files import File

from Educ8.models import CourseFile, Student, Teacher, Course, Flashcard, CourseFile

"""
Things to do:
    Comment functions.
    Create 4 loops for filling database in populate().
    Get someone to check everything.
"""

def populate() -> None:
    
    """
        Define the mock data to be inserted into the database.
        All object attributes will be replaced with the actual database objects after creation
            this is due to the fact that they need to be inserted into other tables
    """

    students = {"Dom1": {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None},
                "Dom2": {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None},
                "Dom3": {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None},
                "Dom4": {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None}}

    teachers = {"Bob1" : {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None},
                "Bob2" : {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None},
                "Bob3" : {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None},
                "Bob4" : {"password":"Password", "first_name":"Dom", "last_name":"Jina", "object":None}}

    courses = {"Maths" : {"createdBy":"Bob1", "students":["Dom1", "Dom2"], "object":None},
               "Extreme Cake Baking" : {"createdBy":"Bob3", "students":["Dom4", "Dom1"], "object":None},
               "English" : {"createdBy":"Bob4", "students":[], "object":None}}

    flashcards = {"Addition Flashcard" : {"question":"What is 1 + 1?", "answer": "2", "createdBy":"Dom1", "Course":"Maths"},
                  "Showdown Winner" : {"question":"Who won the 2008 Jumper Knitting competition?", "answer": "My Gran", "createdBy":"Dom4", "Course":"Extreme Cake Baking"},
                  "Crochet is 4 nerdz" : {"question":"What is better crochet or knitting?", "answer": "Knitting", "createdBy":"Dom2", "Course":"Maths"},
                  "Best Course" : {"question":"Best 2nd year GofU CS course", "answer": "OOSE2", "createdBy":"Dom1", "Course":"Extreme Cake Baking"}}

    """
        Simple loop over all student and teacher data to insert into the database
    """
    for student, student_data in students.items():
        student_data["object"] = add_student(student, student_data["password"], student_data["first_name"], student_data["last_name"])

    for teacher, teacher_data in teachers.items():
        teacher_data["object"] = add_teacher(teacher, teacher_data["password"], teacher_data["first_name"], teacher_data["last_name"])

    """
        We need to determine the actual objects of the students to be added, that is the purpose of the list comprehension
        We also get the actual teacher object in the add_course() call
    """
    for course, course_data in courses.items():
        students_to_add = [students[student]["object"] for student in course_data["students"]]
        course_data["object"] = add_course(course, teachers[course_data["createdBy"]]["object"], students_to_add)
    
    """
        Once again, determine the actual objects of the students and flashcards from their string representation
    """
    for flashcard, flashcard_data in flashcards.items():
        add_flashcard(flashcard, flashcard_data["question"], flashcard_data["answer"], students[flashcard_data["createdBy"]]["object"], courses[flashcard_data["Course"]]["object"])

    course_file = CourseFile(
        course = courses["Maths"]["object"]
    )
    course_file.file.save('manage.py', File(open('manage.py', 'rb')))
    course_file.save()

"""
    For both student and teacher first create the underlying user object and then add a student object to the database
"""
def add_student(Username: str, Password: str, first_name: str, last_name: str) -> Student:
    user = User.objects.get_or_create(username=Username,
                                    first_name = first_name,
                                    last_name = last_name,
                                    password = Password)[0]
    s = Student.objects.get_or_create(user=user)[0]
    return s

def add_teacher(Username: str, Password: str, first_name: str, last_name: str) -> Teacher:
    user = User.objects.get_or_create(username=Username,
                            first_name = first_name,
                            last_name = last_name,
                            password = Password)[0]
    t = Teacher.objects.get_or_create(user=user)[0]
    return t

"""
    Create a course in the database and add the students to it
"""
def add_course(CourseName: str, createdBy: Teacher, studentsToAdd: list) -> Course:
    c = Course.objects.get_or_create(courseName=CourseName, createdBy=createdBy)[0]
    for student in studentsToAdd:
        c.students.add(student)
    c.save()
    return c

"""
    Create a flashcard in the database
"""
def add_flashcard(title: str, question: str, answer: str, createdBy: Student, Course: Course) -> Flashcard:
    f = Flashcard.objects.get_or_create(createdBy=createdBy, course=Course)[0]
    f.title = title
    f.question = question
    f.answer = answer
    f.save()
    return f

if __name__ == '__main__':
    print('Starting Educ8 population script...')
    populate()
