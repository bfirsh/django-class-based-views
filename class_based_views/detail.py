from class_based_views import TemplateView
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
import re

class SingleObjectMixin(object):
    """
    Provides a get_object() method.
    """
    
    queryset = None
    slug_field = 'slug'
    
    def get_object(self, pk=None, slug=None, queryset=None):
        """
        Returns the object the view is displaying.
        
        By default this requires `self.queryset` and a `pk` or `slug` argument 
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either an object id or a slug."
                                 % self.__class__.__name__)

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(u"No %s found matching the query"
                          % (queryset.model._meta.verbose_name))
        return obj
    
    def get_queryset(self):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden.
        """
        if self.queryset is None:
            raise ImproperlyConfigured(u"%(cls)s is missing a queryset. Define "
                                       u"%(cls)s.queryset, or override "\
                                       u"%(cls)s.get_object()." % {
                                            'cls': self.__class__.__name__
                                        })
        return self.queryset._clone()

    def get_slug_field(self):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field
    

class DetailView(SingleObjectMixin, TemplateView):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """
    template_object_name = 'object'
    template_name_field = None
    
    def GET(self, request, *args, **kwargs):
        obj = self.get_object(*args, **kwargs)
        context = self.get_context(obj)
        return self.render_to_response(self.get_template_names(obj), context)
    
    def get_context(self, obj):
        return {
            'object': obj,
            self.get_template_object_name(obj): obj
        }
    
    def get_template_names(self, obj):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        names = super(DetailView, self).get_template_names()

        # If self.template_name_field is set, grab the value of the field
        # of that name from the object; this is the most specific template
        # name, if given.
        if self.template_name_field:
            name = getattr(obj, self.template_name_field, None)
            if name:
                names.insert(0, name)

        # The least-specific option is the default <app>/<model>_detail.html;
        # only use this if the object in question is a model.
        if hasattr(obj, '_meta'):
            names.append("%s/%s_detail.html" % (
                obj._meta.app_label,
                obj._meta.object_name.lower()
            ))

        return names

    def get_template_object_name(self, obj):
        """
        Get the name to use for the object.
        """
        if hasattr(obj, '_meta'):
            return re.sub('[^a-zA-Z0-9]+', '_', 
                    obj._meta.verbose_name.lower())
        else:
            return self.template_object_name
    
