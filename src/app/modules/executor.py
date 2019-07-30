# -*- coding: utf-8 -*-
"""
Summary:
		This Module will take json input, get component and page tests scraped from page, and execute the specified commands
author:
GrimmVenom <grimmvenom@gmail.com>

"""

import os
import sys
import re
import time
import json
import platform
import multiprocessing, urllib3, subprocess
from app.core.base import Base


class Executor:
	def __init__(self, json, arguments):
		self.input_log = json
		self.arguments = arguments
		self.component_tests = dict()
		self.page_tests = dict()
		self.results = dict()
		manager = multiprocessing.Manager()
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	
	def main(self):
		print("Preparing to Execute Test Cases")
		self.logger = Base()
		self.extract_component_tests()
		self.extract_page_tests()
		
		if len(self.component_tests) >= 1:
			component_list = list()
			self.results['component_tests'] = dict()
			for index, data in self.component_tests.items():
				component_list.append([index, data])
			with multiprocessing.Pool(processes=3) as pool:  # Start Multiprocessing pool
				results = pool.map(self.execute_test, component_list)
			for result in results:
				index = result[0]
				result_data = result[1]
				self.results['component_tests'][index] = result_data
				
		if len(self.page_tests) >= 1:
			page_test_list = list()
			self.results['page_tests'] = dict()
			for index, data in self.page_tests.items():
				page_test_list.append([index, data])
			with multiprocessing.Pool(processes=3) as pool:  # Start Multiprocessing pool
				results = pool.map(self.execute_test, page_test_list)
			for result in results:
				index = result[0]
				result_data = result[1]
				self.results['page_tests'][index] = result_data
				
		print("\n\n", self.results)
		out_file = self.logger.write_log(self.results, 'ExecutionResults')  # Write Log to json File
		self.logger.open_out_file(out_file)

	def extract_component_tests(self):
		counter = 0
		for url, data in self.input_log.items():
			if 'components' in data:
				for index, component_data in data['components'].items():
					counter += 1
					self.component_tests[counter] = component_data
		print('Total components Tests found', str(len(self.component_tests)))
	
	def extract_page_tests(self):
		counter = 0
		for url, data in self.input_log.items():
			if 'page_tests' in data:
				for index, pageTest_data in data['page_tests'].items():
					counter += 1
					self.page_tests[counter] = pageTest_data
		print('Total Page Tests found', str(len(self.page_tests)))
	
	def execute_test(self, test: dict):
		# print(test, "\n")
		index = test[0]
		data = test[1]
		command = data['execute_command']
		# print(command, "\n")
		if command != "None" and command != None:
			try:
				result = subprocess.check_output(command, shell=True)
				result = result.decode('utf-8')
				# result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT) # Also Capture STDOUT
			except Exception as e:
				result = str(e)
				pass
		else:
			result = "No Command Defined"
		data['result'] = str(result)
		new_data = [index, data]
		return new_data
