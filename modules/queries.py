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
	#print('asd################')
	#print(columns)
	#print('asd################')
	if not len(results):
		return None
	elif type(results[0]) is not tuple:
		return dictifySingle(results[0], columnDescriptionToArray(columns))
	else:
		ret = []
		for result in results:
			ret.append(dictifySingle(result, columnDescriptionToArray(columns)))
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
		number = True
	except:
		number = False

	if number:
		query = """
SELECT * FROM "packages" AS "p"
	OUTER LEFT JOIN "dependencies" AS "d" ON "d"."dependent" = "p"."name"
	OUTER LEFT JOIN "dependencies AS "r" ON "r"."dependency" = "r"."name";
"""
	cursor.execute(query)
	result = cursor.fetchone()
	cols = cursor.description
	dbConnection.close()
	return dictify(result, cols)
