from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from django.db.models.deletion import SET_NULL

class Batch(models.Model):
	course_name = models.CharField(max_length=30)
	course_year = models.IntegerField()
	course_code = models.CharField(max_length=30,unique=True)

	class Meta:
		unique_together = ('course_name','course_year')
	
	def __str__(self):
		return str(self.course_name)

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50,null=True)
	enroll = models.CharField(max_length=10,null=True)
	hostel = models.CharField(max_length=10,null=True)
	course = models.CharField(max_length=20,null=True)
	roll = models.CharField(max_length=20,null=True,unique=True)
	gender = models.CharField(max_length=10,null=True)
	batch = models.ForeignKey(Batch, on_delete=SET_NULL, null=True)
	s_contact = models.CharField(max_length=9999999999, null=True)
	p_contact = models.CharField(max_length=9999999999, null=True)
	p_mail = models.CharField(max_length=9999999999, null=True)
	student = models.BooleanField(default=False)
	so = models.BooleanField(default=False)
	academics = models.BooleanField(default=False)
	guard = models.BooleanField(default=False)
	date_time = models.DateTimeField(default=timezone.now) 
	out_time = models.DateTimeField(null=True)
	in_time = models.DateTimeField(null=True)
	out_reason = models.BooleanField(default=False)
	out = models.BooleanField(default=False)
	due = IntegerField(default=0)
	
	def __str__(self):
		return str(self.name)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
	   profile, created = UserProfile.objects.get_or_create(user=instance)
	   # profile, created = Booking.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Gatepass(models.Model):
	email = models.CharField(max_length=50,null=True)
	reason = models.CharField(max_length=50,null=True)
	date = models.CharField(max_length=10,null=True)
	home = models.CharField(max_length=10,null=True)
	approved = models.BooleanField(default=False)

	def __str__(self):
		return str(self.email) + ' ' + str(self.date)

class Entry(models.Model):
	roll = models.CharField(max_length=50,null=True)
	name = models.CharField(max_length=50,null=True)
	date_time = models.DateTimeField(default=timezone.now) 

	def __str__(self):
		return str(self.roll)


class Lecture(models.Model):
	subject_name = models.CharField(max_length=30)
	faculty_name = models.CharField(max_length=30)
	batch = models.ForeignKey(Batch, on_delete=SET_NULL, null=True)
	start_time = models.TimeField()
	end_time = models.TimeField()

	class Meta:
		unique_together = ('batch','start_time','end_time')
	
	def clean(self):
		from django.core.exceptions import ValidationError

		found = False # var storing whether any subject is clashing

		for lecture in Lecture.objects.filter(batch=self.batch):
			if (self.start_time > lecture.start_time and self.start_time < lecture.end_time):
				print("1")
				found = True
				break
			if (self.end_time > lecture.start_time and self.end_time < lecture.end_time):
				print("2")
				found = True
				break
			if (self.start_time < lecture.start_time and self.end_time > lecture.end_time):
				print("3")
				found = True
				break
			
		print(found)
		if found:
			raise ValidationError("Overlapping Lectures")
			
		
	def __str__(self):
		return str(self.batch) + ' ' + str(self.subject_name)


class Visitor(models.Model):
	name = models.CharField(max_length=50,null=True)
	roll = models.CharField(max_length=50,null=True)
	contact = models.CharField(max_length=50,null=True)
	relation = models.CharField(max_length=50,null=True)
	reason = models.CharField(max_length=50,null=True)
	ed = models.DateTimeField(default=timezone.now) 
	leftd = models.DateTimeField(default=timezone.now) 
	ld =  models.CharField(max_length=50,null=True)
	left = models.BooleanField(default=False)
		
	def __str__(self):
		return str(self.roll) 