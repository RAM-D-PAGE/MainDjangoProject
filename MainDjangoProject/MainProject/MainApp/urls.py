from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Anime/', views.page1, name='anime'),
    path('Manga/', views.page2, name='manga'),
    path('person/', views.person, name='person'),
    path('about/', views.about, name='about'),
]