from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'Educ8/index.html') 

def home(request):
    pass

def show_course(request, course_name_slug):
    pass

def add_course(request):
    pass

def add_flashcard(request, course_name_slug):
    pass

def show_flashcard(request, course_name_slug, flashcard_name_slug):
    pass
