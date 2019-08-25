# -*- coding: utf-8 -*-
"""
Summary:
		Script to scan urls for links, inpage links, verify links, and components
		that we have written test cases for. All output is to an XML file.
Update:
		canary being separated into modules to be used independently so canary can function
		as the eyes of Ivan and still perform it's tasks. All output will be in JSON and html

author:
GrimmVenom <grimmvenom@gmail.com>

Test using:
http://the-internet.herokuapp.com/
http://automationpractice.com/index.php
"""

import os
import platform
import sys
import json
import time
import multiprocessing
from subprocess import Popen
from app.core.base import Base
from app.core.get_arguments import get_arguments
from app.modules.status import Status
from app.modules.scraper import Scrape
from app.modules.verifier import Verify
from app.modules.parse_results import Parse_Excel
from app.modules.executor import Executor


class Canary:
	def __init__(self, arguments):
		# Global Variables
		self.arguments = arguments
		self.urls = arguments.urls
		self.status_log = dict()
		self.scrape_log = dict()
		self.verified_log = dict()
		self.logger = Base()
		self.main()

	def main(self):
		start_time = time.time()
		
		if self.arguments.exclude:
			print("Excluding: " + str(self.arguments.exclude) + "\n")

		if self.arguments.status:
			self._status()
			
		if self.arguments.scrape:  # Scrape Links, Images, Forms, etc from page
			self._scrape()
			if self.arguments.verify:  # Verify images, links scraped from page
				self._verify()
			if self.arguments.execute_tests:  # Execute found test cases from database
				
				executor = Executor(self.scrape_log, self.arguments)
				executor_results = executor.main()
				
		end_time = '{:.2f}'.format((time.time() - start_time))
		print("\nTotal Runtime: " + str(end_time) + " (seconds)\n")
	
	def _status(self):
		url_status = Status(self.arguments)  # Set Variables in status.py
		self.status_log = url_status.main()  # Request all unique urls and get a list of statuses
		if self.arguments.excel_output:
			parser = Parse_Excel(self.arguments)
			out_file = parser.status_to_excel(self.status_log, 'statusCheck') # Write Excel Output
		else:
			out_file = self.logger.write_log(self.status_log, 'statusCheck')  # Write Log to json File
		self.logger.open_out_file(out_file)
	
	def _scrape(self):
		scraper = Scrape(self.arguments)  # Set Variables in scraper.py
		self.scrape_log = scraper.main()  # Scrape content and return dictionary
		if not self.arguments.verify:
			if self.arguments.excel_output:
				parser = Parse_Excel(self.arguments)
				out_file = parser.scraper_to_excel(self.scrape_log, 'scrapedInfo')
			else:
				out_file = self.logger.write_log(self.scrape_log, 'scrapedInfo')  # Write Scraped Dictionary to json File
			self.logger.open_out_file(out_file)
	
	def _verify(self):
		verifier = Verify(self.scrape_log, self.arguments)  # Define Verifier
		self.verified_log = verifier.main()  # Run Verifier Method
		out_file = self.logger.write_log(self.verified_log, 'verifiedInfo')  # Write Log to json File
		if self.arguments.excel_output:  # Write Scraped / Verified Data to file
			parser = Parse_Excel(self.arguments)
			out_file = parser.scraper_to_excel(self.scrape_log, 'verifiedInfo')
		self.logger.open_out_file(out_file)


if __name__ == "__main__":
	print("Running Canary on ", str(platform.system()))
	current_dir = os.path.dirname(os.path.realpath(__file__))
	python_path = sys.executable
	# Change environment variable to allow multiprocessing
	if platform.system() == 'Darwin':
		try:
			if not 'OBJC_DISABLE_INITIALIZE_FORK_SAFETY' in os.environ:
				os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
		except Exception as e:
			print(e)
			print("If you experience errors when executing, Set the environment variable to allow multiprocessing:")
			print("to set in bash: 'export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES'")
			pass
		
	if not len(sys.argv) > 1:  # No Args Defined
		try:
			print(" ")
			if hasattr(sys, "_MEIPASS"):
				print("Attempting to Launch GUI: ", str(os.path.join(sys._MEIPASS, 'canary_gui.py')))
				try:
					os.listdir(sys._MEIPASS)
					# os.system(str(sys.executable) + " " + str(os.path.join(sys._MEIPASS, 'canary_gui.py')))
					print("Executable: ", str(sys.executable))
					os.system(str(sys.executable) + " " + "canary_gui.py")
				except Exception as e:
					print(e)
					pass
				
			else:
				print("Attempting to Launch GUI: ", 'canary_gui.py')
				os.system(str(sys.executable) + " " + "canary_gui.py")
			
		except Exception as e:
			print(e)
			pass
	# if platform == 'Windows':
	# subprocess.Popen(['start /b "', str(sys.executable), 'canary_gui.py'])
	# os.system('start /b "' + str(sys.executable) + ' canary_gui.py')
	# else:
	# subprocess.Popen([str(sys.executable), 'canary_gui.py'])
	# os.system(str(sys.executable) + ' canary_gui.py &>/dev/null &')
	
	# exit()
	else:
		multiprocessing.freeze_support()
		arguments = get_arguments()
		Canary(arguments)
