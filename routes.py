from flask import Blueprint, jsonify

apiBp = Blueprint('api', __name__,)

@apiBp.route('/')
def apiIndex():
	"""
	Route for getting all the package names for the front page.
	"""
	dbConnection = DBConnection()
	cursor = dbConnection.connection.cursor()
	cursor.execute('SELECT "id", "name" FROM packages ORDER BY "name" ASC;')
	return jsonify(cursor.fetchall())
