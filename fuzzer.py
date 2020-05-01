import requests
from bs4 import BeautifulSoup

import random # These lines and their use in lines 66,67 are temporary until I finalize the sql_creator
PAYLOADS = "sql_bank.txt"

def get_input_fields(URL):
	"""
	This function gets URL and returns all the id/name of the input tags in this url
	:param: URL - The url to get the info from
	"""
	# Get the html page
	r = requests.get(URL)
	soup = BeautifulSoup(r.text, 'html.parser')

	# Check all the input tags
	fields = []
	for inpt in soup.find_all("input"):
	# Some sites uses the name of the tag to send the data instead of the id
		if "id" in inpt.attrs:
			fields.append(inpt["id"])
		elif "name" in inpt.attrs:
			fields.append(inpt["name"])
		else:
			print("Can't handle this input tag:\n" + str(inpt))

	return fields


def send_data(URL, params):
	"""
	This function sends the givemn parameters in params to the URL using post method
		TO DO: check automaticly wether or not to send in POST of GET
	The function returns the status code of the response and the time it took for the response to come
	:param: URL - The url to send the data to
	:param: params - The parameters to send. MUST BE IN THE FORMAT {id/name: data}
	"""
	# Check how to send the data (get/post)
	r = requests.get(URL)
	soup = BeautifulSoup(r.text, 'html.parser')

	form_tag = soup.find_all("form")
	form_tag = form_tag[0]

	# Sends the response to the URL
	if "method" in form_tag.attrs and form_tag["method"].lower() == "post":
		# Use default - GET
		r = requests.post(URL, data=params)
	else:
		r = requests.get(URL, data=params)


	return r.status_code, r.elapsed.total_seconds()


def main(URL):
	"""
	This function shows how the fuzzer is meant to be used

	:param: URL - This is the url intendent to be checked
	"""
	input_fields = get_input_fields(URL) # Saves the unput fields to the list

	# This is where I'll add the corrupted data
	params = {}
	sql_file = open(PAYLOADS)
	sql_payloads = sql_file.readlines()

	for field in input_fields:
		params[field] = random.choice(sql_payloads)
		print("Now trying: {0} for field: {1}".format(params[field], field))

	status_code, time_elapsed = send_data(URL, params)
	print("Status Code: {0}\nTime Elapsed: {1}".format(status_code, time_elapsed))

if __name__ == '__main__':
	URL = "https://www.hackthissite.org/missions/realistic/4/"

	main(URL)