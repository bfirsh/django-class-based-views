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
    

class HashView(View):
    def GET(self, request):
        return unicode(hash(self))
    

class JsonView(View):
    template_name = 'tests/apple_detail.html'
    
    def __init__(self, *args, **kwargs):
        super(JsonView, self).__init__(*args, **kwargs)
        self.allowed_formats.append('json')
        self.format_mimetypes['json'] = 'application/json'
    
    def render_json(self, request, *args, **kwargs):
        return simplejson.dumps(self.get_resource(request, *args, **kwargs))
    
    def get_resource(self, request, color='red', **kwargs):
        return {'apple': {
            'color': color,
        }}
    

class ContextArgsJsonView(JsonView):
    def get_context(self, request, extra='', **kwargs):
        context = super(ContextArgsJsonView, self).get_context(request)
        context['extra'] = extra
        return context
    

class DefaultJsonView(JsonView):
    default_format = 'json'


class ContextJsonView(JsonView):
    def get_context(self, request, *args, **kwargs):
        context = super(ContextJsonView, self).get_context(request, *args, **kwargs)
        context['tasty'] = True
        return context
    
    
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
        view = HashView()
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
    
    def test_get(self):
        """
        Test a view that renders a template on GET with the template name as 
        an attribute on the class.
        """
        self._assert_about(AboutTemplateAttributeView()(self.rf.get('/about/')))
    
# Broken
class ResourceViewTest(unittest.TestCase):
    rf = RequestFactory()
    
    def _assert_html_apple(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'text/html')
        self.assertEqual(response.content, 'This is a red apple')
    
    def _assert_json_apple(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'application/json')
        self.assertEqual(
            simplejson.loads(response.content)['apple']['color'],
            'red'
        )
    
    def test_json_default_html(self):
        """
        Test a view with different formats returns HTML by default.
        """
        self._assert_html_apple(JsonView()(self.rf.get('/apple/')))
    
    def test_json_view(self):
        """
        Test a view returns the correct format when explicitly set.
        """
        self._assert_json_apple(JsonView()(self.rf.get('/apple/?format=json')))
    
    def test_default_json_view(self):
        """
        Test a view that returns JSON by default.
        """
        self._assert_json_apple(DefaultJsonView()(self.rf.get('/apple/')))
    
    def test_default_json_view_html(self):
        """
        Test a view that returns JSON by default returns HTML if explicitly
        set.
        """
        self._assert_html_apple(DefaultJsonView()(
            self.rf.get('/apple/?format=html')
        ))
    
    def _assert_tasty(self, view):
        response = view(self.rf.get('/apple/'))
        self.assertEqual(response.content, 'This is a tasty red apple')
        response = view(self.rf.get('/apple/?format=json'))
        self.assertTrue(
            'tasty' not in simplejson.loads(response.content)['apple']
        )
    
    def test_context_only_passed_to_template(self):
        """
        Test any extra context defined with ``get_context`` is only passed to 
        templates.
        """
        self._assert_tasty(ContextJsonView())
    
    def test_context_processors(self):
        """
        Test any context processors defined are used to render the template.
        """
        self._assert_tasty(ContextProcessorJsonView())
    
    def test_resource_arguments(self):
        """
        Test any arguments from the URL are passed through to the resource.
        """
        response = JsonView()(self.rf.get('/apple/blue/'), color='blue')
        self.assertEqual(response.content, 'This is a blue apple')
    
    def test_context_arguments(self):
        """
        Test any arguments from the URL are passed through to the context.
        """
        response = ContextArgsJsonView()(
            self.rf.get('/apple/'),
            extra='. That is good'
        )
        self.assertEqual(
            response.content,
            'This is a red apple. That is good'
        )

# Broken
class DecoratorViewTest(TestCase):
    urls = 'class_based_views.tests.urls'
    
    def test_decorators(self):
        """
        Test any decorators applied with the ``decorators`` attribute are 
        applied.
        """
        res = self.client.get('/about/login-required/')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, 'http://testserver/accounts/login/?next=/about/login-required/')
    
