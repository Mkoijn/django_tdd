from selenium import webdriver
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
		self.fail('Finish the test!')

		# He sees the page title and header mention to-do lists


		# He is asked to enter a to-do item straight away

		# He types "Buy socks" into a text box

		# When he hits enter, the page updates, and the page lists
		# 1: "Buy socks" as an item in to-do list

		# Text box remains asking for another item. He enters
		# "Put socks on"

		# Page updates again, with both items on list

		# The site generates a unique URL for her

		# He visits that URL - and list is there

if __name__ == '__main__':
	unittest.main(warnings='ignore')


