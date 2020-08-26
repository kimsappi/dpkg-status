from modules.DBConnection import DBConnection

def addTag(data):
	if type(data) is not dict:
		data = data.to_dict()
	if 'id' not in data.keys() or 'tag' not in data.keys() or len((str(data['tag'])).strip()) < 1:
		return False

	query = "INSERT INTO tags (package, tag) VALUES (?, ?);"
	dbConnection = DBConnection()
	cursor = dbConnection.connection.cursor()
	try:
		cursor.execute(query, (int(data['id']), str(data['tag']).strip()))
		dbConnection.connection.commit()
		ret = True
	except:
		ret = False
	dbConnection.close()
	return ret
