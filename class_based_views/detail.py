import re
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from class_based_views import View

class DetailView(View):
    """
    Render a "detail" view of an object.

    By default this is a model instance lookedup from `self.queryset`, but the
    view will support display of *any* object by overriding `get_object()`.
    """

    def __init__(self, **kwargs):
        self._load_config_values(kwargs,
            queryset = None,
            slug_field = 'slug',
            template_object_name = None,
            template_name_field = None,
        )
        super(DetailView, self).__init__(**kwargs)

    def get_object(self, request, pk=None, slug=None, object_id=None, queryset=None):
        """
        Get the object this request wraps. By default this requires
        `self.queryset` and a `pk` or `slug` argument in the URLconf, but
        subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset(request)

        # Next, try looking up by primary key.
        if pk:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug:
            slug_field = self.get_slug_field(request)
            queryset = queryset.filter(**{slug_field: slug})

        # Finally, look for the (deprecated) object_id argument.
        elif object_id:
            import warnings
            warnings.warn(
                "The 'object_id' parameter to generic views is deprecated. "\
                "Use 'pk' instead.",
                PendingDeprecationWarning
            )
            queryset = queryset.filter(pk=object_id)

        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "\
                                 "either an object id or a slug." \
                                 % self.__class__.__name__)

        try:
            return queryset.get()
        except ObjectDoesNotExist:
            raise Http404("No %s found matching the query" % \
                          (queryset.model._meta.verbose_name))

    def get_queryset(self, request):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden.
        """
        if self.queryset is None:
            raise ImproperlyConfigured("%(cls)s is missing a queryset. Define "\
                                       "%(cls)s.queryset, or override "\
                                       "%(cls)s.get_object()." % {'cls': self.__class__.__name__})
        return self.queryset._clone()

    def get_slug_field(self, request):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field

    def get_template_names(self, request, obj):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        names = super(DetailView, self).get_template_names(request, obj)

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
            names.append("%s/%s_detail.html" % (obj._meta.app_label,
                                                obj._meta.object_name.lower()))

        return names

    def get_context(self, request, obj):
        """
        Get the context. Must return a Context (or subclass) instance.
        """
        context = super(DetailView, self).get_context(request, obj, {'object': obj})
        nicename = self.get_template_object_name(request, obj)
        if nicename:
            context[nicename] = obj
        return context

    def get_template_object_name(self, request, obj):
        """
        Get the name of the object to use in the context.
        """
        if self.template_object_name:
            return self.template_object_name
        elif hasattr(obj, '_meta'):
            return re.sub('[^a-zA-Z0-9]+', '_', obj._meta.verbose_name.lower())
        else:
            return None

