from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Tom goes to check out a new online to-do app.
		self.browser.get('http://localhost:8000')

		# He sees the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		print(header_text)
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
		time.sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy socks', [row.text for row in rows])

		# Text box remains asking for another item. He enters
		# "Put socks on"
		# There is still a text box inviting her to add another item. He
    	# enters "Put socks on"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

    	# The page updates again, and now shows both items on her list
		
		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
		self.assertIn('2: Put socks on' ,[row.text for row in rows])

		# Tom wonders whether the site will remember her list. He sees
		# that the site has generated a unique URL for him -- there is some
    	# explanatory text to that effect.
		self.fail('Finish the test!')

    	# He visits that URL - her to-do list is still there.

		# Page updates again, with both items on list

		# The site generates a unique URL for her

		# He visits that URL - and list is there

if __name__ == '__main__':
	unittest.main(warnings='ignore')
