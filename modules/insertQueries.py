from modules.DBConnection import DBConnection

def realStrip(s: str) -> str:
	return ''.join(str(s).split())

def addTag(data):
	data = data.to_dict()
	if not data['id'] or not data['tag']:
		return False

	query = "INSERT INTO tags (package, tag) VALUES (?, ?);"
	dbConnection = DBConnection()
	cursor = dbConnection.connection.cursor()
	try:
		cursor.execute(query, (int(data['id']), realStrip(data['tag'])))
		dbConnection.connection.commit()
		ret = True
	except:
		ret = False
	dbConnection.close()
	return ret
