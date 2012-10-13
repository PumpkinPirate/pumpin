from time import strftime
import random

from django.db import models
from django.core.urlresolvers import reverse

def uploaded_image_path(instance, filename):
    extension = filename.split(".")[-1]
    return "uploaded/%s/%s.%s" % (strftime("%Y-%m-%d"), instance.secret, extension)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to=uploaded_image_path)
    secret = models.CharField(max_length=32, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(verbose_name="Display this image in the public gallery")
    
    def save(self, *args, **kwargs):
        if not self.secret:
            chars = "0123456789abcdefghijklmnopABCDEFGHIJKLMNOP-_"
            self.secret = "".join(random.choice(chars) for i in xrange(32))
        
        super(UploadedImage, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("edit", kwargs={'secret': self.secret})
    
mod_choices = ((0, "unmoderated"),
               (1, "flagged"),
               (2, "approved"),
               (3, "rejected"))

class SubmittedImage(models.Model):
    image = models.ImageField(upload_to=uploaded_image_path)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(verbose_name="Display this image in the public gallery")
    mod_status = models.IntegerField(choices=mod_choices, default=0)
