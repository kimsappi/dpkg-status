import sqlite3

class DBConnection:
	def __init__(self):
		self.connection = None
		try:
			self.connection = sqlite3.connect('database')

		except sqlite3.Error as e:
			print(e)

	def close(self):
		if self.connection:
			self.connection.close()
