from flask import Blueprint, render_template, request
import modules.queries as queries
import modules.insertQueries as insertQueries

bp = Blueprint('html', __name__,)

@bp.route('/packages')
@bp.route('/')
def index():
	"""
	Route for getting all the package names for the front page.
	"""
	results = queries.index()
	tags = queries.tags()
	return render_template('index.html', packages=results, tags=tags, currentFilter=None)

@bp.route('/packages/<id>', methods=['GET'])
def package(id = 0):
	"""
	Route for getting all the information about a single package.
	"""
	results = queries.package(id)
	if not results:
		return render_template('package_not_found.html')
	return render_template('package.html', package=results)

@bp.route('/packages/<id>', methods=['POST'])
def addTag(id = 0):
	"""
	Route for adding a tag to a package
	"""
	insertQueries.addTag(request.form)
	results = queries.package(id)
	return render_template('package.html', package=results)

@bp.route('/tagged/<tag>')
def tagged(tag = ''):
	"""
	Route for getting list of packages tagged with {tag}
	"""
	results = queries.tagged(tag)
	tags = queries.tags()
	return render_template('index.html', packages=results, tags=tags, currentFilter=tag)

@bp.route('/apiDocs')
def apiDocs():
	"""
	Route for API documentation
	"""
	return render_template('apiDocs.html')
