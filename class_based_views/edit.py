from django.http import HttpResponseRedirect
from class_based_views import ListView
from class_based_views.base import TemplateView
from class_based_views.detail import SingleObjectMixin, DetailView

class FormMixin(object):
    """
    A mixin that provides a get_form() method.
    """
    
    initial = {}
    form = None
    
    def get_form(self):
        """
        Returns the form to be used in this view.
        """
        if self.request.method in ('POST', 'PUT'):
            return self.form(
                self.request.POST,
                self.request.FILES,
                initial=self.initial,
            )
        else:
            return self.form(
                initial=self.initial,
            )
    

class ModelFormMixin(SingleObjectMixin):
    """
    A derivative of SingleObjectMixin that passes get_object() as an instance 
    to a form.
    """
    
    initial = {}
    form = None
    
    def get_form(self):
        """
        Returns a form instantiated with the model instance from get_object().
        """
        if self.request.method in ('POST', 'PUT'):
            return self.form(
                self.request.POST,
                self.request.FILES,
                initial=self.initial,
                instance=self.get_object(*self.args, **self.kwargs),
            )
        else:
            return self.form(
                initial=self.initial,
                instance=self.get_object(*self.args, **self.kwargs),
            )
    

class ProcessFormView(TemplateView, FormMixin):
    """
    A view that processes a form on POST.
    """
    def POST(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    PUT = POST
    
    def form_valid(self, form):
        """
        Called when the submitted form is verified as valid.
        """
        raise NotImplementedError("You must override form_valid.")

    def form_invalid(self, form):
        """
        Called when the submitted form comes back with errors.
        """
        raise NotImplementedError("You must override form_invalid.")
    

class ProcessModelFormView(ModelFormMixin, ProcessFormView):
    """
    A view that saves a ModelForm on POST.
    """
    

class DisplayFormView(TemplateView, FormMixin):
    """
    Displays a form for the user to edit and submit on GET.
    """
    def GET(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(context=self.get_context(form))
    
    def get_context(self, form):
        return {
            'form': form,
        }
    

class DisplayModelFormView(ModelFormMixin, DisplayFormView):
    """
    Displays a ModelForm for the user to edit on GET.
    """
    

class ModelFormMixin(object):
    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(self.redirect_to(obj))
    
    def redirect_to(self, obj):
        raise NotImplementedError("You must override redirect_to.")
    
    def form_invalid(self, form):
        return self.GET(self.request, form)
    

class CreateView(ModelFormMixin, DisplayFormView, ProcessFormView):
    """
    View for creating an object.
    """
    

class UpdateView(ModelFormMixin, DisplayModelFormView, ProcessModelFormView):
    """
    View for updating an object.
    """
    

class DeleteView(DetailView):
    """
    View for deleting an object retrieved with `self.get_object()`.
    """    
    def DELETE(self, request, *args, **kwargs):
        obj = self.get_object(*args, **kwargs)
        obj.delete()
        return HttpResponseRedirect(self.redirect_to(obj))

    # Add support for browsers which only accept GET and POST for now.
    POST = DELETE

    def redirect_to(self, obj):
        raise NotImplementedError("You must override redirect_to.")
    
