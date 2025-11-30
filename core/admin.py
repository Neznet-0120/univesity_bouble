from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Faculty, Department, Classroom
from groups_app.models import StudentGroup
from schedule.models import Lesson
from news.models import News


# Ограничение только для НЕ-суперадминов
class FacultyFilterAdmin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:          # ← стандартное поле Django
            return qs
        if request.user.role == "faculty_admin" and request.user.faculty:
            return qs.filter(group__faculty=request.user.faculty)
        return qs.none()


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin, FacultyFilterAdmin):
    list_display = ("name", "faculty", "head")
    list_filter = ("faculty",)
    search_fields = ("name",)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin, FacultyFilterAdmin):
    list_display = ("number", "faculty", "capacity")
    list_filter = ("faculty",)
    search_fields = ("number",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "faculty", "status", "is_active", "is_staff")
    list_filter = ("role", "faculty", "status", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")

    # ВАЖНО: НЕ наследуем FacultyFilterAdmin здесь — иначе суперадмин не увидит is_staff!
    # Оставляем стандартный BaseUserAdmin + вручную фильтруем только список
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == "faculty_admin" and request.user.faculty:
            return qs.filter(faculty=request.user.faculty)
        return qs.none()

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name", "email", "phone", "photo")}),
        ("Права и роли", {"fields": ("role", "faculty", "department", "status")}),
        ("Важные флаги", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "faculty", "status", "is_staff"),
        }),
    )




