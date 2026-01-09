from django.contrib import admin
from .models import Task
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.site_header = 'Task App'

@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    list_display = ("id", "title", "status", "priority", "created_by")