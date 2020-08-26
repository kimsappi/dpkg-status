from typing import List
import sqlite3, os, re

from modules.Package import Package
from modules.DBConnection import DBConnection
import modules.utils as utils

class DpkgParser:
	"""
	Class for parsing the file and committing it to the database
	"""

	def __init__(self):
		"""
		Loads the contents of dpkg/status into an array of strings.
		"""

		if os.access("/var/lib/dpkg/status", os.R_OK):
			filepath = "/var/lib/dpkg/status"
		else:
			filepath = "example_dpkg_status"

		with open(filepath) as f:
			self.lines = f.readlines()

	def initialisePackages(self):
		"""
		Loop through all the packages once to insert all the names into the DB
		"""
		packages = []

		for line in self.lines:
			if re.match("Package: ", line):
				name = line[line.find(" ") + 1:-1]
				packages.append((name,)) # DB expects a tuple

		dbConnection = DBConnection()
		dbCursor = dbConnection.connection.cursor()

		query = 'INSERT INTO packages ("name") VALUES (?);'
		dbCursor.executemany(query, packages)
		dbConnection.connection.commit()
		dbConnection.close()

	

	def completePackageInformation(self):
		"""
		Traverse file again to read and add all the other parsed data
		"""
		dbConnection = DBConnection()
		dbCursor = dbConnection.connection.cursor()

		strictDeps, subDeps = [], []
		inDescription = False
		description, descriptionSummary, name = '', '', ''
		for line in self.lines:
			if re.match("package: ", line.lower()):
				name = line[line.find(" ") + 1:-1]
				inDescription = False

			elif re.match("version: ", line.lower()):
				version = line[line.find(" ") + 1:-1]

			elif re.match("(pre-)?depends: ", line.lower()):
				utils.parseDependencies(line, strictDeps, subDeps)

			elif re.match("description: ", line.lower()):
				descriptionSummary = line[line.find(" ") + 1:-1]
				inDescription = True

			elif re.match(r"\n", line):
				thisPkg = Package(
					name=name,
					version=version,
					descriptionSummary=descriptionSummary,
					description=description,
					strictDeps=strictDeps,
					subDeps=subDeps
				)
				thisPkg.addToDB(dbCursor)
				subDeps, strictDeps = [], []
				description, descriptionSummary, name = '', '', ''
				inDescription = False

			# Multiline descriptions handled here
			elif inDescription and re.match(r" ", line):
				# Maintainer wants an empty line here
				if re.match(r" .\n", line):
					description += "\n"
				# Otherwise just concatenate
				else:
					description += line[1:]
		else:
			if len(name):
				thisPkg = Package(
					name=name,
					version=version,
					descriptionSummary=descriptionSummary,
					description=description,
					strictDeps=strictDeps,
					subDeps=subDeps
				)
				thisPkg.addToDB(dbCursor)

		dbConnection.connection.commit()
		dbConnection.close()
