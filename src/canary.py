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
from app.modules.executor import Executor


class Canary:
	def __init__(self, arguments):
		# Global Variables
		self.arguments = arguments
		self.urls = arguments.urls
		self.status_log = dict()
		self.scrape_log = dict()
		self.verified_log = dict()
		self.mapping = {'status': {'function': "Status(self.arguments).main()", 'var': "self.status_log"},
			'scrape': {'function': "Scrape(self.arguments).main()", 'var': "self.scrape_log"},
			'verify': {'function': "Verify(self.scrape_log, self.arguments).main()", 'var': "self.verified_log"}}
		self.logger = Base()
		self.main()

	def main(self):
		start_time = time.time()
		type_loop = self.arguments.type.copy()
		if 'verify' in type_loop:
			type_loop.remove('verify')

		if self.arguments.exclude:
			print("Excluding: " + str(self.arguments.exclude) + "\n")

		for type in type_loop:
			type = str(type)
			var = str(self.mapping[type]['var'])
			function = str(self.mapping[type]["function"])
			# print(var)
			# print(function)
			setattr(self, var, exec(function))

		end_time = '{:.2f}'.format((time.time() - start_time))
		print("\nTotal Runtime: " + str(end_time) + " (seconds)\n")


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
