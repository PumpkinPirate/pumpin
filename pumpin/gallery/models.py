from time import strftime
import random

from django.db import models
from django.core.urlresolvers import reverse

def gen_secret(instance):
    if not instance.secret:
        chars = "0123456789abcdefghijklmnopABCDEFGHIJKLMNOP-_"
        instance.secret = "".join(random.choice(chars) for i in xrange(8))

def uploaded_image_path(instance, filename):
    extension = filename.split(".")[-1]
    gen_secret(instance)
    return "uploaded/%s/%s.%s" % (strftime("%Y-%m-%d"), instance.secret, extension)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to=uploaded_image_path)
    secret = models.CharField(max_length=8, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(verbose_name="Display this image in the public gallery")
    
    def save(self, *args, **kwargs):
        gen_secret(self)
        super(UploadedImage, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("edit", kwargs={'secret': self.secret})
    
mod_choices = ((0, "unmoderated"),
               (1, "flagged"),
               (2, "approved"),
               (3, "rejected"))

def submitted_image_path(instance, filename):
    gen_secret(instance)
    return "submitted/%s/%s.jpg" % (strftime("%Y-%m-%d"), instance.secret)

def submitted_thumb_path(instance, filename):
    gen_secret(instance)
    return "submitted/%s/%s_th.jpg" % (strftime("%Y-%m-%d"), instance.secret)

class SubmittedImage(models.Model):
    image = models.ImageField(upload_to=submitted_image_path)
    thumbnail = models.ImageField(upload_to=submitted_thumb_path)
    timestamp = models.DateTimeField(auto_now_add=True)
    secret = models.CharField(max_length=8, unique=True)
    is_public = models.BooleanField(verbose_name="Display this image in the public gallery")
    mod_status = models.IntegerField(choices=mod_choices, default=0)
    view_count = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        gen_secret(self)
        super(SubmittedImage, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('image_detail', kwargs={'secret': self.secret})
    
    @classmethod
    def public_objects(cls):
        return cls.objects.filter(is_public=True, mod_status__in=[0,2])