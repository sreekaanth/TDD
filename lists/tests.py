from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item
from django.template.loader import render_to_string
from django.test import TestCase
# Create your tests here.

class HomePageTest(TestCase):   
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'home.html')

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
    
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')

        def test_home_page_redirects_after_POST(self):
            request=HttpRequest()
            request.method = 'POST'
            request.POST['item_text'] = 'A new list item'
            response = home_page(request)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['location'], '/')        
    
    def test_home_page_only_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(),0)
    
    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey1')
        Item.objects.create(text='itemey2')
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('itemey1',response.content.decode())
        self.assertIn('itemey2',response.content.decode())
        
class SmokeTest(TestCase):

    # def test_bad_maths(self):
    #     self.assertEqual(1 + 1,3)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
