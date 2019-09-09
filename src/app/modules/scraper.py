# -*- coding: utf-8 -*-
"""
Summary:
		This Module Scrapes images, links, forms and the specified attributes for each element type
		results are returned in json / dictionary format
		
		Also supports beautifulsoup element lookup, xpath lookup, and url comparison based on db input
		
author:
GrimmVenom <grimmvenom@gmail.com>

"""

import re
import urllib3
import multiprocessing
import requests
from bs4 import BeautifulSoup
from enum import Enum
from lxml import etree
# Imports Change if __main__
from app.core.base import Base
from app.modules.verifier import Verify
from app.modules.db_query import Components_DB
from app.modules.parse_results import Parse_Excel


class ScrapeRequirements(Enum):
	IMAGES = ["img"], ["src", "name", "class", "id", "value", 'title', 'alt', 'role', 'data-srcset']
	LINKS = ["a"], ["href",  "name", "class", "id", "type", "alt", "title", 'role']
	FORMS = ["input", 'textarea', 'select', 'button'], ["name", "class", "id", "type", "value", 'role']
	IFRAMES = ["iframe"], ["src"]


class Scrape:
	def __init__(self, arguments):
		self.arguments = arguments
		self.urls = self.arguments.urls
		self.base = Base()
		self.scrape_results = dict()
		self.sorted_results = dict()
		self.scraped_total = 0
		self.session = requests.session()
		self.available_components = dict()
		self.available_page_tests = dict()
		self.logger = Base()
		if self.arguments.web_username and self.arguments.web_password:
			print("Setting Auth with username: " + str(self.arguments.web_username))
			self.session.auth = (self.arguments.web_username, self.arguments.web_password)
		manager = multiprocessing.Manager()
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		
	def main(self):
		if self.arguments.database:
			Query = Components_DB(self.arguments)
			self.available_components = Query.list_components()
			self.available_page_tests = Query.list_page_tests()
			print("\n\n")
			# print(self.components)
			
		self._worker(self.urls)
		self._sort_dict()
		print("total scraped results: " + str(self.scraped_total) + "\n")
		self._log()
		return self.sorted_results

	def _worker(self, urls):
		element_results = dict()
		with multiprocessing.Pool(processes=10) as pool:  # Start Multiprocessing pool
			results = pool.map(self._scrape, urls)
			# queue = dict(pair for d in results for pair in d.items())  # convert the returned list to dictionary
		# print(str(results))
		for result in results:
			for item in result:
				self.scraped_total += 1
				keys = item.keys()
				try:
					if 'url' in keys:
						if item['url'] not in element_results:  # IF url as key not exist, create it
							element_results[item['url']] = {}
					if 'elementType' in keys:
						if str(item['elementType']) not in element_results[item['url']]:  # If Element Type not exist, create it
							element_results[item['url']][item['elementType']] = {}
					if 'index' in keys:
						if str(item['index']) not in element_results[item['url']][item['elementType']]:
							element_results[item['url']][item['elementType']][item['index']] = {}
							
					for key in keys:
						if key not in ['url', 'elementType', 'index']:
							try:
								if isinstance(item[key], dict):
									for k in item[key].keys():
										element_results[item['url']][item['elementType']][item['index']][k] = item[key][k]
								else:
									element_results[item['url']][item['elementType']][item['index']][str(key)] = item[key]
							except Exception as e:
								print(e)
								pass
				except Exception as e:
					print(e)
					print(item)
					pass
			self.scrape_results = element_results  # Set Class Log to element_results dictionary
	
	def _scrape(self, url):
		response, self.session, page_source = self.base.session_get_response(self.session, url, True, False)
		
		# print("URL: " + str(url))
		results = self._scrape_enum_elements(url, response, page_source)
		
		if self.arguments.database:
			component_results = self._scrape_components(url, response, page_source)
			for result in component_results:
				results.append(result)
				
			page_test_results = self._scrape_page_tests(url)
			for result in page_test_results:
				results.append(result)
		print("\n\n")
		return results
	
	def _scrape_enum_elements(self, url, response, page_source):
		print("Scraping Enum Elements from: " + str(url))
		results = list()
		manual = ('javascript:void(0);', 'java', '#', 'data:')
		soup = BeautifulSoup(page_source, 'html.parser')
		for index, type in enumerate(ScrapeRequirements):
			element_type = str(type).split(".", 1)[1].lower()
			# print("Checking " + str(element_type) + " on: " + str(url))
			element_tags = ScrapeRequirements[element_type.upper()].value[0]
			attributes = ScrapeRequirements[element_type.upper()].value[1]
			
			elements = list()
			for tag in element_tags:
					temp = soup.find_all(tag)
					for t in temp:
						elements.append({'tag': str(tag), 'value': t})
			
			# print(str(element_tags) + " tags found: " + str(len(elements)))
			# print(elements)
			for x, y in enumerate(elements):
				tag = elements[x]['tag']
				element = elements[x]['value']
				element_log = dict()
				for attribute in attributes:
					try:
						# print("scraping " + str(attribute))
						temp = element[attribute]
						if isinstance(temp, list):
							temp = temp[0]
						if attribute in ['href', 'src']:
							if not temp.startswith(manual):
								if temp.startswith("https://") or temp.startswith("http://"):
									element_log['target_url'] = temp
								elif temp.startswith("//"):
									element_log['target_url'] = self.base.get_protocol(url) + temp
								elif temp.startswith("/") or not any([temp.startswith(s) for s in ['http://', 'https://', "//"]]):
									element_log['target_url'] = str(self.base.get_site_root(url)) + temp
								else:
									pass
								if element_log['target_url']:
									valid_url = self.base.detect_valid_url(element_log['target_url'])
									element_log['valid_url'] = valid_url
						element_log[str(attribute)] = str(temp)
					except:
						pass
				element_log['scraped_from'] = str(url)
				result = {'url': str(url),
						'elementType': str(element_type),
						'index': str(x),
						'htmlTag': str(tag),
						'data': element_log}
				if elements[x]['value'].content:
					content = str(element.content).replace("\\t", "").replace("\\r", "").replace("\\n", ",").strip()  # Remove encoded characters
					new_content = str(re.sub("\s{3,}", ",", content))  # Replace 3+ spaces with a comma
					try:
						string = self.base.unicode_to_ascii(new_content)
						result['data']['content'] = string
					except Exception as e:
						result['data']['content'] = new_content
						# print("Content Exception: " + str(e))
						pass
				if elements[x]['value'].text:
					text = str(element.text).replace("\\t", "").replace("\\r", "").replace("\\n", "").strip()  # Remove encoded characters
					new_text = str(re.sub("\s{3,}", ",", text))
					try:
						string = self.base.unicode_to_ascii(new_text)
						result['data']['text'] = string
					except Exception as e:
						result['data']['text'] = str(new_text)
						# print("Text Exception: " + str(e))
						pass
				
				# Domain URL Filters
				if self.arguments.limit:
					if 'target_url' in result['data']:
						target_domain = self.base.get_site_root(result['data']['target_url'])
						protocol = self.base.get_protocol(target_domain)
						# target_domain = target_domain.replace(protocol, '')
						if target_domain in self.arguments.limit:
							results.append(result)
					else:
						results.append(result)
				elif self.arguments.exclude:
					if 'target_url' in result['data']:
						target_domain = self.base.get_site_root(result['data']['target_url'])
						protocol = self.base.get_protocol(target_domain)
						# target_domain = target_domain.replace(protocol, '')
						if not target_domain in self.arguments.exclude:
							results.append(result)
							# print("Excluding link: " + str(result['data']['target_url']))
					else:
						results.append(result)
				else:
					results.append(result)
		return results
	
	def _scrape_components(self, url, response, page_source):
		print("Scraping Components from: " + str(url))
		results = list()
		components_found = 0
		soup = BeautifulSoup(page_source, 'html.parser')
		for index, value in self.available_components.items():
			component_name = value['component_name']
			component_description = value['component_description']
			html_element = value['html_element']
			html_attribute = value['html_attribute']
			attribute_value = value['attribute_value']
			execute_command = value['execute_command']
			success = 0
			if html_element.lower() == "xpath":
				print("Checking XPATH: " + str(attribute_value))
				htmlparser = etree.HTMLParser()
				# tree = etree.parse(str(page_source), htmlparser)
				tree= etree.fromstring(str(page_source), htmlparser)
				r = tree.xpath(str(attribute_value))
				if len(r) != 0:
					success = 1
					components_found += 1
			else:
				soup_results = soup.findAll(html_element, {html_attribute: attribute_value})
				if len(soup_results) >= 1:
					components_found += 1
					success = 1
			if success == 1:
				result = {'url': str(url),
							'index': components_found,
							'found_on': str(url),
							'elementType': 'components',
							'component_name': component_name,
							'component_description': component_description,
							'html_element': html_element,
							'html_attribute': html_attribute,
							'attribute_value': attribute_value,
							'execute_command': execute_command}
				results.append(result)
		print(str(components_found) + " Components FOUND on " + str(url))
		# print("\n\n")
		return results
	
	def _scrape_page_tests(self, url):
		print("Checking if Page Test exists for: " + str(url))
		results = list()
		page_tests_found = 0
		for index, value in self.available_page_tests.items():
			description = value['description']
			db_url = value['page_test_url']
			execute_command = value['execute_command']
			success = 0
			if str(db_url) == url:
				success = 1
				page_tests_found += 1
			
			if success == 1:
				result = {'url': str(url),
							'index': page_tests_found,
							'elementType': 'page_tests',
							'page_test_url': db_url,
							'description': description,
							'execute_command': execute_command}
				results.append(result)
		print(str(page_tests_found) + " Page Tests Found on: " + str(url))
		# print("\n\n")
		return results
	
	def _sort_dict(self):
		print("Sorting Scraped Results")
		verifiable = ['images', 'links', 'iframes']
		for url_key in self.scrape_results.keys():  # Sort Through URLs dictionary and organize it
			for et_key, et_value in self.scrape_results[url_key].items():  # Sort Through Element Types (images, links, forms, etc)
				ignored_count = 0
				x = 0
				if et_key not in verifiable:  # If not a link or image, skip and add to dictionary
					if url_key not in self.sorted_results:
						self.sorted_results[url_key] = {}
					self.sorted_results[url_key][et_key] = et_value
				else:
					for index, value in self.scrape_results[url_key][et_key].items():  # If Element Type is an image or link
						# print("\nKey: " + str(index) + ":\nValue: " + str(value))
						# If not a verifiable link, add to dictionary under ignored_<key>
						# if ('target_url' not in value) or ('href' in value.keys() and (value['href'].startswith(('java', '#', 'data')))) or \
						# 		('src' in value.keys() and value['src'].startswith(('data:'))):
						if 'target_url' not in value:
							ignored_count += 1
							# Add Item to Ignored Key in New Dictionary
							if url_key not in self.sorted_results:
								self.sorted_results[url_key] = {}
							if "ignored_" + str(et_key) not in self.sorted_results[url_key]:
								self.sorted_results[url_key]['ignored_' + str(et_key)] = {}
							if ignored_count not in self.sorted_results[url_key]['ignored_' + str(et_key)]:
								value['original_scraped_index'] = int(index)
								self.sorted_results[url_key]['ignored_' + str(et_key)][ignored_count] = value
						else:
							x += 1
							# Add Item to Ignored Key in New Dictionary
							if url_key not in self.sorted_results:
								self.sorted_results[url_key] = {}
							if str(et_key) not in self.sorted_results[url_key]:
								self.sorted_results[url_key][str(et_key)] = {}
							if x not in self.sorted_results[url_key][str(et_key)]:
								value['original_scraped_index'] = int(index)
								self.sorted_results[url_key][str(et_key)][x] = value
		# logger.write_log(self.sorted_results, 'verifiedInfo')

	def _log(self):
		if 'verify' not in self.arguments.type:
			if self.arguments.excel_output:
				parser = Parse_Excel(self.arguments)
				out_file = parser.scraper_to_excel(self.sorted_results, 'scrapedInfo')
			else:
				out_file = self.logger.write_log(self.sorted_results, 'scrapedInfo')  # Write Scraped Dictionary to json File
			if not self.arguments.no_open:
				self.logger.open_out_file(out_file)
		else:
			verifier = Verify(self.sorted_results, self.arguments)  # Define Verifier
			self.verified_log = verifier.main()  # Run Verifier Method
			self.sorted_results = self.verified_log
			# out_file = self.logger.write_log(self.verified_log, 'verifiedInfo')  # Write Log to json File

