import copy
from django import http
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

class View(object):
    """
    Parent class for all views.
    """
    
    def __init__(self, *args, **kwargs):
        # TODO: Check if request is in *args and raise warning
        
        self._load_config_values(kwargs,
            context_processors = None,
            mimetype = 'text/html',
            template_loader = None,
            template_name = None,
            decorators = [],
            allowed_methods = ['GET',],
            strict_allowed_methods = False,
            allowed_formats = ['html',],
            default_format = 'html',
            format_mimetypes = {
                'html': 'text/html'
            },
        )
        if kwargs:
            raise TypeError("__init__() got an unexpected keyword argument '%s'" % iter(kwargs).next())
    
    def __call__(self, request, *args, **kwargs):
        view = copy.copy(self)
        view.request = request
        callback = view.get_callback()
        if callback:
            return callback(*args, **kwargs)
        allowed_methods = [m for m in view.allowed_methods if hasattr(view, m)]
        return http.HttpResponseNotAllowed(allowed_methods)
    
    def get_callback(self):
        """
        Based on the request's HTTP method, get the callback on this class that 
        returns a response. If the method isn't allowed, None is returned.
        """
        method = self.request.method.upper()
        if method not in self.allowed_methods:
            if self.strict_allowed_methods:
                return None
            else:
                method = 'GET'
        callback = getattr(self, method, getattr(self, 'GET', None))
        if callback:
            if self.decorators is not None:
                for decorator in self.decorators:
                    callback = decorator(callback)
        return callback
    
    def GET(self, *args, **kwargs):
        content = self.get_content(*args, **kwargs)
        mimetype = self.get_mimetype()
        return self.get_response(content, mimetype=mimetype)
    
    def get_response(self, content, **httpresponse_kwargs):
        """
        Construct an `HttpResponse` object.
        """
        return http.HttpResponse(content, **httpresponse_kwargs)
    
    def get_content(self, *args, **kwargs):
        """
        Get the content to go in the response.
        """
        format = self.get_format()
        return getattr(self, 'render_%s' % format)(*args, **kwargs)
    
    def get_resource(self, *args, **kwargs):
        """
        Get a dictionary representing the resource for this view.
        """
        return {}
    
    def get_mimetype(self):
        """
        Get the mimetype to be used for the response.
        """
        return self.format_mimetypes[self.get_format()]
    
    def get_format(self):
        """
        Get the format for the content, defaulting to ``default_format``.
        
        The format is usually a short string to identify the format of the 
        content in the response. For example, 'html' or 'json'.
        """
        format = self.request.GET.get('format', self.default_format)
        if format not in self.allowed_formats:
            format = self.default_format
        return format
    
    def render_html(self, *args, **kwargs):
        """
        Render a template with a given resource
        """
        return self.get_template().render(self.get_context(*args, **kwargs))
    
    def get_template(self):
        """
        Get a ``Template`` object for the given request.
        """
        names = self.get_template_names()
        if not names:
            raise ImproperlyConfigured("'%s' must provide template_name." 
                % self.__class__.__name__)
        return self.load_template(names)
    
    def get_template_names(self):
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
    
    def load_template(self, names=[]):
        """
        Load a template, using self.template_loader or the default.
        """
        return self.get_template_loader().select_template(names)
    
    def get_template_loader(self):
        """
        Get the template loader to be used for this request. Defaults to
        ``django.template.loader``.
        """
        import django.template.loader
        return self.template_loader or django.template.loader
    
    def get_context(self, *args, **kwargs):
        """
        Get the template context. Must return a Context (or subclass) instance.
        """
        resource = self.get_resource(*args, **kwargs)
        context_processors = self.get_context_processors()
        return RequestContext(self.request, resource, context_processors)
    
    def get_context_processors(self):
        """
        Get the template context processors to be used.
        """
        return self.context_processors
    
    def _check_has_been_called(self):
        if self._has_been_called:
            raise ImproperlyConfigured("'%(class)s' has been instantiated in "
                "the URLconf. Class-based views should only be passed as "
                "classes. Try changing '%(class)s()' to '%(class)s'." % {
                    'class': self.__class__.__name__
                })
        self._has_been_called = True
    
    def _load_config_values(self, initkwargs, **defaults):
        """
        Set on self some config values possibly taken from __init__, or
        attributes on self.__class__, or some default.
        """
        for k in defaults:
            default = getattr(self.__class__, k, defaults[k])
            value = initkwargs.pop(k, default)
            setattr(self, k, value)
    
