from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.RETURN)
        WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "has-error")))
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")


        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'td'), 'Buy milk'))

        self.check_for_row_in_list_table('1: Buy milk')
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "has-error")))
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Make tea')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'tr:nth-child(2) td'), 'Make tea'))
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
