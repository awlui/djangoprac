import time
import sys
from unittest import skip
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn(row_text, [row.text for row in rows])

class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # self.fail('Finish the test!')

        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.server_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        print(inputbox.location['x'], inputbox.size['width'])
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5
        )
class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        time.sleep(10)
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')

        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')