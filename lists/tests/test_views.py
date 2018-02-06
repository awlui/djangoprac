from django.test import TestCase
from unittest import skip
from django.core.urlresolvers import resolve
from lists.views import home_page, view_list
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR, ExistingListItemForm
class ListViewTest(TestCase):
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/lists.html')
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
    def test_uses_list_template(self):
        list_ = List.objects.create()

        response = self.client.get('/lists/%d/' % (list_.id))

        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text')

    def test_displays_all_items_of_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        list2_ = List.objects.create()
        Item.objects.create(text='itemey 3', list=list2_)
        Item.objects.create(text='itemey 4', list=list2_)


        # request = HttpRequest()
        # response = view_list(request)
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'itemey 3')
        self.assertNotContains(response, 'itemey 4')
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id))
        self.assertEqual(response.context['list'], correct_list)
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id),
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/lists.html')
        expected_error = escape(EMPTY_LIST_ERROR)
        self.assertContains(response, expected_error)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

class ItemModeltest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        first_item = Item()
        first_item.list = list_
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.list = list_
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))
        expected_html = render_to_string('lists/home.html', {'form': ItemForm()})
        self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class NewListTest(TestCase):
    def test_home_page_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (list_.id))
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['item_text'] = 'A new list item'
        #
        # response = home_page(request)
        #
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


    def test_home_page_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={ 'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape(EMPTY_LIST_ERROR)
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': 'textey'}
        )
        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/lists.html')
        self.assertEqual(Item.objects.all().count(), 1)
