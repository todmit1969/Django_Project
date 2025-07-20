from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview_image = models.ImageField(upload_to='previews/')
    is_published = models.BooleanField(default=False)
    views_counter = models.PositiveIntegerField(default=0)
    notified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'

    def __str__(self):
        return self.title