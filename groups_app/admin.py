from django.contrib import admin
from .models import StudentGroup
from core.admin import FacultyFilterAdmin

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin, FacultyFilterAdmin):
    list_display = ("name", "faculty", "course", "students_count")
    list_filter = ("faculty", "course")
    search_fields = ("name",)

    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = "Кол-во студентов"