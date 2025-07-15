from django.shortcuts import render
from django.http import HttpResponse
from . models import Person

def index(request):
    return render(request, 'index.html')
def page1(request):
    return render(request,'Anime.html')
def page2(request):
    return render(request,'Manga.html')
def person(request):
    all_persons = Person.objects.all()
    return render(request, 'person.html', {'persons': all_persons})
def about(request):
    return render(request, 'about.html')