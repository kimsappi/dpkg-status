from flask import Blueprint, render_template
import modules.queries as queries

bp = Blueprint('html', __name__,)

@bp.route('/')
def index():
	"""
	Route for getting all the package names for the front page.
	"""
	results = queries.index()
	return render_template('index.html', packages=results)

@bp.route('/package/<id>')
def package(id = 0):
	"""
	Route for getting all the information about a single package.
	"""
	results = queries.package(id)
