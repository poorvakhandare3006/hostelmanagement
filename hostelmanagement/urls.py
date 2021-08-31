"""HostelManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url ,include
from django.urls import path
from django.views.generic.base import TemplateView
from website import views
# from forms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('logout/',views.logoutuser,name="logout"),
    path('login/',views.loginuser,name='login'),
    path('add_student/',views.add_student,name='add_student'),
    path('add_timetable/',views.add_timetable,name='add_timetable'),
    path('gatepass/',views.gatepass,name='gatepass'),
    path(r'^approve_gatepass/(?P<id>\d+)/$',views.approve_gatepass,name='approve_gatepass'),
    path(r'^approve_exit_visitor/(?P<id>\d+)/$',views.approve_exit_visitor,name='approve_exit_visitor'),
    path('so_gatepass/',views.so_gatepass,name='so_gatepass'),
    path('student_gatepass/',views.student_gatepass,name='student_gatepass'),
    path('add_entry/',views.add_entry,name='add_entry'),
    path('add_exit/',views.add_exit,name='add_exit'),
    path('view_history/',views.view_history,name='view_history'),
    path('out_students/',views.out_students,name='out_students'),
    path('add_visitor/',views.add_visitor,name='add_visitor'),
    path('exit_visitor/',views.exit_visitor,name='exit_visitor'),
    path('exit_visitor_so/',views.exit_visitor_so,name='exit_visitor_so'),
    path('visitor/',views.visitor,name='visitor'),


]
