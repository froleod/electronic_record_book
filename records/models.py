from django.db import models
from django.contrib.auth.models import User

class Semester(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер семестра")

    def __str__(self):
        return f"Семестр {self.number}"

class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название предмета")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Семестр")

    def __str__(self):
        return f"{self.name} ({self.semester})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subjects = models.ManyToManyField(Subject, through='Grade', verbose_name="Предметы")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")

    def __str__(self):
        return self.user.username

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    grade = models.IntegerField(verbose_name="Оценка")

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"