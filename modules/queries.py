from typing import List
from modules.DBConnection import DBConnection

def dictifySingle(array: List, columns: List[str]):
	ret = {}
	for i in range(len(columns)):
		ret[columns[i]] = array[i]
	return ret

def columnDescriptionToArray(columns: tuple):
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
	for i in range(0, len(dependencies), 2):
		depDict = {}
		depDict['id'] = dependencies[i] if dependencies[i] is not '0' else None
		depDict['name'] = dependencies[i + 1]
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

	depsQuery = f"""
SELECT "name", "version", "description", descriptionSummary,
		GROUP_CONCAT((SELECT id FROM packages WHERE "name"=d.dependency UNION SELECT '0' LIMIT 1) || ' ' || d.dependency, ' ') AS dependencies
	FROM packages AS p
	OUTER LEFT JOIN dependencies AS d ON d.dependent = p."name"
	WHERE {condition};
"""

	revDepsQuery = f"""
SELECT GROUP_CONCAT((SELECT (SELECT id FROM packages WHERE "name"=r.dependent UNION SELECT '0' LIMIT 1)) || ' ' || r.dependent, ' ') AS reverseDependencies
	FROM packages AS p
	OUTER LEFT JOIN dependencies AS r ON r.dependency = p."name"
	WHERE {condition};
"""
	cursor.execute(depsQuery, (id,))
	result = cursor.fetchone()
	cols = cursor.description
	cursor.close()

	cursor = dbConnection.connection.cursor()
	cursor.execute(revDepsQuery, (id,))
	reverseResult = cursor.fetchone()
	reverseCols = cursor.description
	dbConnection.close()
	result = dictify(result + reverseResult, cols + reverseCols)
	result['dependencies'] = separatePackageIdAndName(result['dependencies'])
	result['reverseDependencies'] = separatePackageIdAndName(result['reverseDependencies'])
	return result
