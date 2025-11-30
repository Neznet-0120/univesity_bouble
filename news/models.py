from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField(_("Заголовок"), max_length=200)
    content = models.TextField(_("Текст новости"))
    faculty = models.ForeignKey("core.Faculty", on_delete=models.CASCADE, related_name="news",
                                verbose_name=_("Факультет"), null=True, blank=True)
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)
    is_published = models.BooleanField(_("Опубликовано"), default=True)
    image = models.ImageField(_("Изображение"), upload_to="news/", blank=True, null=True)

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ("-created_at", )

    def __str__(self):
        return self.title
    