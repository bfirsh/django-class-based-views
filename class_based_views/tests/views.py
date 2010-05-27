from django.core.urlresolvers import reverse

from models import Author, Book
from forms import AuthorForm
import class_based_views

class DictList(class_based_views.ListView):
    """A ListView that doesn't use a model."""
    items = [
        {'first': 'John', 'last': 'Lennon'},
        {'last': 'Yoko',  'last': 'Ono'}
    ]
    template_name = 'tests/list.html'

class AuthorList(class_based_views.ListView):
    queryset = Author.objects.all()
    template_name = 'tests/list.html'

class AuthorDetail(class_based_views.DetailView):
    queryset = Author.objects.all()

class AuthorCreate(class_based_views.CreateView):
    queryset = Author.objects.all()
    template_name = 'tests/list.html'
    methods = ['GET', 'POST']

    def get_form(self, request, obj, *args, **kwargs):
        return AuthorForm(request.POST or None)

    def process_form(self, request, obj, data):
        Author.objects.create(**data)

    def redirect_to(self, request, obj):
        return reverse('authors_list')


class AuthorUpdate(class_based_views.UpdateView):
    queryset = Author.objects.all()

class ObjectDetail(class_based_views.DetailView):
    template_name = 'tests/detail.html'
    def get_object(self, request, **kwargs):
        return {'foo': 'bar'}

class BookConfig(object):
    queryset = Book.objects.all()
    date_field = 'pubdate'

class BookArchive(BookConfig, class_based_views.ArchiveView):
    pass

class BookYearArchive(BookConfig, class_based_views.YearView):
    pass

class BookMonthArchive(BookConfig, class_based_views.MonthView):
    pass

class BookWeekArchive(BookConfig, class_based_views.WeekView):
    pass

class BookDayArchive(BookConfig, class_based_views.DayView):
    pass

class BookTodayArchive(BookConfig, class_based_views.TodayView):
    pass

class BookDetail(BookConfig, class_based_views.DateDetailView):
    pass