from typing import List
import sqlite3, os, re

from modules.Package import Package
from modules.DBConnection import DBConnection

def readFile() -> List[str]:
	"""
	Loads the contents of dpkg/status into an array of strings.
	"""
	if os.access("/var/lib/dpkg/status", os.R_OK):
		filepath = "/var/lib/dpkg/status"
	else:
		filepath = "example_dpkg_status"

	with open(filepath) as f:
		return f.readlines()

def initialisePackages(lines: str):
	"""
	Loop through all the packages once to insert all the names into the DB
	"""
	packages = []

	for line in lines:
		if re.match("Package: ", line):
			name = line[line.find(" ") + 1:-1]
			packages.append((name,)) # DB expects a tuple

	dbConnection = DBConnection()
	dbCursor = dbConnection.connection.cursor()

	query = 'INSERT INTO packages ("name") VALUES (?);'
	dbCursor.executemany(query, packages)
	dbConnection.connection.commit()
	dbConnection.close()

def cleanDependency(line: str) -> str:
	"""
	Removes version information (if any) from a dependency string.
	"""
	name = re.sub(" \(.*\)", "", line)
	return name

def parseDependencies(line: str, strictDeps: List[str], subDeps: List[str]):
	"""
	Appends all dependencies in a line to deps. Typical dependencies will be
	appended as strings. Dependencies that can be substituted with another
	package will be appended as List[str].
	"""
	line = line[line.find("Depends: ") + 9:-1] # Can also be "Pre-Depends"
	dependencies = line.split(", ")
	for dependency in dependencies:
		if " | " in dependency: # Substitutable depedencies
			subDependencies = dependency.split(" | ")
			subDependencies = [cleanDependency(dep) for dep in subDependencies]
			subDeps.append(subDependencies)
		else:
			strictDeps.append(cleanDependency(dependency))

def completePackageInformation(lines: str):
	"""
	Traverse file again to read and add all the other parsed data
	"""
	dbConnection = DBConnection()
	dbCursor = dbConnection.connection.cursor()

	strictDeps = []
	subDeps = []
	inDescription = False
	description = ""
	for line in lines:
		if re.match("package: ", line.lower()):
			name = line[line.find(" ") + 1:-1]
			inDescription = False

		elif re.match("version: ", line.lower()):
			version = line[line.find(" ") + 1:-1]

		elif re.match("(pre-)?depends: ", line.lower()):
			parseDependencies(line, strictDeps, subDeps)

		elif re.match("description: ", line.lower()):
			descriptionSummary = line[line.find(" ") + 1:-1]
			inDescription = True

		elif re.match(r"\n", line) or (inDescription and not re.match(r" ", line)):
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
			description = ""
			inDescription = False

		# Multiline descriptions handled here
		elif inDescription:
			# Maintainer wants an empty line here
			if re.match(r" .\n", line):
				description += "\n"
			# Otherwise just concatenate
			else:
				description += line[1:]

	dbConnection.connection.commit()
	dbConnection.close()
