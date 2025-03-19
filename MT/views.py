from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
# trainers/views.py

from .forms import MasterTrainerForm,CourseForm
from .models import Course, Attendance

def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course_list")  # Redirect to course list after saving
    else:
        form = CourseForm()
    
    return render(request, "courses/add_course.html", {"form": form})

def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/course_detail.html", {"course": course})

def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, "attendance/attendance_list.html", {"attendances": attendances})

def attendance_detail(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    return render(request, "attendance/attendance_detail.html", {"attendance": attendance})


def register_trainer(request):
    if request.method == 'POST':
        form = MasterTrainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')  # Redirect to a success page
    else:
        form = MasterTrainerForm()
    return render(request, 'register_mt.html', {'form': form})
