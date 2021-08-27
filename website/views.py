from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from website.models import Gatepass, UserProfile
from website.models import Timetable,Entry
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import template
from django.contrib.auth import login as loginn
from django.conf import settings
register = template.Library()
# Create your views here.
from django.utils import timezone
from website.tasks import send_mail_parents
from datetime import time



def home(request):
	return render(request, 'room/index.html')


@login_required
def logoutuser(request):
	logout(request)
	return redirect('/')


def loginuser(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			loginn(request, user)

			if user.is_active:
				loginn(request, user)

				return render(request, "room/index.html")
			else:
				HttpResponse("Inactive User.")
				return render(request, "room/index.html")
		else:
			return render(request, "login_members.html")
	else:
		return render(request, "login_members.html")


@login_required
def add_student(request):
	if(request.user.userprofile.academics == True):
		if request.method == "POST":
			name = request.POST.get('name', '')
			email = request.POST.get('email', '')
			password = request.POST.get('password', '')
			hostel = request.POST.get('hostel', '')
			address = request.POST.get('address', '')
			s_contact = request.POST.get('scontact', '')
			p_contact = request.POST.get('pcontact', '')
			p_email = request.POST.get('pemail', '')
			enroll = request.POST.get('enroll', '')
			gender = request.POST.get('gender', '')
			room_no = request.POST.get('room', '')
			course = request.POST.get('course', '')
			roll = request.POST.get('roll', '')
			user = User.objects.create_user(
				username=email, email=email, password=password, first_name=name, last_name='student')
			user.is_active = True
			
			profile = user.userprofile
			profile.hostel = hostel
			profile.address = address
			profile.p_contact = p_contact
			profile.s_contact = s_contact
			profile.enroll = enroll
			profile.gender = gender
			profile.room = room_no
			profile.pemail = p_email
			profile.student = True
			profile.academics = False
			profile.so = False
			profile.guard = False
			profile.course = course
			profile.roll = roll
			profile.save()
			user.save()
			
			# thank = True

			return render(request, 'add_student.html')
		else:
			return render(request, "add_student.html")
	else:
		return render(request, '')

@login_required
def add_timetable(request):
	if(request.user.userprofile.academics == True):
		if request.method == "POST":
			course_name = request.POST.get('name', '')
			faculty = request.POST.get('facutly', '')
			course_code= request.POST.get('coursecode', '')
			batch = request.POST.get('batch', '')
			m = request.POST.get('m', '')
			t = request.POST.get('t', '')
			w = request.POST.get('w', '')
			tt = request.POST.get('tt', '')
			f = request.POST.get('f', '')
			user = Timetable(
				course_name=course_name, course_code=course_code, faculty=faculty, batch=batch, m=m,t=t,w=w,tt=tt,f=f)
			user.save()
		

			return render(request, 'add_timetable.html')
		else:
			return render(request, "add_timetable.html")
	else:
		return render(request, '')


@login_required
def gatepass(request):
	if(request.user.userprofile.student == True):
		if request.method == "POST":
			email = request.user.username
			reason = request.POST.get('reason', '')
			date= request.POST.get('date', '')
			home = request.POST.get('home', '')
			user = Gatepass(
				email=email, reason=reason, date=date,home=home)
			user.save()
			# thank = True

			return render(request, 'gatepass.html')
		else:
			return render(request, "gatepass.html")
	else:
		return render(request, '')
@login_required
def approve_gatepass(request, *args, **kwargs):
	if(request.user.userprofile.so == True):
		id = kwargs['id']
		Gatepass.objects.filter(pk=id).update(approved=True)
		return render(request, 'so_gatepass.html')
	else:
		return render(request, "room/index.html")

@login_required
def so_gatepass(request):
	if(request.user.userprofile.so == True):
		context = Gatepass.objects.filter(approved=False)
		context_dict = {
			'context':context
		}
		return render(request, 'so_gatepass.html',context_dict)
	else:
		return render(request, '')

@login_required
def student_gatepass(request):
	if(request.user.userprofile.student == True):
		context = Gatepass.objects.filter(email=request.user.username)
		context_dict = {
			'context':context
		}
		return render(request, 'student_gatepass.html',context_dict)
	else:
		return render(request, '')

import pytz
@login_required
def add_entry(request):
	if(request.user.userprofile.guard == True):
		if request.method == "POST":
			roll = request.POST.get('roll', '')
			name = "Entry"
			user = Entry(roll=roll,name=name)
			user.save()
			mail = str(roll)+'@iiitg.com'
			# mail = "new@a.com"
			timezone.activate(pytz.timezone("Asia/Kolkata"))
			obj = User.objects.filter(username=mail).first()
			person = UserProfile.objects.filter(user=obj).first()		
			UserProfile.objects.filter(user=obj).update(out=False)
			print("<<-------------------------------------->>")
			print(timezone.now())
			UserProfile.objects.filter(user=obj).update(in_time=timezone.now())
			in_time_mx = time(23, 00, 00)
				
			if(int(timezone.now().strftime("%H"))>in_time_mx.hour):
				print("<<-------------------------------------->>")
				print(person.due)
							
				if(person.due==0):
					UserProfile.objects.filter(user=obj).update(due=1)
				elif(person.due==1):
					UserProfile.objects.filter(user=obj).update(due=2)
				elif(person.due==2):
					UserProfile.objects.filter(user=obj).update(due=0)
					to_mail = person.p_mail
					send_mail_parents.delay(to_mail)

			return render(request, 'add_entry.html')
		else:
			return render(request, 'add_entry.html')
	else:
		return render(request, '')

@login_required
def add_exit(request):
	if(request.user.userprofile.guard == True):
		if request.method == "POST":
			roll = request.POST.get('roll', '')
			name = "Exit"
			user = Entry(roll=roll,name=name)
			user.save()

			mail = str(roll)+'@iiitg.com'
			# mail = "new@a.com"
			obj = User.objects.filter(username=mail).first()
			oo = UserProfile.objects.filter(user=obj).first()
			UserProfile.objects.filter(user=obj).update(out=True)
			UserProfile.objects.filter(user=obj).update(out_time=timezone.now())
		
			return render(request, 'add_exit.html')
		else:
			return render(request, 'add_exit.html')
	else:
		return render(request, '')

@login_required
def view_history(request):
	if(request.user.userprofile.so == True):
		context = Entry.objects.all()
		context_dict = {
			'context':context
		}
		return render(request, 'view_history.html',context_dict)
	else:
		return render(request, '')

@login_required
def out_students(request):
	if(request.user.userprofile.so == True or request.user.userprofile.guard==True) :
		all = UserProfile.objects.filter(out=True)
		context_dict = {
			'context':all
		}
		print(context_dict)
		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJ")
		return render(request, 'out_students.html',context_dict)
	else:
		return render(request, '')





