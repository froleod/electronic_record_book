from django.contrib import admin
from .models import Semester, Subject, Student, Grade

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('number',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin')
    list_editable = ('is_admin',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade')
