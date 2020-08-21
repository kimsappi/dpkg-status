from typing import List
from modules.DBConnection import DBConnection
from modules.Package import Package

def constructPackage(results: List[tuple]) -> Package:
	baseData = results[0]
	ret = Package(name=baseData[0], version=baseData[1],
		description=baseData[2], descriptionSummary=baseData[3],
		strictDeps=[], subDeps=[])

	for dependency in results:
		ret.addDependency(dependency)
	return ret

def dictifySingle(array: List, columns: List[str]) -> dict:
	ret = {}
	for i in range(len(columns)):
		ret[columns[i]] = array[i]
	return ret

def columnDescriptionToArray(columns: tuple) -> List:
	ret = []
	for i in range(len(columns[0])):
		ret.append(columns[0][i][0])
	return ret

def dictify(results: tuple, *columns):
	"""
	Converts the returned values to dictionary for easier handling.
	"""
	if not len(results):
		return None
	elif type(results[0]) is not tuple:
		return dictifySingle(results, columnDescriptionToArray(columns))
	else:
		ret = []
		for result in results:
			ret.append(dictifySingle(result, columnDescriptionToArray(columns)))
		return ret

def separatePackageIdAndName(dependencies: str):
	if not dependencies:
		return None
	dependencies = dependencies.split(' ')
	ret = []
	for i in range(0, len(dependencies), 3):
		depDict = {}
		depDict['id'] = dependencies[i] if dependencies[i] is not '0' else None
		depDict['name'] = dependencies[i + 1]
		depDict['subId'] = dependencies[i + 2]
		ret.append(depDict)
	return ret

def index():
	dbConnection = DBConnection()
	cursor = dbConnection.connection.cursor()
	cursor.execute('SELECT "id", "name" FROM packages ORDER BY "name" ASC;')
	results = cursor.fetchall()
	cols = cursor.description
	dbConnection.close()
	return dictify(results, cols)

def package(id: str):
	dbConnection = DBConnection()
	cursor = dbConnection.connection.cursor()

	try: # Checking if user provided numeric id or package name
		int(id)
		condition = 'p.id = ?'
	except:
		condition = 'p."name" = ?'

	# Query that gets all the information about a package, plus the following
	# about all of its dependencies: id, name, substitutionId
	depsQuery = f"""
SELECT "name", "version", "description", descriptionSummary,
		(SELECT id FROM packages WHERE "name"=d.dependency UNION SELECT '0' LIMIT 1) AS dependencyId,
		d.dependency AS dependencyName, d.substitutionId AS dependencySubstitutionId
	FROM packages AS p
	OUTER LEFT JOIN dependencies AS d ON d.dependent = p."name"
	WHERE {condition};
"""
	# Query that gets all the id and name of all packages that depend on this
	# package as well as all potential substitutionIds of those dependencies
	revDepsQuery = f"""
SELECT (SELECT id FROM packages WHERE "name"=r.dependent) AS dependentId,
		r.dependent AS dependencyName, r.substitutionId AS dependencySubstitutionId
	FROM packages AS p
	OUTER LEFT JOIN dependencies AS r ON r.dependency = p."name"
	WHERE {condition};
"""
	cursor.execute(depsQuery, (id,))
	results = cursor.fetchall()
	cursor.close()

	if not len(results):
		return None

	# Initialising a package object with its basic information & dependencies
	package = constructPackage(results)

	cursor = dbConnection.connection.cursor()
	cursor.execute(revDepsQuery, (id,))
	reverseResult = cursor.fetchall()
	dbConnection.close()
	return package.toDict()
