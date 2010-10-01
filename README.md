Django class-based views
========================

Work on [ticket #6735](http://code.djangoproject.com/ticket/6735).

Installation
------------

    $ python setup.py install

Or for the moment:

    $ pip install -e git@github.com:bfirsh/django-class-based-views.git#egg=django-cbv


Usage
-----

Inherit your own class-based views from existing ones listed below:

    class AuthorDetail(class_based_views.DetailView):
        queryset = Author.objects.all()


Declare your view in your URLs like you already do for classic views:

    import views
    from django.conf.urls.defaults import *
    
    urlpatterns = patterns('',
        url(r'^detail/author/(?P<pk>\d+)/$',
            views.AuthorDetail(),
            name="author_detail"),
    )

Note: you must declare an **instance** of the class in your URLs, not the 
class in order to avoid shared attributes across requests.


Views
-----

### CRUD views

* ListView: Render some list of objects, set by `self.queryset`. 
  This can be any iterable of items, not just a queryset.

* DetailView: Render a "detail" view of an object. By default this is a 
  model instance looked up from `self.queryset`, but the view will support 
  display of *any* object by overriding `self.get_object()`.

* CreateView: View for creating an object.

* UpdateView: View for updating an object.

* DeleteView: View for deleting an object retrieved with `self.get_object()`.

HTTP support: note that you can use POST or PUT HTTP verb for 
creating/editing an object and POST or DELETE for deleting an object.

### Extra views

* PaginatedListView
* ProcessFormView
* ProcessModelFormView
* DisplayFormView
* DisplayModelFormView


### Date-based views

* ArchiveView
* YearView
* MonthView
* WeekView
* DayView
* TodayView
* DateDetailView



API
---

TODO
