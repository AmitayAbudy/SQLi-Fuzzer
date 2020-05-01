import random

chars = {} # Identify the score of each character
old_strings = []
special_charecters = [",", "/", "\\", "\'", "\"", "*", ")", "%", "=", "-"] # special charecters to add extra garde
def initialize():
	for i in range(33, 127):
		chars[chr(i)] = 0

	# Add extra score to specific characters
	for char in special_charecters:
		chars[char] += 1

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
		char, ch_grade = random.choice(chars.items())
		
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

	print create_string(1, 15)