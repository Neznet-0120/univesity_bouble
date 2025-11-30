from django.db import models
from core.models import Faculty, Classroom
from groups_app.models import StudentGroup
from django.utils.translation import gettext_lazy as _

WEEKDAYS = [
    ("monday", "Понедельник"),
    ("tuesday", "Вторник"),
    ("wednesday", "Среда"),
    ("thursday", "Четверг"),
    ("friday", "Пятница"),
    ("saturday", "Суббота"),
    ("sanday", "Воскресенье"),
]

WEEK_TYPES = [
    ("numerator", "Числитель"),
    ("denomirator", "Знаменатель"),
    ("both", "Обе недели"),
    ]


class Lesson(models.Model):
    subject = models.CharField(_("Предмет"), max_length=200)
    teacher = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True,
                                limit_choices_to={"role": "teacher"},
                                related_name="lessons", verbose_name=_("Преподаватель"))
    group = models.ForeignKey("groups_app.StudentGroup", on_delete=models.CASCADE,
                              related_name="lessons", verbose_name=_("Студенческая группа"))
    classroom = models.ForeignKey("core.Classroom", on_delete=models.CASCADE,
                                  related_name="lessons", verbose_name=_("Аудитория"))
    day = models.CharField(_("День недели"), max_length=10, choices=WEEKDAYS)
    time_start = models.TimeField(_("Начало"))
    time_end = models.TimeField(_("Конец"))
    week_type = models.CharField(_("Тип недели"), max_length=12, choices=WEEK_TYPES, default="both")

    class Meta:
        verbose_name = _("Занятие")
        verbose_name_plural = _("Занятия")
        ordering = ("day", "time_start")

    def __str__(self):
        return f"{self.subject} - {self.group} ({self.get_day_display()})"
    
    