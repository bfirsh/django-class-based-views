from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

from class_based_views.tests.models import Author, Book
from class_based_views.tests.forms import AuthorForm
import class_based_views

class ObjectDetail(class_based_views.DetailView):
    template_name = 'tests/detail.html'
    
    def get_object(self):
        return {'foo': 'bar'}


class AuthorDetail(class_based_views.DetailView):
    queryset = Author.objects.all()


class DictList(class_based_views.ListView):
    """A ListView that doesn't use a model."""
    queryset = [
        {'first': 'John', 'last': 'Lennon'},
        {'last': 'Yoko',  'last': 'Ono'}
    ]
    template_name = 'tests/list.html'


class AuthorList(class_based_views.ListView):
    queryset = Author.objects.all()
    template_name = 'tests/list.html'


class PaginatedAuthorList(class_based_views.PaginatedListView):
    queryset = Author.objects.all()
    template_name = 'tests/list.html'


class AuthorCreate(class_based_views.CreateView):
    form = AuthorForm
    template_name = 'tests/list.html'
    
    def redirect_to(self, obj):
        return reverse('authors_list')


class AuthorCreateRestricted(AuthorCreate):
    POST = method_decorator(login_required)(AuthorCreate.POST)


class AuthorUpdate(class_based_views.UpdateView):
    queryset = Author.objects.all()
    form = AuthorForm
    template_name = 'tests/detail.html'

    def redirect_to(self, obj):
        return reverse('author_detail', args=[obj.id,])


class AuthorDelete(class_based_views.DeleteView):
    queryset = Author.objects.all()
    template_name = 'tests/detail.html'

    def redirect_to(self, obj):
        return reverse('authors_list')


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
