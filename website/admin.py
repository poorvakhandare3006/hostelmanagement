from django.contrib import admin

# Register your models here.
from .models import Batch, Entry, Gatepass, Lecture, Timetable, UserProfile

# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Gatepass)
admin.site.register(Timetable)
admin.site.register(Entry)
admin.site.register(Batch)
admin.site.register(Lecture)