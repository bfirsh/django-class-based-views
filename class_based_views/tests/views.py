from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

from class_based_views.tests.models import Author, Book
from class_based_views.tests.forms import AuthorForm
import class_based_views

class ObjectDetail(class_based_views.DetailView):
    template_name = 'tests/detail.html'
    
    def get_object(self, request, **kwargs):
        return {'foo': 'bar'}


class AuthorDetail(class_based_views.DetailView):
    queryset = Author.objects.all()


class DecoratedAboutView(class_based_views.View):
    template_name = 'tests/about.html'
    decorators = [login_required,]



# class DictList(class_based_views.ListView):
#     """A ListView that doesn't use a model."""
#     items = [
#         {'first': 'John', 'last': 'Lennon'},
#         {'last': 'Yoko',  'last': 'Ono'}
#     ]
#     template_name = 'tests/list.html'
# 
# class AuthorList(class_based_views.ListView):
#     queryset = Author.objects.all()
#     template_name = 'tests/list.html'



# class AuthorCreate(class_based_views.CreateView):
#     queryset = Author.objects.all()
#     template_name = 'tests/list.html'
#     methods = ['GET', 'POST']
# 
#     def get_form(self, request, obj, *args, **kwargs):
#         return AuthorForm(request.POST or None)
# 
#     def process_form(self, request, obj, data):
#         Author.objects.create(**data)
# 
#     def redirect_to(self, request, obj):
#         return reverse('authors_list')
# 
# 
# class AuthorCreateRestricted(AuthorCreate):
#     post = method_decorator(login_required)(AuthorCreate.post)
# 
# 
# class AuthorUpdate(class_based_views.UpdateView):
#     queryset = Author.objects.all()
#     template_name = 'tests/detail.html'
#     methods = ['GET', 'POST', 'PUT']
# 
#     def get_form(self, request, obj, *args, **kwargs):
#         return AuthorForm(request.REQUEST or None)
# 
#     def process_form(self, request, obj, data):
#         for k, v in data.iteritems():
#             setattr(obj, k, v)
#         obj.save()
# 
#     def redirect_to(self, request, obj):
#         return reverse('author_detail', args=[obj.id,])
# 
# 
# class AuthorDelete(class_based_views.DeleteView):
#     queryset = Author.objects.all()
#     template_name = 'tests/detail.html'
#     methods = ['GET', 'POST', 'DELETE']
# 
#     def redirect_to(self, request, obj):
#         return reverse('authors_list')

# class BookConfig(object):
#     queryset = Book.objects.all()
#     date_field = 'pubdate'
# 
# class BookArchive(BookConfig, class_based_views.ArchiveView):
#     pass
# 
# class BookYearArchive(BookConfig, class_based_views.YearView):
#     pass
# 
# class BookMonthArchive(BookConfig, class_based_views.MonthView):
#     pass
# 
# class BookWeekArchive(BookConfig, class_based_views.WeekView):
#     pass
# 
# class BookDayArchive(BookConfig, class_based_views.DayView):
#     pass
# 
# class BookTodayArchive(BookConfig, class_based_views.TodayView):
#     pass
# 
# class BookDetail(BookConfig, class_based_views.DateDetailView):
#     pass