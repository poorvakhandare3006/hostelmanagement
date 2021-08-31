from hostelmanagement.celery import app
# celery = Celery('tasks', broker='redis://localhost:6379')
import pytz
from django.utils import timezone
from django.core.mail import send_mail

from .models  import User,UserProfile,Batch,Lecture
@app.task
def send_mail_for_students():
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for user in UserProfile.objects.filter(out=True):
        mail = str(user.roll)+'@iiitg.com'
        print(mail)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        send_mail(
                'Campus Time Up',
            f'Hi, you need to return to campus before 11PM',
                'poorvakhandare3006@gmail.com',
                [mail],
                fail_silently=False,
            )  


@app.task
def send_mail_parents(email):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    mail = email
    print(mail)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    send_mail(
            'Campus Time Exceeded',
        f'Hi, you child has been returned campus late for 3 consecutive time today. We urge you to look into this matter. Thanks IIITGwalior',
            'poorvakhandare3006@gmail.com',
            [mail],
            fail_silently=False,
        )  


@app.task
def send_email_to_batch(batch_id,lecture_id):
    batch = Batch.objects.get(pk=batch_id)
    lecture = Lecture.objects.get(pk=lecture_id)
    for user in UserProfile.objects.filter(batch=batch):
        print(user)
        mail = str(user.roll)+'@iiitg.com'
        mail = "poorvakhandare1999@gmail.com"
        send_mail(
            f'{lecture.subject_name}',
           f'Hi, your {lecture.subject_name} is schedule from {lecture.start_time} to {lecture.end_time}.',
            'poorvakhandare3006@gmail.com',
            [mail],
            fail_silently=False,
        )

@app.task
def task_send_lecture_email():
    print("HI")

    time_now = timezone.localtime(timezone.now()) 
    time_after_fifteen_minute = time_now + timezone.timedelta(minutes=15)
    time_after_thirty_minute = time_now + timezone.timedelta(minutes=60)
    for batch in Batch.objects.all():
        for lecture in Lecture.objects.filter(batch=batch,start_time__gt=time_after_fifteen_minute,start_time__lte=time_after_thirty_minute):
            send_email_to_batch.delay(batch.id,lecture.id)
