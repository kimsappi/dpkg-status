from flask import Flask

import modules.dpkgParser as dpkgParser
from modules.DBConnection import DBConnection
from routes.api import bp as apiBp
from routes.html import bp as htmlBp

app = Flask(__name__)

# The routes are specified in these blueprints
app.register_blueprint(apiBp, url_prefix='/api')
app.register_blueprint(htmlBp)

if __name__ == '__main__':
	# Database initialisation
	dbConnection = DBConnection()
	with open('dbSchema.sql') as f:
		dbSchema = ''.join(f.readlines())
	cursor = dbConnection.connection.cursor().executescript(dbSchema)
	dbConnection.close()

	# Reading the file into a string
	fileData = dpkgParser.readFile()
	# Initialising all the packages as names in the DB
	dpkgParser.initialisePackages(fileData)
	# Completing all the other information.
	# The file has to be traversed twice, because there might be dependencies
	# that aren't present in the file.
	dpkgParser.completePackageInformation(fileData)

	app.run(host='0.0.0.0', port=3000, debug=True)
