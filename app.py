import os
from flask import Flask

from modules.DpkgParser import DpkgParser
from modules.DBConnection import DBConnection
from routes.api import bp as apiBp
from routes.html import bp as htmlBp
import modules.utils as utils

app = Flask(__name__)

# The routes are specified in these blueprints
app.register_blueprint(apiBp, url_prefix='/api')
app.register_blueprint(htmlBp)

if __name__ == '__main__':
	dbConnection = DBConnection(connect=False)
	# Database initialisation if not initialised
	if not os.path.isfile(dbConnection.getFilename()):
		# Create SQLite database file
		fileCreationSuccess = dbConnection.createDatabaseFile()
		if not fileCreationSuccess:
			print('Cannot create database file, exiting')
			sys.exit()

		# Reopening database connection, as previous couldn't connect
		dbConnection = DBConnection()

		with open('dbSchema.sql') as f:
			dbSchema = ''.join(f.readlines())
		cursor = dbConnection.connection.cursor().executescript(dbSchema)
		dbConnection.close()

		# Reading the file into a string
		pkgData = DpkgParser()
		# Initialising all the packages as names in the DB
		pkgData.initialisePackages()
		# Completing all the other information.
		# The file has to be traversed twice, because there might be dependencies
		# that aren't present in the file.
		pkgData.completePackageInformation()

		utils.tagSuperDependencies()
	dbConnection.close()

	app.run(host='0.0.0.0', port=3000, debug=False)
