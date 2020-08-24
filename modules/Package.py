from typing import List

class Package:
	"""
	Class that contains information relating to a single package.
	Note:
	self.deps == List whose nodes can be str or List[str] if there are
	dependencies that can be substituted with another package
	self.reverse_deps == List who can be str or dict (key: str (dependent
	package name), value: List[str] (substitutable packages))
	"""
	def __init__(
		self, name: str, description: str, descriptionSummary: str,
		version: str, strictDeps: List, subDeps: List
	):
		self.name = name
		self.description = description
		self.descriptionSummary = descriptionSummary
		self.version = version
		self.strictDeps = strictDeps
		self.subDeps = subDeps
		self.subDepsDict = {}
		self.revDeps = []
		self.subRevDeps = {}

	def addDepsToDB(self, dbCursor):
		depTuples = []
		baseId = 'subDepId'
		i = 0
		for dep in self.strictDeps:
			depTuples.append((self.name, dep, None))

		for subDeps in self.subDeps:
			# Generate a unique identifier for all the substitutable deps
			subDepId = self.name + baseId + str(i)
			i += 1
			for dep in subDeps:
				depTuples.append((self.name, dep, subDepId))

		dbCursor.executemany("""
INSERT INTO "dependencies" ("dependent", "dependency", "substitutionId")
	VALUES (?, ?, ?);""",
			depTuples)

	def addToDB(self, dbCursor):
		# Simple query for the package's own data
		dbCursor.execute("""
UPDATE "packages"
	SET "version"=?, "descriptionSummary"=?, "description"=?
	WHERE "name"=?;
""", (self.version, self.descriptionSummary, self.description, self.name))
		# Add dependencies
		self.addDepsToDB(dbCursor)

	def addDependency(self, dep: tuple):
		# This is called even if there are no dependencies
		if not dep[-2]:
			return

		depDict = {
			# '0' as id means the package isn't in packages, should be None
			# but SQLite doesn't work as expected
			'id': dep[-3] if dep[-3] != '0' else None,
			'name': dep[-2]
		}
		if not dep[-1]:
			self.strictDeps.append(depDict)
		else:
			if not dep[-1] in self.subDepsDict:
				self.subDepsDict[dep[-1]] = []
			self.subDepsDict[dep[-1]].append(depDict)

	def addStrictReverseDependency(self, revDep: tuple):
		if (revDep[1]):
			self.revDeps.append({'id': revDep[0], 'name': revDep[1]})

	def addSubReverseDependencies(self, revDep: tuple, subRevDeps: List[tuple]):
		revDepKey = f'{revDep[0]} {revDep[1]}'
		self.subRevDeps[revDepKey] = [{
			'dependentId': revDep[0],
			'dependentName': revDep[1]
		}]
		for subDep in subRevDeps:
			self.subRevDeps[revDepKey].append({
				'id': subDep[0],
				'name': subDep[1]
			})

	def toDict(self):
		return {
			'name': self.name,
			'version': self.version,
			'descriptionSummary': self.descriptionSummary,
			'description': self.description,
			'dependencies': self.strictDeps + list(self.subDepsDict.values()),
			'reverseDependencies': self.revDeps + list(self.subRevDeps.values())
		}

	def __lt__(self, other):
		return self.name <= other.name
