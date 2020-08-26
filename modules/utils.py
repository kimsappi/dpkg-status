import re
from typing import List

def tagsStringParser(tagsString: str) -> List[str]:
	if not tagsString:
		return []
	else:
		return tagsString.split('#CONCAT_PLACEHOLDER#')

def cleanDependency(line: str) -> str:
	"""
	Removes version information (if any) from a dependency string.
	"""
	name = re.sub(" \(.*\)", "", line)
	return name

def parseDependencies(line: str, strictDeps: List[str], subDeps: List[str]):
	"""
	Appends all dependencies in a line to deps. Typical dependencies will be
	appended as strings. Dependencies that can be substituted with another
	package will be appended as List[str].
	"""
	line = line[line.find("Depends: ") + 9:-1] # Can also be "Pre-Depends"
	dependencies = line.split(", ")
	for dependency in dependencies:
		if " | " in dependency: # Substitutable depedencies
			subDependencies = dependency.split(" | ")
			subDependencies = [cleanDependency(dep) for dep in subDependencies]
			subDeps.append(subDependencies)
		else:
			strictDeps.append(cleanDependency(dependency))
