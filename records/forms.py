from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subject, Grade

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'semester']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        grade = cleaned_data.get('grade')

        if subject and grade:
            ct = subject.control_type
            if ct in [Subject.EXAM, Subject.COURSEWORK]:
                if not grade.isdigit() or int(grade) not in range(2, 6):
                    raise forms.ValidationError("Оценка должна быть от 2 до 5.")
            elif ct == Subject.CREDIT:
                if grade.lower() not in ['зачет', 'незачет']:
                    raise forms.ValidationError("Зачёт: допустимо только 'зачет' или 'незачет'.")


