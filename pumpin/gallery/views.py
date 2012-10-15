from django.views.generic import TemplateView, DetailView, View, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from pumpin.gallery.models import *
from pumpin.gallery.forms import *

page_size = 100

class IndexView(CreateView):
    template_name = "index.html"
    model = UploadedImage
    form_class = UploadImageForm
    
    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        
        data['upload_form'] = UploadImageForm()
        data['latest'] = SubmittedImage.public_objects().order_by("-timestamp")[:page_size]
        data['popular'] = SubmittedImage.public_objects().order_by("-view_count")[:page_size]
        data['feature_image'] = data['popular'][0]
        
        return data

class LatestPageView(TemplateView):
    template_name = "image_list.html"
    
    def get_context_data(self, **kwargs):
        page = int(self.kwargs['page'])
        data = super(LatestPageView, self).get_context_data(**kwargs)
        
        data['object_list'] = SubmittedImage.public_objects().order_by("-timestamp")[page_size*page:page_size*(page+1)]
        
        return data

class PopularPageView(TemplateView):
    template_name = "image_list.html"
    
    def get_context_data(self, **kwargs):
        page = int(self.kwargs['page'])
        data = super(PopularPageView, self).get_context_data(**kwargs)
        
        data['object_list'] = SubmittedImage.public_objects().order_by("-view_count")[page_size*page:page_size*(page+1)]
        
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

class SumbittedImageView(IndexView):
    template_name = "image_detail.html"
    
    def get_context_data(self, **kwargs):
        data = super(SumbittedImageView, self).get_context_data(**kwargs)
        
        obj = get_object_or_404(SubmittedImage, secret=self.kwargs['secret'])
        obj.view_count += 1
        obj.save()
        
        data['feature_image'] = obj
        
        return data

class ReportImageView(SingleObjectMixin, View):
    model = SubmittedImage
    slug_field = 'secret'
    slug_url_kwarg = 'secret'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.mod_status == 0:
            self.object.mod_status = 1
            self.object.save()
            return HttpResponse("1", mimetype="application/json")
        
        return HttpResponse("0", mimetype="application/json")
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ModerateView(ListView):
    queryset = SubmittedImage.objects.filter(mod_status=1)
    template_name="moderate.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ModerateView, self).dispatch(*args, **kwargs)



class SetImageStatusView(SingleObjectMixin, View):
    model = SubmittedImage
    slug_field = 'secret'
    slug_url_kwarg = 'secret'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SetImageStatusView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        self.object.mod_status = int(self.request.POST['new_status'])
        self.object.save()
        
        return HttpResponseRedirect(reverse("moderate"))