from flask import Blueprint, render_template, request
import modules.queries as queries
import modules.insertQueries as insertQueries

bp = Blueprint('html', __name__,)

@bp.route('/')
def index():
	"""
	Route for getting all the package names for the front page.
	"""
	results = queries.index()
	return render_template('index.html', packages=results)

@bp.route('/packages/<id>', methods=['GET'])
def package(id = 0):
	"""
	Route for getting all the information about a single package.
	"""
	results = queries.package(id)
	return render_template('package.html', package=results)

@bp.route('/packages/<id>', methods=['POST'])
def addTag(id = 0):
	"""
	Route for adding a tag to a package
	"""
	insertQueries.addTag(request.form)
	results = queries.package(id)
	return render_template('package.html', package=results)
