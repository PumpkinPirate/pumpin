from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploaded/%Y-%m-%d/")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(verbose_name="Display this image in the public gallery")
