from typing import List

def tagsStringParser(tagsString: str) -> List[str]:
	if not tagsString:
		return []
	else:
		return tagsString.split('#CONCAT_PLACEHOLDER#')
