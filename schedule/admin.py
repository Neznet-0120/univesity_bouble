from django.contrib import admin
from .models import Lesson
from core.models import User
from core.admin import FacultyFilterAdmin  # если нужно ограничение по факультету

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin, FacultyFilterAdmin):
    list_display = ("subject", "teacher", "group", "classroom", "day", "time_start", "time_end")
    list_filter = ("group__faculty", "day", "week_type", "teacher")
    search_fields = ("subject", "teacher__last_name", "group__name")
    
    autocomplete_fields = ("teacher", "group", "classroom")  # всё чётко

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(role="teacher", status="approved")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)