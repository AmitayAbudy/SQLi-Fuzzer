import random

GRADES_FILE="grades.txt"
chars = {} # Identify the score of each character
old_strings = []
special_charecters = [",", "/", "\\", "\'", "\"", "*", ")", "%", "=", "-"] # special charecters to add extra garde

def is_file_empty(filepath):
	""" Check if file is empty by reading first character in it"""
	# open ile in read mode
	read_obj = open(filepath, 'r')
	# read first character
	one_char = read_obj.read(1)
	# if not fetched then file is empty
	if not one_char:
		return True
	return False

def update_grades_from_file(filepath):
	"""
	This function is updating the grades in the run using the grade in the file
	"""
	f = open(GRADES_FILE, "r")
	grade_lines = f.readlines()

	for line in grade_lines:
		if len(line.split(" ")) == 3:
			chars[" "] = int(line.split(" ")[-1])
			continue

		char, grade = line.split(" ")
		chars[char] = int(grade)

	f.close()

def update_grades_to_file(filepath):
	"""
	This file is in charge of back up the current grades in the running file to a backup grades file
	"""
	f = open("grades.txt", "w")
	for char, grade in chars.items():
		f.write("{0} {1}\n".format(str(char), str(grade)))
	f.close()


def initialize():
	# Check if there is a backup for grades
	if is_file_empty(GRADES_FILE):
		# The file is empty so we will fill it with new grades
		for i in range(33, 127):
			chars[chr(i)] = 0

		# Add extra score to specific characters
		for char in special_charecters:
			chars[char] += 1
	else:
		update_grades_from_file(GRADES_FILE)

	# Anyway before starting to handle, we backup the grades file
	update_grades_to_file(GRADES_FILE)


"""
def create_string(grade, length):

	total_grade = 0
	s = ""

	while (len(s) < length or total_grade < grade) and s not in old_strings:
		if len(s) == length and total_grade < grade:
			s = ""
		elif len(s) == length and total_grade == grade:
			bre
		char, ch_grade = random.choice(chars.items())
		
		s += char
		total_grade += ch_grade

	old_strings.append(s)
	return s
"""

def make_string(length):
	"""
	Creates string and returns the string with the grade
	"""
	total_grade = 0
	s = ""

	while len(s) < length and s not in old_strings:
		char, ch_grade = random.choice(list(chars.items()))
		
		s += char
		total_grade += ch_grade

	return s

def add_grade(s):
	"""
	Adding more grade to characters by a good string
	:param: s - A string to use 
	"""
	for char in s:
		chars[char] += 1

if __name__ == '__main__':
	initialize()