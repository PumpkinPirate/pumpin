from os.path import join
from cStringIO import StringIO

import Image

from django import forms
from django.conf import settings
from django.core.files.base import ContentFile

from pumpin.gallery.models import *

target_width = 620
target_height = 465

class UploadImageForm(forms.ModelForm):
    def __init__(self, *a, **k):
        k['label_suffix'] = ""
        super(UploadImageForm, self).__init__(*a, **k)
        
    
    image = forms.ImageField(label="")
    agree = forms.BooleanField(required=True, label="I've got the rights to upload this image, and it's not porn.")
    is_public = forms.BooleanField(required=False, initial=True, label="Add to public gallery")
    
    class Meta:
        model = UploadedImage
        exclude = ['secret']
    
    def save(self):
        instance = super(UploadImageForm, self).save()
        
        image = Image.open(instance.image.path)
        
        ratio = max(float(target_width) / image.size[0], float(target_height) / image.size[1])
        width = int(round(image.size[0] * ratio))
        height = int(round(image.size[1] * ratio))
        if (ratio < 1):
            image = image.resize([width, height], Image.ANTIALIAS)
        else:
            image = image.resize([width, height], Image.BICUBIC)
            
        top = (height - target_height) / 2
        bottom = (height + target_height) / 2
        left = (width - target_width) / 2
        right = (width + target_width) / 2
        image = image.crop([left, top, right, bottom])
        
        image.save(instance.image.path)
        
        return instance


overlays = ((1, "img/overlay/ryan_01.png"),
            (2, "img/overlay/ryan_02.png"),)

overlay_dict = dict(overlays)

class SubmitImageForm(forms.Form):
    overlay = forms.ChoiceField(choices = overlays)
    x = forms.IntegerField()
    y = forms.IntegerField()
    
    def save(self):
        instance = SubmittedImage()
        
        instance.is_public = self.uploaded_image.is_public
        
        image = Image.open(self.uploaded_image.image.path)
        overlay = Image.open(join(settings.STATIC_ROOT, overlay_dict[int(self.cleaned_data['overlay'])]))
        image.paste(overlay, (self.cleaned_data['x'], self.cleaned_data['y']), overlay)
        
        outfile = StringIO()
        image.save(outfile, "jpeg")
        
        instance.image.save("submitted.jpg", ContentFile(outfile.getvalue()))
        return instance
        
