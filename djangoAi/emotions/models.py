from django.db import models

# Create your models here.
class ImageFromModel(models.Model):
    image = models.FileField(upload_to='uploads/')