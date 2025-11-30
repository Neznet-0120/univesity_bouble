from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from groups_app.models import StudentGroup

# ============= РОЛИ =============
ROLE_CHOICES = (
    ("student", "Студент"),
    ("teacher", "Преподаватель"),
    ("faculty_admin", "Админ факультета"),
    ("super_admin", "Суперадмин (ректорат)"),
)

STATUS_CHOICES = (
    ("pending", "Ожидает одобрения"),
    ("approved", "Одобрен"),
    ("rejected", "Отклонён"),
)


class Faculty(models.Model):
    name = models.CharField(_("Название факультета"), max_length=200, unique=True)
    slug = models.SlugField(_("Слаг"), unique=True, max_length=100)
    description = models.TextField(_("Описание"), blank=True)
    created_at = models.DateTimeField(_("Создан"), auto_now_add=True)

    class Meta:
        verbose_name = _("Факультет")
        verbose_name_plural = _("Факультеты")

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(_("Название кафедры"), max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")
    head = models.OneToOneField('User', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="headed_department", verbose_name=_("Зав. кафедрой"))
    description = models.TextField(_("Описание"), blank=True)

    class Meta:
        verbose_name = _("Кафедра")
        verbose_name_plural = _("Кафедры")
        unique_together = ("name", "faculty")

    def __str__(self):
        return f"{self.name} ({self.faculty})"


class Classroom(models.Model):
    number = models.CharField(_("Номер аудитории"), max_length=20)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="classrooms")
    capacity = models.PositiveSmallIntegerField(_("Вместимость"), default=30)

    class Meta:
        verbose_name = _("Аудитория")
        verbose_name_plural = _("Аудитории")

    def __str__(self):
        return f"{self.number} — {self.faculty}"


class User(AbstractUser):
    role = models.CharField(_("Роль"), max_length=20, choices=ROLE_CHOICES, default="student")
    faculty = models.ForeignKey(Faculty, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="users", verbose_name=_("Факультет"))
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="members", verbose_name=_("Кафедра"))
    status = models.CharField(_("Статус"), max_length=20, choices=STATUS_CHOICES, default="pending")
    phone = models.CharField(_("Телефон"), max_length=20, blank=True)
    photo = models.ImageField(_("Фото"), upload_to="profiles/", blank=True, null=True)
    group = models.ForeignKey(
        "groups_app.StudentGroup", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="main_users", verbose_name="Учебная группа"
    )

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    # Удобные свойства
    @property
    def is_faculty_admin(self):
        return self.role == "faculty_admin"

    @property
    def is_super_admin(self):
        return self.role == "super_admin"