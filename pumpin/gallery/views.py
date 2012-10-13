from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from pumpin.gallery.models import *
from pumpin.gallery.forms import *

class IndexView(CreateView):
    template_name = "index.html"
    model = UploadedImage
    form_class = UploadImageForm
    
    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        
        data['upload_form'] = UploadImageForm()
        
        return data

class EditImageView(FormView):
    form_class = SubmitImageForm
    template_name = "edit.html"
    
    def get_context_data(self, **kwargs):
        self.uploaded_image = get_object_or_404(UploadedImage, secret=self.kwargs['secret'])
        
        data = super(EditImageView, self).get_context_data(**kwargs)
        data['uploaded_image'] = self.uploaded_image
        return data
    
    def form_valid(self, form):
        self.uploaded_image = get_object_or_404(UploadedImage, secret=self.kwargs['secret'])
        
        form.uploaded_image = self.uploaded_image
        instance = form.save()
        
        self.success_url = instance.get_absolute_url()
        return super(EditImageView, self).form_valid(form)
        