from django.contrib import admin
from .models import Role,Task,UserProfile

# Register your models here.

admin.site.site_header = 'Task App'
admin.site.register(Role)
admin.site.register(Task)
admin.site.register(UserProfile)

