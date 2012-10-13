from django import forms

from pumpin.gallery.models import *

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

class SubmitImageForm(forms.Form):
    uploaded_image = forms.CharField