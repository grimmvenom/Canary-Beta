# -*- coding: utf-8 -*-
"""
Summary:
		This Module will make multiprocessed requests to determine a list of urls availability
		results are returned in json / dictionary format
author:
GrimmVenom <grimmvenom@gmail.com>

"""

import requests
import json
import urllib3
import multiprocessing
from http.client import responses
from lxml.html import fromstring
from app.core.base import Base
from app.modules.parse_results import Parse_Excel


class Status:
	def __init__(self, arguments):
		self.arguments = arguments
		self.urls = self.arguments.urls
		self.base = Base()
		self.status_results = dict()
		self.session = requests.session()
		self.logger = Base()
		if self.arguments.web_username and self.arguments.web_password:
			print("Setting Auth with username: " + str(self.arguments.web_username))
			self.session.auth = (self.arguments.web_username, self.arguments.web_password)
		multiprocessing.freeze_support()
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		
	def main(self):
		print("Checking URL Statuses")
		print("# of Urls Defined: " + str(len(self.urls)))
		self._worker()
		self._log()
		return self.status_results
	
	def _worker(self):
		unique_urls = list()
		malformed_urls = list()
		for url in self.urls:
			valid = self.base.detect_valid_url(url)
			if valid == True:
				if url not in unique_urls:
					unique_urls.append(url)
			else:
				malformed_urls.append(url)
		print("# of Unique Urls to request: " + str(len(unique_urls)))
		print("# of Malformed URLs: " + str(len(malformed_urls)))
		print(str(malformed_urls) + "\n")
		with multiprocessing.Pool(processes=10) as pool:  # Start Multiprocessing pool
			results = pool.map(self._verify, unique_urls)
		self.status_results = results
		print("\n")
	
	def _verify(self, url):
		response_data, session = self.base.session_get_response(self.session, url, False)
		return {url: response_data}

	def _log(self):
		if self.arguments.excel_output:
			parser = Parse_Excel(self.arguments)
			out_file = parser.status_to_excel(self.status_results, 'statusCheck')  # Write Excel Output
		else:
			out_file = self.logger.write_log(self.status_results, 'statusCheck')  # Write Log to json File
		if not self.arguments.no_open:
			self.logger.open_out_file(out_file)