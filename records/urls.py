from django.urls import path
from . import views

urlpatterns = [
    path('grades/', views.student_grades, name='student_grades'),
    path('register/', views.register, name='register'),

]
