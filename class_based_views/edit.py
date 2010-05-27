from class_based_views import DetailView

class FormView(DetailView):
    def post(self, request, obj, *args, **kwargs):
        form = self.get_form(request, obj, *args, **kwargs)
        if form.is_valid():
            self.process_form(request, obj, form.cleaned_data)
            return HttpResponseRedirect(self.redirect_to(request, obj))
        template = self.get_template(request, obj)
        context = self.get_context(request, obj)
        mimetype = self.get_mimetype(request, obj)
        response = self.get_response(request, obj, template, context, mimetype=mimetype)
        return response

    def get_form(self, request, obj, *args, **kwargs):
        raise NotImplementedError

    def process_form(self, request, obj, data):
        raise NotImplementedError

    def redirect_to(self, request, obj):
        raise NotImplementedError


class CreateView(FormView):
    pass


class UpdateView(FormView):
    def put(self, request, obj, *args, **kwargs):
        obj = self.get_object(request, *args, **kwargs)
        return self.post(request, obj, *args, **kwargs)


class DeleteView(DetailView):
    def delete(self, request, obj, *args, **kwargs):
        obj = self.get_object(request, *args, **kwargs)
        obj.delete()
        return HttpResponseRedirect(self.redirect_to(request, obj))

    def post(self, request, obj, *args, **kwargs):
        return self.delete(request, obj, *args, **kwargs)

    def redirect_to(self, request, obj):
        raise NotImplementedError

