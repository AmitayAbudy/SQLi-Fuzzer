import sql_creator
import random

# Get the strings to use to grade
with open("sql_bank.txt") as f:
	sql_payloads = f.readlines()
	f.close()

# Calculate grade
def count_specials(s):
	counter = 0
	for char in s:
		if char in blind_sql_injection.special_charecters:
			counter += 1

	return counter


sql_creator.initialize()

made_it = False
attempt_num = 0

for payload in sql_payloads:
	print("Now checking " + payload)
	made_it = False
	while not made_it:
		attempt_num += 1
		made_sql = sql_creator.make_string(len(payload))
		made_it = made_sql == payload
		print("Attempt number {0}: {1}. Expected: {2}".format(attempt_num, made_sql, payload))
	print("Success! Updating grades")
	sql_creator.add_grades(s)


"""
while True:
	made_sql = sql_creator.make_string(1)
	print(made_sql)
	if (made_sql == "a"):
		print("No problem")
		break
"""