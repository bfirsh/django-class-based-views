from class_based_views.base import TemplateView
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.encoding import smart_str

class ListView(TemplateView):
    """
    Render some list of objects, set by `self.queryset`. This can be any 
    iterable of items, not just a queryset.
    """
    allow_empty = True
    template_object_name = None
    queryset = None
    
    def GET(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(queryset) == 0:
            raise Http404("Empty list and '%s.allow_empty' is False."
                          % self.__class__.__name__)
        context = self.get_context(queryset)
        return self.render_to_response(self.get_template_names(queryset), context)
    
    def get_context(self, queryset):
        """
        Get the context for this view.
        """
        context = {
            'object_list': queryset,
        }
        template_object_name = self.get_template_object_name(queryset)
        if template_object_name is not None:
            context[template_object_name] = queryset
        return context
    
    def get_queryset(self):
        """
        Get the list of items for this view. This must be an interable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if hasattr(self, 'queryset') and self.queryset is not None:
            queryset = self.queryset
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset'"
                                       % self.__class__.__name__)
        if hasattr(queryset, '_clone'):
            queryset = queryset._clone()
        return queryset
        
    def get_allow_empty(self):
        """
        Returns ``True`` if the view should display empty lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty
    
    def get_template_names(self, queryset, suffix='list'):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """ 
        names = super(ListView, self).get_template_names()
        
        # If the list is a queryset, we'll invent a template name based on the
        # app and model name. This name gets put at the end of the template 
        # name list so that user-supplied names override the automatically-
        # generated ones.
        if hasattr(queryset, 'model'):
            opts = queryset.model._meta
            names.append("%s/%s_%s.html" % (opts.app_label, opts.object_name.lower(), suffix))
        
        return names
    
    def get_template_object_name(self, queryset):
        """
        Get the name of the item to be used in the context.
        """
        if self.template_object_name:
            return '%s_list' % self.template_object_name
        elif hasattr(queryset, 'model'):
            return smart_str(queryset.model._meta.verbose_name_plural)
        else:
            return None
    

class PaginatedListView(ListView):
    paginate_by = None
    
    def get_context(self, queryset):
        page = self.kwargs.get('page', None)
        paginator, page, queryset = self.paginate_queryset(queryset, page)
        context = super(PaginatedListView, self).get_context(queryset)
        context.update({
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': paginator is not None,
        })
        return context
    
    def paginate_queryset(self, queryset, page):
        """
        Paginate the queryset, if needed.
        """
        paginate_by = self.get_paginate_by(queryset)
        paginator = Paginator(queryset, paginate_by, allow_empty_first_page=self.get_allow_empty())
        page = page or self.request.GET.get('page', 1)
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404("Page is not 'last', nor can it be converted to an int.")
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list)
        except InvalidPage:
            raise Http404('Invalid page (%s)' % page_number)
    
    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by
    
