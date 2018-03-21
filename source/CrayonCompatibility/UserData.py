
def UserData_fileReadText(path):
	return read_text_file('saves/' + path)

def UserData_fileWriteText(path, content):
	return write_text_file('saves/' + path, content)

def UserData_fileExists(path):
	return file_exists('saves/' + path)

UserData = EmptyObj()
UserData.fileReadText = UserData_fileReadText
UserData.fileWriteText = UserData_fileWriteText
UserData.fileExists = UserData_fileExists
