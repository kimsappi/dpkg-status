from flask import Blueprint, jsonify
import modules.queries as queries
import modules.insertQueries as insertQueries

bp = Blueprint('api', __name__,)

@bp.route('/packages')
@bp.route('/')
def index():
	"""
	Route for getting all the package names for the front page.
	"""
	results = queries.index()
	return jsonify(results)

@bp.route('/packages/<id>', methods=['GET'])
def package(id = 0):
	"""
	Route for getting all the information about a single package.
	"""
	results = queries.package(id)
	return jsonify(results)

@bp.route('/packages/<id>', methods=['POST'])
def addTag(id = 0):
	"""
	Route for adding a tag to a package
	"""
	success = insertQueries.addTag(request.form)
	if success:
		ret = 'OK'
	else:
		ret = 'error'
	return jsonify(ret)	

@bp.route('/tagged/<tag>')
def tagged(tag = ''):
	"""
	Route for getting list of packages tagged with {tag}
	"""
	results = queries.tagged(tag)
	return jsonify(results)
