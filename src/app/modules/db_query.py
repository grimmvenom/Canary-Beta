import os
import sys
import platform
import sqlite3
from enum import Enum


class Table_Headers(Enum):
	components = ['component_name', 'component_description', 'html_element', 'html_attribute', 'attribute_value', 'execute_command']
	page_tests = ['description', 'page_test_url', 'execute_command']
	
	
class Components_DB:
	def __init__(self, arguments):
		self.arguments = arguments
		self.database = self.arguments.database
		self.tables = ['components', 'page_tests']
		self.components = dict()
		self.page_tests = dict()
		self.main()
	
	def main(self):
		self.check_db_existance()
		# self.list_components()
		# self.list_page_tests()
		# print(self.components)
		# print(self.page_tests)
		# return self.components, self.page_tests
		
	def check_db_existance(self):
		if os.path.exists(self.database):
			connection = sqlite3.connect(self.database)
		else:
			print(str(self.database) + " NOT Found!")
			exit()
	
	def check_tables_existance(self, table):
		connection = sqlite3.connect(self.database)
		cursor = connection.cursor()
		cursor.execute("select count(*) from sqlite_master where type='table' and name='" + str(table) + "'")
		for row in cursor:
			if row[0] == 1:
				print(str(table) + " Table Found")
				return True
			else:
				print(str(table) + " Table NOT Found")
				return False
		connection.close()
	
	def get_rows(self, table_name):
		connection = sqlite3.connect(self.database)
		cursor = connection.cursor()
		cursor.execute("select * from " + str(table_name))
		results = cursor.fetchall()
		connection.close()
		return results
	
	def list_components(self):
		table_name = 'components'
		found = self.check_tables_existance(table_name)
		if found == True:
			headers = Table_Headers[table_name].value[0:]
			records = self.get_rows(table_name)
			# print(headers)
			# print(" ")
			x = 0
			for record in records:
				x += 1
				if x not in self.components:
					self.components[x] = dict()
				for index, data in enumerate(list(record)):
					header = headers[index]
					# print(header + " : " + str(data))
					self.components[x][header] = str(data)
		else:
			self.components = None
		return self.components
	
	def list_page_tests(self):
		table_name = 'page_tests'
		found = self.check_tables_existance(table_name)
		if found == True:
			headers = Table_Headers[table_name].value[0:]
			records = self.get_rows(table_name)
			# print(headers)
			# print(" ")
			x = 0
			for record in records:
				x += 1
				if x not in self.page_tests:
					self.page_tests[x] = dict()
				for index, data in enumerate(list(record)):
					header = headers[index]
					# print(header + " : " + str(data))
					self.page_tests[x][header] = str(data)
		else:
			self.page_tests = None
		return self.page_tests
