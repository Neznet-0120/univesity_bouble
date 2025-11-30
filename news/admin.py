from django.contrib import admin
from .models import News
from core.admin import FacultyFilterAdmin



@admin.register(News)
class NewsAdmin(admin.ModelAdmin, FacultyFilterAdmin):
    list_display = ("title", "faculty", "created_at", "is_published")
    list_filter = ("faculty", "is_published", "created_at")
    search_fields = ("title",)