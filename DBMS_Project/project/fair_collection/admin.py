from django.contrib import admin
from .models import Package,Enrollment,Interest,UserProfile,ResultHistory
# Register your models here.
admin.site.register(Package)
admin.site.register(Enrollment)
admin.site.register(Interest)
admin.site.register(UserProfile)
admin.site.register(ResultHistory)