from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.person, name='index'),  # หน้าแรกเป็นรายชื่อพนักงาน
    path('about/', views.about, name='about'),
    
    # Person management
    path('person/', views.person, name='person'),
    path('form/', views.from_view, name='from_view'),
    path('delete-person/', views.delete_person, name='delete_person'),
]