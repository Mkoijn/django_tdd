from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		# Tom goes to check out a new online to-do app.
		self.browser.get(self.live_server_url)

		# He sees the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text

		self.assertIn('To-Do', header_text)

		# He is asked to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item')

		# He types "Buy socks" into a text box
		inputbox.send_keys('Buy socks')


		# When he hits enter, the page updates, and the page lists
		# 1: "Buy socks" as an item in to-do list
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy socks')

		# Text box remains asking for another item. He enters
		# "Put socks on"
		# There is still a text box inviting her to add another item. He
    	# enters "Put socks on"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Put socks on')
		inputbox.send_keys(Keys.ENTER)

    	# The page updates again, and now shows both items on her list
		self.wait_for_row_in_list_table('2: Put socks on')
		self.wait_for_row_in_list_table('1: Buy socks')


	def test_multiple_users_can_start_at_different_urls(self):
		# Tom starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy socks')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy socks')

    	# He notices that his list has a unique URl.
		tom_list_url = self.browser.current_url
		self.assertRegex(tom_list_url, '/lists/.+')

		# Now Mary comes along.
		## We use a new browser session to make sure that no
		## information of Tom's is coming thru from cookies
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Mary visits home page. No sign of Tom's list.
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buys socks', page_text)
		self.assertNotIn('Put socks on', page_text)

		# Mary starts new list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Mary gets her own URL
		mary_list_url= self.browser.current_url
		self.assertRegex(mary_list_url, '/lists/.+')
		self.assertNotEqual(mary_list_url, tom_list_url)

		# Again no trace of Tom's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buys socks', page_text)
		self.assertIn('Buy milk', page_text)

		# They are both happy

	def test_layout_and_styling(self):
		# Tom goes to home_page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024,768)

		# He notices the input box is nicely created
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

		# She starts a new list and notices it's centered to-do
		# He notices the input box is nicely created
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)
