from django.db import models
from django.contrib.auth.models import User

class Semester(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер семестра")

    def __str__(self):
        return f"Семестр {self.number}"

class Subject(models.Model):
    EXAM = 'exam'
    CREDIT = 'credit'
    COURSEWORK = 'coursework'

    CONTROL_TYPES = [
        (EXAM, 'Экзамен'),
        (CREDIT, 'Зачёт'),
        (COURSEWORK, 'Курсовая работа'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название предмета")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Семестр")
    control_type = models.CharField(
        max_length=12,
        choices=CONTROL_TYPES,
        default=EXAM,
        verbose_name="Тип контроля"
    )

    def __str__(self):
        return f"{self.name} ({self.get_control_type_display()}, семестр {self.semester.number})"



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subjects = models.ManyToManyField(Subject, through='Grade', verbose_name="Предметы")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")

    def __str__(self):
        return self.user.username

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    grade = models.CharField(max_length=10, verbose_name="Оценка")

    def clean(self):
        from django.core.exceptions import ValidationError
        control_type = self.subject.control_type

        if control_type in [Subject.EXAM, Subject.COURSEWORK]:
            if not self.grade.isdigit() or int(self.grade) not in range(2, 6):
                raise ValidationError("Оценка должна быть числом от 2 до 5.")
        elif control_type == Subject.CREDIT:
            if self.grade.lower() not in ['зачет', 'незачет']:
                raise ValidationError("Для зачёта допустимы значения: 'зачет' или 'незачет'.")

