from django.shortcuts import render

from django.shortcuts import render

from .models import Subject


def index(request):

    all_courses = Subject.objects.all() # objects - менеджер
    print("all_courses", all_courses)
    return render(request, "courses/index.html")
