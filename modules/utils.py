import re
from typing import List

from modules.DBConnection import DBConnection

def tagsStringParser(tagsString: str) -> List[str]:
	if not tagsString:
		return []
	else:
		return tagsString.split('#CONCAT_PLACEHOLDER#')

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
	line = line[line.lower().find("depends: ") + 9:-1] # Can also be "Pre-Depends"
	dependencies = line.split(", ")
	for dependency in dependencies:
		if " | " in dependency: # Substitutable depedencies
			subDependencies = dependency.split(" | ")
			subDependencies = [cleanDependency(dep) for dep in subDependencies]
			subDeps.append(subDependencies)
		else:
			strictDeps.append(cleanDependency(dependency))

def tagSuperDependencies():
	"""
	Tag packages with at least 20 dependents as super-dependencies
	"""
	dbConnection = DBConnection()
	cursor = dbConnection.connection.cursor()

	query = """
INSERT INTO tags (package, tag)
	SELECT id, 'Super Dependency'
		FROM (SELECT id, COUNT(*) AS c
			FROM dependencyIdAndNameAndSubId
			GROUP BY dependency HAVING c > 19)
		WHERE id NOT NULL;
"""
	try:
		cursor.execute(query)
		dbConnection.connection.commit()
	except:
		pass

	dbConnection.close()
