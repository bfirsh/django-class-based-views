from class_based_views.tests.models import Author
from django.test import TestCase

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

    def test_restricted_create_restricted(self):
        res = self.client.get('/edit/authors/create/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/list.html')

        res = self.client.post('/edit/authors/create/restricted/',
                        {'name': 'Randall Munroe', 'slug': 'randall-munroe'})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, 'http://testserver/accounts/login/?next=/edit/authors/create/restricted/')

    def test_update(self):
        Author.objects.create(**{'name': 'Randall Munroe', 'slug': 'randall-munroe'})
        res = self.client.get('/edit/author/1/update/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/detail.html')

        # Modification with both POST and PUT (browser compatible)
        res = self.client.post('/edit/author/1/update/',
                        {'name': 'Randall Munroe (xkcd)', 'slug': 'randall-munroe'})
        self.assertEqual(res.status_code, 302)
        self.assertEqual(str(Author.objects.all()), "[<Author: Randall Munroe (xkcd)>]")

    def test_delete(self):
        Author.objects.create(**{'name': 'Randall Munroe', 'slug': 'randall-munroe'})
        res = self.client.get('/edit/author/1/delete/')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'tests/detail.html')

        # Deletion with both POST and DELETE (browser compatible)
        res = self.client.post('/edit/author/1/delete/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(str(Author.objects.all()), '[]')
    
