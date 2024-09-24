from django.db import models

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=200)

    def __str__(self):
        return self.name
