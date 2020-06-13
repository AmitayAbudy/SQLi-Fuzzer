import json

FILENAME = "sql_bank.txt"
JSON_NAME = "odds_new.json"

with open(FILENAME) as f:
	lines = f.readlines()

unique_char = set()

for line in lines:
	for chr in line:
		if chr == "\n":
			continue
		unique_char.add(chr)

next_char = {}

for chr in unique_char:
	next_char[chr] = []

for line in lines:
	for i in range(len(line)):
		if line[i] == "\n" or line[i+1] == "\n":
			break
		next_char[line[i]].append(line[i+1])

stats_char = {}

for key, value in next_char.items():
	# print(value)
	total_chars = len(value)
	stats_char[key] = {}
	for chr in set(value):
		char_count = value.count(chr)
		stat = float(char_count / total_chars)
		stats_char[key][chr] = stat

json_string = json.dumps(stats_char, indent=4)
with open(JSON_NAME, "w") as f:
	f.write(json_string)
