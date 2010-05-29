from class_based_views.base import View
from class_based_views.tests.utils import TestCase
from django.core.exceptions import ImproperlyConfigured

class AboutView(View):
    template_name = 'views/about.html'


class GetOnlyAboutView(AboutView):
    allowed_methods = ['GET']


class StrictGetOnlyAboutView(GetOnlyAboutView):
    strict_allowed_methods = True


class JsonView(View):
    allowed_formats.append('json')
    format_mimetypes['json'] = 'application/json'


class DefaultJsonView(JsonView):
    default_format = 'json'


class ViewTest(TestCase):
    def _assert_about(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '<h1>About</h1>')
    
    def test_simple_template_view(self):
        """
        Test a view that simply renders a template and allows both GET and POST
        """
        self._assert_about(AboutView()(self.rf.get('/about/')))
        self._assert_about(AboutView()(self.rf.post('/about/')))
    
    def test_calling_more_than_once(self):
        """
        Test a view can only be called once.
        """
        request = self.rf.get('/about/')
        view = AboutView()
        self.assertEqual(view(request).status_code, 200)
        self.assertRaises(ImproperlyConfigured, lambda: view(request))
    
    def test_get_only(self):
        """
        Test a view which only allows GET falls through to GET on other methods.
        """
        self._assert_about(GetOnlyAboutView()(self.rf.get('/about/')))
        self._assert_about(GetOnlyAboutView()(self.rf.post('/about/')))
        self._assert_about(GetOnlyAboutView()(
            self.rf.get('/about/', REQUEST_METHOD='FAKE')
        ))

    def test_strict_get_only(self):
        """
        Test a view which strictly only allows GET does not allow other methods.
        """
        self._assert_about(StrictGetOnlyAboutView()(self.rf.get('/about/')))
        response = StrictGetOnlyAboutView()(self.rf.post('/about/'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        response = StrictGetOnlyAboutView()(
            self.rf.get('/about/', REQUEST_METHOD='FAKE')
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
    
