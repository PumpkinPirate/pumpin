# Create your views here.

from django.views.generic import TemplateView

from pumpin.gallery.models import *
from pumpin.gallery.forms import *

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        
        data['upload_form'] = UploadImageForm()
        
        return data