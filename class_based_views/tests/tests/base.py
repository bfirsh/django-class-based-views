from class_based_views.base import View, TemplateView
from class_based_views.tests.utils import RequestFactory
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import TestCase
from django.utils import simplejson
import unittest

class SimpleView(View):
    def GET(self, request):
        return HttpResponse('This is a simple view')
    

class SimplePostView(SimpleView):
    POST = SimpleView.GET
    

class AboutTemplateView(TemplateView):
    def GET(self, request):
        return self.render_to_response('tests/about.html', {})

class AboutTemplateAttributeView(TemplateView):
    template_name = 'tests/about.html'
    
    def GET(self, request):
        return self.render_to_response(context={})
    

class InstanceView(View):
    def GET(self, request):
        return self
    

class ViewTest(unittest.TestCase):
    rf = RequestFactory()
    
    def _assert_simple(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'This is a simple view')
    
    def test_get_only(self):
        """
        Test a view which only allows GET doesn't allow other methods.
        """
        self._assert_simple(SimpleView()(self.rf.get('/')))
        self.assertEqual(SimpleView()(self.rf.post('/')).status_code, 405)
        self.assertEqual(SimpleView()(
            self.rf.get('/', REQUEST_METHOD='FAKE')
        ).status_code, 405)
    
    def test_get_and_post(self):
        """
        Test a view which only allows both GET and POST.
        """
        self._assert_simple(SimplePostView()(self.rf.get('/')))
        self._assert_simple(SimplePostView()(self.rf.post('/')))
        self.assertEqual(SimplePostView()(
            self.rf.get('/', REQUEST_METHOD='FAKE')
        ).status_code, 405)
    
    def test_calling_more_than_once(self):
        """
        Test a view can only be called once.
        """
        request = self.rf.get('/')
        view = InstanceView()
        self.assertNotEqual(view(request), view(request))
    

class TemplateViewTest(unittest.TestCase):
    rf = RequestFactory()
    
    def _assert_about(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '<h1>About</h1>')
    
    def test_get(self):
        """
        Test a view that simply renders a template on GET
        """
        self._assert_about(AboutTemplateView()(self.rf.get('/about/')))
    
    def test_get_template_attribute(self):
        """
        Test a view that renders a template on GET with the template name as 
        an attribute on the class.
        """
        self._assert_about(AboutTemplateAttributeView()(self.rf.get('/about/')))
    
