django-class-based-views
========================

Work on [ticket #6735](http://code.djangoproject.com/ticket/6735).

Installation
------------

    $ python setup.py install


Usage
-----

Inherit your own class-based views from existing ones listed below.

Note: you must declare an **instance** of the class in your URLs, not the 
      class in order to avoid shared attributes across requests.

Views
-----

CRUD views
~~~~~~~~~~

* ListView: Render some list of objects, set by `self.queryset`. 
  This can be any iterable of items, not just a queryset.

* DetailView: Render a "detail" view of an object. By default this is a 
  model instance looked up from `self.queryset`, but the view will support 
  display of *any* object by overriding `self.get_object()`.

* CreateView: View for creating an object.

* UpdateView: View for updating an object.

* DeleteView: View for deleting an object retrieved with `self.get_object()`.


Extra views
~~~~~~~~~~~

* PaginatedListView
* ProcessFormView
* ProcessModelFormView
* DisplayFormView
* DisplayModelFormView


Date-based views
~~~~~~~~~~~~~~~~

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
