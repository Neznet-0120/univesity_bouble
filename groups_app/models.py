from django.db import models
from django.utils.translation import gettext_lazy as _


class StudentGroup(models.Model):
    COURSE_CHOICES = [(i, f"{i}-курс") for i in range(1, 7)]
    name = models.CharField(_("Названые группы"), max_length=20, unique=True)
    faculty = models.ForeignKey("core.Faculty", on_delete=models.CASCADE, related_name="groups",
                                verbose_name=_("Факультет"))
    course = models.PositiveSmallIntegerField(_("Курс"), choices=COURSE_CHOICES)
    students = models.ManyToManyField("core.User",
                                      related_name='users',
                                      limit_choices_to={"role": "student"},
                                      blank=True, verbose_name=_("Студенты"))
    
    class Meta:
        verbose_name = _("Студенческая группа")
        verbose_name_plural = _("Студенческие группы")
        ordering = ("faculty", "course", "name")
    
    def __str__(self):
        return self.name
    
    def students_count(self):
        return self.students.count()
    students_count.short_description = "Кол-во студентов"

    