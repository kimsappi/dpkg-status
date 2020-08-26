import os
import sqlite3

class DBConnection:
	def __init__(self, connect: bool = True):
		self.connection = None
		self._filename = 'database'
		if connect:
			try:
				self.connection = sqlite3.connect(self._filename)
			except:
				pass

	def createDatabaseFile(self):
		try:
			open(self._filename, 'w+')
			return True
		except:
			return False

	def close(self):
		if self.connection:
			self.connection.close()

	def getFilename(self):
		return self._filename
