from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

class View(object):
    """
    Parent class for all views.
    """

    def __init__(self, **kwargs):
        self._load_config_values(kwargs,
            context_processors = None,
            mimetype = 'text/html',
            template_loader = None,
            template_name = None,
        )
        if kwargs:
            raise TypeError("__init__() got an unexpected keyword argument '%s'" % iter(kwargs).next())

    def __call__(self, request, *args, **kwargs):
        method = getattr(self, request.method.lower(), 'get')
        return method(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_object(request, *args, **kwargs)
        template = self.get_template(request, obj)
        context = self.get_context(request, obj)
        mimetype = self.get_mimetype(request, obj)
        response = self.get_response(request, obj, template, context, mimetype=mimetype)
        return response
    
    def get_object(self, request, *args, **kwargs):
        return None
    
    def get_template(self, request, obj):
        """
        Get a ``Template`` object for the given request.
        """
        names = self.get_template_names(request, obj)
        if not names:
            raise ImproperlyConfigured("'%s' must provide template_name." % self.__class__.__name__)
        return self.load_template(request, obj, names)
    
    def get_template_names(self, request, obj):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        if self.template_name is None:
            return []
        elif isinstance(self.template_name, basestring):
            return [self.template_name]
        else:
            return self.template_name
    
    def load_template(self, request, obj, names=[]):
        """
        Load a template, using self.template_loader or the default.
        """
        return self.get_template_loader(request, obj).select_template(names)
    
    def get_template_loader(self, request, obj):
        """
        Get the template loader to be used for this request. Defaults to
        ``django.template.loader``.
        """
        import django.template.loader
        return self.template_loader or django.template.loader
    
    def get_context(self, request, obj, context=None):
        """
        Get the context. Must return a Context (or subclass) instance.
        """
        processors = self.get_context_processors(request, obj)
        if context is None:
            context = {}
        return RequestContext(request, context, processors)
    
    def get_context_processors(self, request, obj):
        """
        Get the context processors to be used for the given request.
        """
        return self.context_processors
    
    def get_mimetype(self, request, obj):
        """
        Get the mimetype to be used for the given request.
        """
        return self.mimetype
    
    def get_response(self, request, obj, template, context, **httpresponse_kwargs):
        """
        Construct an `HttpResponse` object given the template and context.
        """
        return HttpResponse(template.render(context), **httpresponse_kwargs)
    
    def _load_config_values(self, initkwargs, **defaults):
        """
        Set on self some config values possibly taken from __init__, or
        attributes on self.__class__, or some default.
        """
        for k in defaults:
            default = getattr(self.__class__, k, defaults[k])
            value = initkwargs.pop(k, default)
            setattr(self, k, value)
    
