from django.db import models

# Create your models here.
class News(models.Model):
    title = models.TextField()
    url = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title