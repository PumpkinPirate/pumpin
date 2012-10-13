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







class AjaxView(object):
    def form_valid(*args, **kwargs):
        html = super(AjaxView, self).form_valid(*args, **kwargs).content
        response = HttpResponse(mimetype="application/json")
        simplejson.dump({'success':True, 'html':html, image: self.instance.image.url()}, response)
        return response
    
    def form_invalid(*args, **kwargs):
        html = super(AjaxView, self).form_invalid(*args, **kwargs).content
        response = HttpResponse(mimetype="application/json")
        simplejson.dump({'success':False, 'html':html}, response)
        return response

    