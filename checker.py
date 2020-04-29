import blind_sql_injection
import random

with open("sql_bank.txt") as f:
	lines = f.readlines()


def count_specials(s):
	counter = 0
	for char in s:
		if char in blind_sql_injection.special_charecters:
			counter += 1

	return counter

blind_sql_injection.initialize()
"""
s = blind_sql_injection.create_string(2, 10)
print "len: " + str(len(s))
print "special: " + str(count_specials(s))
"""

made_it = False
# s = random.choice(lines)
attempt_num = 0

for s in lines:
	while not made_it:
		attempt_num += 1
		made_sql = blind_sql_injection.make_string(len(s))
		made_it = made_sql == s
		print "Attempt number {0}: {1}. Expected: {2}".format(attempt_num, made_sql, s)
		print "Len: {0}, Specials: {1}".format(len(made_sql), count_specials(made_sql))
	print "Success! Updating grades"
	blind_sql_injection.add_grades(s)


