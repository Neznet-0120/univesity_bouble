from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from core.models import Faculty
from news.models import News
from schedule.models import Lesson
from django.http import HttpResponse
from django.utils import timezone
from datetime import date, datetime, timedelta
from icalendar import Calendar, Event
from openpyxl import Workbook
from openpyxl.styles import Font
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from core.models import User
from groups_app.models import StudentGroup
from schedule.models import Lesson


def register(request):
    if request.method ==  "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка отправлена! Ожидайте одобрения администратора факультета.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.status == "approved":
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Ваша заявка ещё на рассмотрении или отклонена.")
        else:
            messages.error(request, "Неверный логин или пароль")
    return render(request, "accounts/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")

def home(request):
    faculties = Faculty.objects.all()
    news = News.objects.filter(is_published=True).order_by("-created_at")[:6]
    return render(request, "public/home.html", {"faculties": faculties, "news":news})

def faculty_detail(request, slug):
    faculty = Faculty.objects.get(slug=slug)
    news = faculty.news.filter(is_published=True).order_by("-created_at")[:10]
    groups = faculty.groups.all()
    return render(request, "public/faculty.html", {
        "faculty": faculty,
        "news": news,
        "groups": groups,
    })

@login_required
def cabinet(request):
    lessons = Lesson.objects.none()

    if request.user.role == "student" and request.user.group:
        lessons = Lesson.objects.filter(group=request.user.group)
    elif request.user.role == "teacher":
        lessons = Lesson.objects.filter(teacher=request.user)
    elif request.user.role == "faculty_admin":
        lessons = Lesson.objects.filter(group__faculty=request.user.faculty)

    return render(request, "accounts/cabinet.html", {
        "lessons": lessons.order_by("day", "time_start"),
        "selected_group": request.user.group if request.user.role == "student" else None
    })


DAYS_ORDER = {
    'monday': 0, 'tuesday': 1, 'wednesday': 2,
    'thursday': 3, 'friday': 4, 'saturday': 5,
    'sunday': 6
}

@login_required
def export_ical(request):
    user = request.user
    if user.role == "student":
        lessons = Lesson.objects.filter(group__students=user)
    elif user.role == "teacher":
        lessons = Lesson.objects.filter(teacher=user)
    else:
        return HttpResponse("Доступ запрещён", status=403)

    cal = Calendar()
    cal.add('prodid', '-//Твой Университет//Расписание 2025//TJ')
    cal.add('X-WR-CALNAME', f"Расписание - {user.get_full_name() or user.username}")


    semester_start = date(2025, 9, 1)
    semester_end = date(2026, 1, 25)

    for lesson in lessons.order_by('day', 'time_start'):
        start_date = semester_start
        while DAYS_ORDER[start_date.strftime("%A").lower()] != DAYS_ORDER.get(lesson.day, 0):
            start_date += timedelta(days=1)

        if lesson.week_type == 'even':
            start_date += timedelta(days=1)
        elif lesson.week_type == 'odd':
            start_date += timedelta(days=14 if  start_date.weekday() >= DAYS_ORDER.get(lesson.day, 0) else 7)
        
        event = Event()
        event.add('summary', f'{lesson.subject} ({lesson.classroom})')
        event.add('dtstart', datetime.combine(start_date, lesson.time_start))
        event.add('dtend', datetime.combine(start_date, lesson.time_end))
        event.add('location', str(lesson.classroom or "-"))
        event.add('description', f"Преподователь: {lesson.teacher}\nГруппа: {lesson.group}")
        event['uid'] = f"lesson-{lesson.id} - {user.id}@university.tj"

        if lesson.week_type in ['even', 'odd']:
            event.add('rrule', {'freq': 'weekly', 'interval': 2, 'until': semester_end})
        else:
            event.add('rrule', {'freq': 'weekly', 'until': semester_end})
        
        cal.add_component(event)
    
    response = HttpResponse(cal.to_ical(), content_type='text/calendar; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="raspisanie{user.username}.ics"'
    return response


@login_required
def export_pdf(request):
    user = request.user
    if user.role == "student":
        lessons = Lesson.objects.filter(group__students=user)
    elif user.role == "teacher":
        lessons = Lesson.objects.filter(teacher=user)
    else:
        return HttpResponse("Доступ запрещён", status=403)

    # Группируем по дням
    days = {}
    for lesson in lessons.order_by('day', 'time_start'):
        day_name = lesson.get_day_display()
        days.setdefault(day_name, []).append(lesson)

    html_string = render_to_string('schedule/pdf_raspisanie.html', {
        'user': user,
        'days': days,
        'today': date.today(),
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="raspisanie_{user.username}.pdf"'
    
    # Генерируем PDF из HTML
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse("Ошибка генерации PDF", status=500)
    
    return response

@login_required
def export_excel(request):
    user = request.user
    if user.role == 'student':
        lessons = Lesson.objects.filter(group__students=user)
    elif user.role == 'teacher':
        lessons = Lesson.objects.filter(teacher=user)
    else:
        return HttpResponse("Доступ запрещён", status=403)
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Расписание"

    headers = ["День", "Время", "Предмет", "Преподаватель", "Группа", "Аудитория", "Тип недели"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for  lesson in lessons.order_by('day', 'time_start'):
        ws.append([
            lesson.get_day_display(),
            f"{lesson.time_start.strftime('%H:%M')} - {lesson.time_end.strftime('%H:%M')}",
            lesson.subject,
            str(lesson.teacher),
            str(lesson.group),
            str(lesson.classroom or "-"),
            lesson.get_week_type_display()
        ])
    
    response = HttpResponse(content_type='application/vnd.openxlmformats-officedocument.spreadsheet.html.sheet')
    response['Content-Disposition'] = f"attachment; filename='raspisanie_{user.username}.xlsx'"
    wb.save(response)
    return response

