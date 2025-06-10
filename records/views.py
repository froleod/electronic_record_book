from django.shortcuts import render, get_object_or_404
from .models import Student, Grade
from django.shortcuts import render, redirect
from .forms import RegisterForm, SubjectForm, GradeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from .models import Student
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas

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


@login_required
def export_student_record_pdf(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.user != student.user and not request.user.student.is_admin:
        return HttpResponse("Недостаточно прав", status=403)
    pdfmetrics.registerFont(TTFont('DejaVu', 'records/fonts/DejaVuSansCondensed.ttf'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="record_book_{student.user.username}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    p.setFont("DejaVu", 14)
    width, height = A4
    y = height - 50
    p.drawString(50, y, f"Зачётная книжка: {student.user.get_full_name() or student.user.username}")
    y -= 30
    grades = student.grade_set.select_related('subject', 'subject__semester')
    if not grades.exists():
        p.drawString(50, y, "Оценки не найдены.")
    else:
        for grade in grades:
            control_type_display = grade.subject.get_control_type_display()
            line = f"{grade.subject.name} - {grade.grade} ({control_type_display}, семестр {grade.subject.semester.number})"
            p.drawString(50, y, line)
            y -= 20
            if y < 50:
                p.showPage()
                p.setFont("DejaVu", 14)
                y = height - 50
    p.save()
    return response