import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # ListView
    (r'^list/dict/$',                            views.DictList()),
    (r'^list/authors/$',                         views.AuthorList()),    
    (r'^list/authors/paginated/$',               views.AuthorList(paginate_by=30)),
    (r'^list/authors/paginated/(?P<page>\d+)/$', views.AuthorList(paginate_by=30)),
    (r'^list/authors/notempty/$',                views.AuthorList(allow_empty=False)),
    (r'^list/authors/template_object_name/$',    views.AuthorList(template_object_name='author')),
    (r'^list/authors/invalid/$',                 views.AuthorList(queryset=None)),
    
    # DetailView
    (r'^detail/obj/$',                            views.ObjectDetail()),
    (r'^detail/author/(?P<pk>\d+)/$',             views.AuthorDetail()),
    (r'^detail/author/byslug/(?P<slug>[\w-]+)/$', views.AuthorDetail()),
    (r'^detail/author/invalid/url/$',             views.AuthorDetail()),
    (r'^detail/author/invalid/qs/$',              views.AuthorDetail(queryset=None)),
    
    # ArchiveView
    (r'^dates/books/$',         views.BookArchive()),
    (r'^dates/books/invalid/$', views.BookArchive(queryset=None)),
    
    # YearView
    # Mixing keyword and possitional captures below is intentional; the views
    # ought to be able to accept either.
    (r'^dates/books/(?P<year>\d{4})/$',          views.BookYearArchive()),
    (r'^dates/books/(\d{4})/make_object_list/$', views.BookYearArchive(make_object_list=True)),
    (r'^dates/books/(\d{4})/allow_empty/$',      views.BookYearArchive(allow_empty=True)),
    (r'^dates/books/(\d{4})/allow_future/$',     views.BookYearArchive(allow_future=True)),
    (r'^dates/books/no_year/$',                  views.BookYearArchive()),

    # MonthView
    (r'^dates/books/(\d{4})/([a-z]{3})/$',              views.BookMonthArchive()),
    (r'^dates/books/(\d{4})/(\d{1,2})/$',               views.BookMonthArchive(month_format='%m')),
    (r'^dates/books/(\d{4})/([a-z]{3})/allow_empty/$',  views.BookMonthArchive(allow_empty=True)),
    (r'^dates/books/(\d{4})/([a-z]{3})/allow_future/$', views.BookMonthArchive(allow_future=True)),
    (r'^dates/books/(\d{4})/no_month/$',                views.BookMonthArchive()),
    
    # WeekView
    (r'^dates/books/(\d{4})/week/(\d{1,2})/$',              views.BookWeekArchive()),
    (r'^dates/books/(\d{4})/week/(\d{1,2})/allow_empty/$',  views.BookWeekArchive(allow_empty=True)),
    (r'^dates/books/(\d{4})/week/(\d{1,2})/allow_future/$', views.BookWeekArchive(allow_future=True)),
    (r'^dates/books/(\d{4})/week/no_week/$',                views.BookWeekArchive()),
    
    # DayView
    (r'^dates/books/(\d{4})/([a-z]{3})/(\d{1,2})/$',              views.BookDayArchive()),
    (r'^dates/books/(\d{4})/(\d{1,2})/(\d{1,2})/$',               views.BookDayArchive(month_format='%m')),
    (r'^dates/books/(\d{4})/([a-z]{3})/(\d{1,2})/allow_empty/$',  views.BookDayArchive(allow_empty=True)),
    (r'^dates/books/(\d{4})/([a-z]{3})/(\d{1,2})/allow_future/$', views.BookDayArchive(allow_future=True)),
    (r'^dates/books/(\d{4})/([a-z]{3})/no_day/$',                 views.BookDayArchive()),
    
    # TodayView
    (r'dates/books/today/$',              views.BookTodayArchive()),
    (r'dates/books/today/allow_empty/$',  views.BookTodayArchive(allow_empty=True)),
    
    # DateDetailView
    (r'^dates/books/(\d{4})/([a-z]{3})/(\d{1,2})/(\d+)/$',              views.BookDetail()),
    (r'^dates/books/(\d{4})/(\d{1,2})/(\d{1,2})/(\d+)/$',               views.BookDetail(month_format='%m')),
    (r'^dates/books/(\d{4})/([a-z]{3})/(\d{1,2})/(\d+)/allow_future/$', views.BookDetail(allow_future=True)),
    (r'^dates/books/(\d{4})/([a-z]{3})/(\d{1,2})/nopk/$',               views.BookDetail()),
    
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/byslug/(?P<slug>[\w-]+)/$', views.BookDetail()),
)