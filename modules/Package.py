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

	def __lt__(self, other):
		return self.name <= other.name
