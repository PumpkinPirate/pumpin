from django import forms

from pumpin.gallery.models import *

class UploadImageForm(forms.ModelForm):
    def __init__(self, *a, **k):
        k['label_suffix'] = ""
        super(UploadImageForm, self).__init__(*a, **k)
        
    
    image = forms.ImageField(label="")
    agree = forms.BooleanField(required=True, label="I have the rights to this image; it's not porn")
    is_public = forms.BooleanField(required=False, label="Display this image in the public gallery")
    
    class Meta:
        model = UploadedImage