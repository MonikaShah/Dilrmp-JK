"""dilrmp_jk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MT import views
from MT.views import course_list, course_detail, attendance_list, attendance_detail,add_course,upload_mt
from MT.views import feedback_view,feedback_list,feedback_success,quiz_view  # Import feedback_view
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.utils import translation
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('',views.home_page, name='home_page'),
    path('admin/', admin.site.urls),
    path('register/', views.register_trainer, name='register_trainer'),
    path("courses/", course_list, name="course_list"),
    path("courses/<int:course_id>/", course_detail, name="course_detail"),
    path("attendance/", attendance_list, name="attendance_list"),
    path("attendance/<int:attendance_id>/", attendance_detail, name="attendance_detail"),
    path("courses/add/", add_course, name="add_course"),
    #path('success/', views.success, name='success'),  # Define a success view
     path('feedback/', feedback_view, name='feedback_form'),
    path('feedback/list/', feedback_list, name='feedback_list'),
    path('feedback/success/', feedback_success, name='feedback_success'),
    path('upload/', upload_mt, name='upload_mt'),
    path('quiz/', quiz_view, name='quiz'),
    path('quiz/thankyou/', TemplateView.as_view(template_name='quiz_thankyou.html'), name='quiz_thankyou'),
    # path('set_language/', set_language, name='set_language'),  # Ensure this line exists
]
urlpatterns += i18n_patterns(
    path('set_language/', set_language, name='set_language'),
    )