from flask import Blueprint, jsonify
import modules.queries as queries

bp = Blueprint('api', __name__,)

@bp.route('/')
def index():
	"""
	Route for getting all the package names for the front page.
	"""
	results = queries.index()
	return jsonify(results)

@bp.route('/packages/<id>')
def package(id = 0):
	"""
	Route for getting all the information about a single package.
	"""
	results = queries.package(id)
	return jsonify(results)
