from modules.DBConnection import DBConnection

def index():
	dbConnection = DBConnection()
	cursor = dbConnection.connection.cursor()
	cursor.execute('SELECT "id", "name" FROM packages ORDER BY "name" ASC;')
	results = cursor.fetchall()
	dbConnection.close()
	return results

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
	OUTER LEFT JOIN "dependencies" ON 
"""
