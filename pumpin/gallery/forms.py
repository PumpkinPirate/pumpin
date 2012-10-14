from os.path import join
from cStringIO import StringIO

import Image

from django import forms
from django.conf import settings
from django.core.files.base import ContentFile

from pumpin.gallery.models import *

target_width = 620
target_height = 465

thumb_width = 120
thumb_height = 90

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
        
        image.save(instance.image.path, quality=90)
        
        return instance


class SubmitImageForm(forms.Form):
    overlay_choices = ((1, "img/overlay/ryan_01.png"),
                       (2, "img/overlay/ryan_02.png"),
                       (3, "img/overlay/ryan_03.png"),
                       (4, "img/overlay/ryan_04.png"),)
    overlay_dict = dict(overlay_choices)
    
    
    overlay = forms.ChoiceField(choices=overlay_choices, widget=forms.HiddenInput, initial=1)
    x = forms.IntegerField(widget=forms.HiddenInput)
    y = forms.IntegerField(widget=forms.HiddenInput)
    
    def save(self):
        instance = SubmittedImage()
        
        instance.is_public = self.uploaded_image.is_public
        
        image = Image.open(self.uploaded_image.image.path)
        overlay = Image.open(join(settings.STATIC_ROOT, self.overlay_dict[int(self.cleaned_data['overlay'])]))
        watermark = Image.open(join(settings.STATIC_ROOT, "img/overlay/watermark.png"))
        image.paste(overlay, (self.cleaned_data['x'], self.cleaned_data['y']), overlay)
        image.paste(watermark, (0,0), watermark)
        
        outfile = StringIO()
        image.save(outfile, "jpeg", quality=90)
        instance.image.save("submitted.jpg", ContentFile(outfile.getvalue()), save=False)
        
        image = image.resize([thumb_width, thumb_height], Image.ANTIALIAS)
        outfile = StringIO()
        image.save(outfile, "jpeg", quality=90)
        instance.thumbnail.save("submitted-th.jpg", ContentFile(outfile.getvalue()), save=True)
        
        return instance
