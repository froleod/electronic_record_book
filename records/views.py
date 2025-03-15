from django.shortcuts import render, get_object_or_404
from .models import Student, Grade
from django.shortcuts import render, redirect
from .forms import RegisterForm, SubjectForm, GradeForm
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def student_grades(request):
    student = get_object_or_404(Student, user=request.user)
    grades = Grade.objects.filter(student=student).select_related('subject')
    if not grades.exists():  # Если оценки не найдены
        return render(request, 'records/grades_not_found.html')
    context = {
        'student': student,
        'grades': grades,
    }
    return render(request, 'records/student_grades.html', context)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def is_admin(user):
    return user.student.is_admin

@login_required
@user_passes_test(is_admin)
def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'records/create_subject.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def create_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'records/create_grade.html', {'form': form})
