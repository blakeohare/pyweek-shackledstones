
def Resources_readText(path):
	return read_text_file('source/' + path)

Resources = EmptyObj()
Resources.readText = Resources_readText
