from class_based_views.tests.models import Author
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

class DetailViewTest(TestCase):
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
        #self.assertEqual(res.context['object'], Author.objects.get(pk=1))
        self.assertEqual(res.context['author'], Author.objects.get(pk=1))
        self.assertTemplateUsed(res, 'tests/author_detail.html')

    def test_detail_by_slug(self):
        res = self.client.get('/detail/author/byslug/scott-rosenberg/')
        self.assertEqual(res.status_code, 200)
        #self.assertEqual(res.context['object'], Author.objects.get(slug='scott-rosenberg'))
        self.assertEqual(res.context['author'], Author.objects.get(slug='scott-rosenberg'))
        self.assertTemplateUsed(res, 'tests/author_detail.html')

    def test_invalid_url(self):
        self.assertRaises(AttributeError, self.client.get, '/detail/author/invalid/url/')

    def test_invalid_queryset(self):
        self.assertRaises(ImproperlyConfigured, self.client.get, '/detail/author/invalid/qs/')
