from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.RETURN)
        WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "has-error")))
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")


        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'td'), 'Buy milk'))

        self.check_for_row_in_list_table('1: Buy milk')
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "has-error")))
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Make tea')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'tr:nth-child(2) td'), 'Make tea'))
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_item(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'td'), 'Buy wellies'))
        self.check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'has-error')))
        self.check_for_row_in_list_table('1: Buy wellies')

        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'has-error')))
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        self.get_item_input_box().send_keys('a')
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'has-error')))
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())

# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
