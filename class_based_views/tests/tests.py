import datetime
from models import Author, Book
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

class ListViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_items(self):
        res = self.client.get('/list/dict/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')
        self.assertEqual(res.context['object_list'][0]['first'], 'John')
        self.assertEqual(res.context['paginator'], None)
        self.assertEqual(res.context['page_obj'], None)
        self.assertEqual(res.context['is_paginated'], False)

    def test_queryset(self):
        res = self.client.get('/list/authors/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')
        self.assertEqual(list(res.context['object_list']), list(Author.objects.all()))
        self.assertEqual(list(res.context['authors']), list(Author.objects.all()))
        self.assertEqual(res.context['paginator'], None)
        self.assertEqual(res.context['page_obj'], None)
        self.assertEqual(res.context['is_paginated'], False)

    def test_paginated_queryset(self):
        self._make_authors(100)
        res = self.client.get('/list/authors/paginated/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')
        self.assertEqual(len(res.context['authors']), 30)
        self.assertNotEqual(res.context['paginator'], None)
        self.assertNotEqual(res.context['page_obj'], None)
        self.assertEqual(res.context['is_paginated'], True)
        self.assertEqual(res.context['page_obj'].number, 1)
        self.assertEqual(res.context['paginator'].num_pages, 4)
        self.assertEqual(res.context['authors'][0].name, 'Author 00')
        self.assertEqual(list(res.context['authors'])[-1].name, 'Author 29')

    def test_paginated_get_page_by_query_string(self):
        self._make_authors(100)
        res = self.client.get('/list/authors/paginated/', {'page': '2'})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')
        self.assertEqual(len(res.context['authors']), 30)
        self.assertEqual(res.context['authors'][0].name, 'Author 30')
        self.assertEqual(res.context['page_obj'].number, 2)

    def test_paginated_get_last_page_by_query_string(self):
        self._make_authors(100)
        res = self.client.get('/list/authors/paginated/', {'page': 'last'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context['authors']), 10)
        self.assertEqual(res.context['authors'][0].name, 'Author 90')
        self.assertEqual(res.context['page_obj'].number, 4)

    def test_paginated_get_page_by_urlvar(self):
        self._make_authors(100)
        res = self.client.get('/list/authors/paginated/3/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')
        self.assertEqual(len(res.context['authors']), 30)
        self.assertEqual(res.context['authors'][0].name, 'Author 60')
        self.assertEqual(res.context['page_obj'].number, 3)

    def test_paginated_page_out_of_range(self):
        self._make_authors(100)
        res = self.client.get('/list/authors/paginated/42/')
        self.assertEqual(res.status_code, 404)

    def test_paginated_invalid_page(self):
        self._make_authors(100)
        res = self.client.get('/list/authors/paginated/?page=frog')
        self.assertEqual(res.status_code, 404)

    def test_allow_empty_false(self):
        res = self.client.get('/list/authors/notempty/')
        self.assertEqual(res.status_code, 200)
        Author.objects.all().delete()
        res = self.client.get('/list/authors/notempty/')
        self.assertEqual(res.status_code, 404)

    def test_template_object_name(self):
        res = self.client.get('/list/authors/template_object_name/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['object_list']), list(Author.objects.all()))
        self.assertEqual(list(res.context['author_list']), list(Author.objects.all()))
        self.assert_('authors' not in res.context)

    def test_missing_items(self):
        self.assertRaises(ImproperlyConfigured, self.client.get, '/list/authors/invalid/')

    def _make_authors(self, n):
        Author.objects.all().delete()
        for i in range(n):
            Author.objects.create(name='Author %02i' % i, slug='a%s' % i)

class DetailViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_simple_object(self):
        res = self.client.get('/detail/obj/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['object'], {'foo': 'bar'})
        self.assertTemplateUsed(res, 'tests/detail.html')

    def test_detail_by_pk(self):
        res = self.client.get('/detail/author/1/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['object'], Author.objects.get(pk=1))
        self.assertEqual(res.context['author'], Author.objects.get(pk=1))
        self.assertTemplateUsed(res, 'tests/author_detail.html')

    def test_detail_by_slug(self):
        res = self.client.get('/detail/author/byslug/scott-rosenberg/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['object'], Author.objects.get(slug='scott-rosenberg'))
        self.assertEqual(res.context['author'], Author.objects.get(slug='scott-rosenberg'))
        self.assertTemplateUsed(res, 'tests/author_detail.html')

    def test_invalid_url(self):
        self.assertRaises(AttributeError, self.client.get, '/detail/author/invalid/url/')

    def test_invalid_queryset(self):
        self.assertRaises(ImproperlyConfigured, self.client.get, '/detail/author/invalid/qs/')

class EditViewTests(TestCase):
    urls = 'class_based_views.tests.urls'

    def test_create(self):
        res = self.client.get('/edit/authors/create/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')

        res = self.client.post('/edit/authors/create/',
                        {'name': 'Randall Munroe', 'slug': 'randall-munroe'})
        self.assertEqual(res.status_code, 302)
        self.assertEqual(str(Author.objects.all()), "[<Author: Randall Munroe>]")

    def test_update(self):
        Author.objects.create(**{'name': 'Randall Munroe', 'slug': 'randall-munroe'})
        res = self.client.get('/edit/author/1/update/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/detail.html')

        res = self.client.post('/edit/author/1/update/',
                        {'name': 'Randall Munroe (xkcd)', 'slug': 'randall-munroe'})
        self.assertEqual(res.status_code, 302)
        self.assertEqual(str(Author.objects.all()), "[<Author: Randall Munroe (xkcd)>]")

        res = self.client.put('/edit/author/1/update/',
                        {'name': 'Randall Munroe (xkcd)', 'slug': 'randall-munroe-xkcd'})
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Author.objects.get(id=1).slug, 'randall-munroe-xkcd')


class ArchiveViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_archive_view(self):
        res = self.client.get('/dates/books/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['date_list'], Book.objects.dates('pubdate', 'year')[::-1])
        self.assertEqual(list(res.context['latest']), list(Book.objects.all()))
        self.assertTemplateUsed(res, 'tests/book_archive.html')

    def test_archive_view_invalid(self):
        self.assertRaises(ImproperlyConfigured, self.client.get, '/dates/books/invalid/')

class YearViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_year_view(self):
        res = self.client.get('/dates/books/2008/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['date_list']), [datetime.datetime(2008, 10, 1)])
        self.assertEqual(res.context['year'], 2008)
        self.assertTemplateUsed(res, 'tests/book_archive_year.html')

    def test_year_view_make_object_list(self):
        res = self.client.get('/dates/books/2006/make_object_list/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['date_list']), [datetime.datetime(2006, 5, 1)])
        self.assertEqual(list(res.context['books']), list(Book.objects.filter(pubdate__year=2006)))
        self.assertEqual(list(res.context['object_list']), list(Book.objects.filter(pubdate__year=2006)))
        self.assertTemplateUsed(res, 'tests/book_archive_year.html')

    def test_year_view_empty(self):
        res = self.client.get('/dates/books/1999/')
        self.assertEqual(res.status_code, 404)
        res = self.client.get('/dates/books/1999/allow_empty/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['date_list']), [])
        self.assertEqual(list(res.context['books']), [])

    def test_year_view_allow_future(self):
        # Create a new book in the future
        year = datetime.date.today().year + 1
        b = Book.objects.create(name="The New New Testement", pages=600, pubdate=datetime.date(year, 1, 1))
        res = self.client.get('/dates/books/%s/' % year)
        self.assertEqual(res.status_code, 404)

        res = self.client.get('/dates/books/%s/allow_empty/' % year)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['books']), [])

        res = self.client.get('/dates/books/%s/allow_future/' % year)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['date_list']), [datetime.datetime(year, 1, 1)])

    def test_year_view_invalid_pattern(self):
        self.assertRaises(TypeError, self.client.get, '/dates/books/no_year/')

class MonthViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_month_view(self):
        res = self.client.get('/dates/books/2008/oct/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/book_archive_month.html')
        self.assertEqual(list(res.context['date_list']), [datetime.datetime(2008, 10, 1)])
        self.assertEqual(list(res.context['books']),
                         list(Book.objects.filter(pubdate=datetime.date(2008, 10, 1))))
        self.assertEqual(res.context['month'], datetime.date(2008, 10, 1))

        # Since allow_empty=False, next/prev months must be valid (#7164)
        self.assertEqual(res.context['next_month'], None)
        self.assertEqual(res.context['previous_month'], datetime.date(2006, 5, 1))

    def test_month_view_allow_empty(self):
        # allow_empty = False, empty month
        res = self.client.get('/dates/books/2000/jan/')
        self.assertEqual(res.status_code, 404)

        # allow_empty = True, empty month
        res = self.client.get('/dates/books/2000/jan/allow_empty/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['date_list']), [])
        self.assertEqual(list(res.context['books']), [])
        self.assertEqual(res.context['month'], datetime.date(2000, 1, 1))

        # Since it's allow empty, next/prev are allowed to be empty months (#7164)
        self.assertEqual(res.context['next_month'], datetime.date(2000, 2, 1))
        self.assertEqual(res.context['previous_month'], datetime.date(1999, 12, 1))

        # allow_empty but not allow_future: next_month should be empty (#7164)
        url = datetime.date.today().strftime('/dates/books/%Y/%b/allow_empty/').lower()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['next_month'], None)

    def test_month_view_allow_future(self):
        future = (datetime.date.today() + datetime.timedelta(days=60)).replace(day=1)
        urlbit = future.strftime('%Y/%b').lower()
        b = Book.objects.create(name="The New New Testement", pages=600, pubdate=future)

        # allow_future = False, future month
        res = self.client.get('/dates/books/%s/' % urlbit)
        self.assertEqual(res.status_code, 404)

        # allow_future = True, valid future month
        res = self.client.get('/dates/books/%s/allow_future/' % urlbit)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['date_list'][0].date(), b.pubdate)
        self.assertEqual(list(res.context['books']), [b])
        self.assertEqual(res.context['month'], future)

        # Since it's allow_future but not allow_empty, next/prev are not
        # allowed to be empty months (#7164)
        self.assertEqual(res.context['next_month'], None)
        self.assertEqual(res.context['previous_month'], datetime.date(2008, 10, 1))

        # allow_future, but not allow_empty, with a current month. So next
        # should be in the future (yup, #7164, again)
        res = self.client.get('/dates/books/2008/oct/allow_future/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['next_month'], future)
        self.assertEqual(res.context['previous_month'], datetime.date(2006, 5, 1))

    def test_custom_month_format(self):
        res = self.client.get('/dates/books/2008/10/')
        self.assertEqual(res.status_code, 200)

    def test_month_view_invalid_pattern(self):
        self.assertRaises(TypeError, self.client.get, '/dates/books/2007/no_month/')

class WeekViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_week_view(self):
        res = self.client.get('/dates/books/2008/week/39/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/book_archive_year.html')
        self.assertEqual(res.context['books'][0], Book.objects.get(pubdate=datetime.date(2008, 10, 1)))
        self.assertEqual(res.context['week'], datetime.date(2008, 9, 28))

    def test_week_view_allow_empty(self):
        res = self.client.get('/dates/books/2008/week/12/')
        self.assertEqual(res.status_code, 404)

        res = self.client.get('/dates/books/2008/week/12/allow_empty/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['books']), [])

    def test_week_view_allow_future(self):
        future = datetime.date(datetime.date.today().year + 1, 1, 1)
        b = Book.objects.create(name="The New New Testement", pages=600, pubdate=future)

        res = self.client.get('/dates/books/%s/week/0/' % future.year)
        self.assertEqual(res.status_code, 404)

        res = self.client.get('/dates/books/%s/week/0/allow_future/' % future.year)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['books']), [b])

    def test_week_view_invalid_pattern(self):
        self.assertRaises(TypeError, self.client.get, '/dates/books/2007/week/no_week/')

class DayViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_day_view(self):
        res = self.client.get('/dates/books/2008/oct/01/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/book_archive_day.html')
        self.assertEqual(list(res.context['books']),
                         list(Book.objects.filter(pubdate=datetime.date(2008, 10, 1))))
        self.assertEqual(res.context['day'], datetime.date(2008, 10, 1))

        # Since allow_empty=False, next/prev days must be valid.
        self.assertEqual(res.context['next_day'], None)
        self.assertEqual(res.context['previous_day'], datetime.date(2006, 5, 1))

    def test_day_view_allow_empty(self):
        # allow_empty = False, empty month
        res = self.client.get('/dates/books/2000/jan/1/')
        self.assertEqual(res.status_code, 404)

        # allow_empty = True, empty month
        res = self.client.get('/dates/books/2000/jan/1/allow_empty/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['books']), [])
        self.assertEqual(res.context['day'], datetime.date(2000, 1, 1))

        # Since it's allow empty, next/prev are allowed to be empty months (#7164)
        self.assertEqual(res.context['next_day'], datetime.date(2000, 1, 2))
        self.assertEqual(res.context['previous_day'], datetime.date(1999, 12, 31))

        # allow_empty but not allow_future: next_month should be empty (#7164)
        url = datetime.date.today().strftime('/dates/books/%Y/%b/%d/allow_empty/').lower()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['next_day'], None)

    def test_day_view_allow_future(self):
        future = (datetime.date.today() + datetime.timedelta(days=60))
        urlbit = future.strftime('%Y/%b/%d').lower()
        b = Book.objects.create(name="The New New Testement", pages=600, pubdate=future)

        # allow_future = False, future month
        res = self.client.get('/dates/books/%s/' % urlbit)
        self.assertEqual(res.status_code, 404)

        # allow_future = True, valid future month
        res = self.client.get('/dates/books/%s/allow_future/' % urlbit)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['books']), [b])
        self.assertEqual(res.context['day'], future)

        # allow_future but not allow_empty, next/prev amust be valid
        self.assertEqual(res.context['next_day'], None)
        self.assertEqual(res.context['previous_day'], datetime.date(2008, 10, 1))

        # allow_future, but not allow_empty, with a current month.
        res = self.client.get('/dates/books/2008/oct/01/allow_future/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['next_day'], future)
        self.assertEqual(res.context['previous_day'], datetime.date(2006, 5, 1))

    def test_next_prev_context(self):
        res = self.client.get('/dates/books/2008/oct/01/')
        self.assertEqual(res.content, "Archive for 2008-10-01. Previous day is 2006-05-01")

    def test_custom_month_format(self):
        res = self.client.get('/dates/books/2008/10/01/')
        self.assertEqual(res.status_code, 200)

    def test_day_view_invalid_pattern(self):
        self.assertRaises(TypeError, self.client.get, '/dates/books/2007/oct/no_day/')

    def test_today_view(self):
        res = self.client.get('/dates/books/today/')
        self.assertEqual(res.status_code, 404)
        res = self.client.get('/dates/books/today/allow_empty/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['day'], datetime.date.today())

class DateDetailViewTests(TestCase):
    fixtures = ['generic-views-test-data.json']
    urls = 'class_based_views.tests.urls'

    def test_date_detail_by_pk(self):
        res = self.client.get('/dates/books/2008/oct/01/1/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['object'], Book.objects.get(pk=1))
        self.assertEqual(res.context['book'], Book.objects.get(pk=1))
        self.assertTemplateUsed(res, 'tests/book_detail.html')

    def test_date_detail_by_slug(self):
        res = self.client.get('/dates/books/2006/may/01/byslug/dreaming-in-code/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['book'], Book.objects.get(slug='dreaming-in-code'))

    def test_date_detail_custom_month_format(self):
        res = self.client.get('/dates/books/2008/10/01/1/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['book'], Book.objects.get(pk=1))

    def test_date_detail_allow_future(self):
        future = (datetime.date.today() + datetime.timedelta(days=60))
        urlbit = future.strftime('%Y/%b/%d').lower()
        b = Book.objects.create(name="The New New Testement", slug="new-new", pages=600, pubdate=future)

        res = self.client.get('/dates/books/%s/new-new/' % urlbit)
        self.assertEqual(res.status_code, 404)

        res = self.client.get('/dates/books/%s/%s/allow_future/' % (urlbit, b.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['book'], b)
        self.assertTemplateUsed(res, 'tests/book_detail.html')

    def test_invalid_url(self):
        self.assertRaises(AttributeError, self.client.get, "/dates/books/2008/oct/01/nopk/")
