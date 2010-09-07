from class_based_views.tests.models import Author
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

    def test_queryset(self):
        res = self.client.get('/list/authors/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')
        self.assertEqual(list(res.context['object_list']), list(Author.objects.all()))
        self.assertEqual(list(res.context['authors']), list(Author.objects.all()))

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

