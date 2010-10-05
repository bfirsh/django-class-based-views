import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # base
    #(r'^about/login-required/$',
    #    views.DecoratedAboutView()),
    
    # DetailView
    (r'^detail/obj/$',
        views.ObjectDetail.as_view()),
    url(r'^detail/author/(?P<pk>\d+)/$',
        views.AuthorDetail.as_view(),
        name="author_detail"),
    (r'^detail/author/byslug/(?P<slug>[\w-]+)/$',
        views.AuthorDetail.as_view()),
    (r'^detail/author/invalid/url/$',
        views.AuthorDetail.as_view()),
    (r'^detail/author/invalid/qs/$',
        views.AuthorDetail.as_view(queryset=None)),

    # EditView
    (r'^edit/authors/create/$',
        views.AuthorCreate.as_view()),
    (r'^edit/authors/create/restricted/$',
        views.AuthorCreateRestricted.as_view()),
    (r'^edit/author/(?P<pk>\d+)/update/$',
        views.AuthorUpdate.as_view()),
    (r'^edit/author/(?P<pk>\d+)/delete/$',
        views.AuthorDelete.as_view()),
    
    # ArchiveView
    (r'^dates/books/$',
        views.BookArchive.as_view()),
    (r'^dates/books/invalid/$',
        views.BookArchive.as_view(queryset=None)),
    
    # ListView
    (r'^list/dict/$',
        views.DictList.as_view()),
    url(r'^list/authors/$',
        views.AuthorList.as_view(),
        name="authors_list"),
    (r'^list/authors/paginated/$', 
        views.PaginatedAuthorList.as_view(paginate_by=30)),
    (r'^list/authors/paginated/(?P<page>\d+)/$', 
        views.PaginatedAuthorList.as_view(paginate_by=30)),
    (r'^list/authors/notempty/$',
        views.AuthorList.as_view(allow_empty=False)),
    (r'^list/authors/template_object_name/$', 
        views.AuthorList.as_view(template_object_name='author')),
    (r'^list/authors/invalid/$',
        views.AuthorList.as_view(queryset=None)),
    
    # YearView
    # Mixing keyword and possitional captures below is intentional; the views
    # ought to be able to accept either.
    (r'^dates/books/(?P<year>\d{4})/$',
        views.BookYearArchive.as_view()),
    (r'^dates/books/(?P<year>\d{4})/make_object_list/$', 
        views.BookYearArchive.as_view(make_object_list=True)),
    (r'^dates/books/(?P<year>\d{4})/allow_empty/$',
        views.BookYearArchive.as_view(allow_empty=True)),
    (r'^dates/books/(?P<year>\d{4})/allow_future/$',
        views.BookYearArchive.as_view(allow_future=True)),
    (r'^dates/books/no_year/$',
        views.BookYearArchive.as_view()),

    # MonthView
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        views.BookMonthArchive.as_view()),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.BookMonthArchive.as_view(month_format='%m')),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/allow_empty/$',
        views.BookMonthArchive.as_view(allow_empty=True)),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/allow_future/$',
        views.BookMonthArchive.as_view(allow_future=True)),
    (r'^dates/books/(?P<year>\d{4})/no_month/$',
        views.BookMonthArchive.as_view()),

    # WeekView
    (r'^dates/books/(?P<year>\d{4})/week/(?P<week>\d{1,2})/$',
        views.BookWeekArchive.as_view()),
    (r'^dates/books/(?P<year>\d{4})/week/(?P<week>\d{1,2})/allow_empty/$',
        views.BookWeekArchive.as_view(allow_empty=True)),
    (r'^dates/books/(?P<year>\d{4})/week/(?P<week>\d{1,2})/allow_future/$',
        views.BookWeekArchive.as_view(allow_future=True)),
    (r'^dates/books/(?P<year>\d{4})/week/no_week/$',
        views.BookWeekArchive.as_view()),

    # DayView
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$',
        views.BookDayArchive.as_view()),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.BookDayArchive.as_view(month_format='%m')),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/allow_empty/$',
        views.BookDayArchive.as_view(allow_empty=True)),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/allow_future/$',
        views.BookDayArchive.as_view(allow_future=True)),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/no_day/$',
        views.BookDayArchive.as_view()),

    # TodayView
    (r'dates/books/today/$',
        views.BookTodayArchive.as_view()),
    (r'dates/books/today/allow_empty/$',
        views.BookTodayArchive.as_view(allow_empty=True)),

    # DateDetailView
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/(?P<pk>\d+)/$',
        views.BookDetail.as_view()),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)/$',
        views.BookDetail.as_view(month_format='%m')),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/(?P<pk>\d+)/allow_future/$',
        views.BookDetail.as_view(allow_future=True)),
    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/nopk/$',
        views.BookDetail.as_view()),

    (r'^dates/books/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/byslug/(?P<slug>[\w-]+)/$',
        views.BookDetail.as_view()),

    # Useful for testing redirects
    (r'^accounts/login/$',  'django.contrib.auth.views.login')
)