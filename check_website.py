import requests
from bs4 import BeautifulSoup


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

	# Sends the response to the URL
	r = requests.post(URL, data=params) # TO DO: check automaticly wether or not to send in POST of GET
	return r.status_code, r.elapsed.total_seconds()


if __name__ == '__main__':
	URL = "https://sqlzoo.net/hack/" # The URL to check

	input_fields = get_input_fields(URL) # Saves the unput fields to the list

	# This is where I'll add the corrupted data
	params = {}
	for field in input_fields:
		params[field] = "data"

	status_code, time_elapsed = send_data(URL, params)
	print("Status Code: {0}\nTime Elapsed: {1}".format(status_code, time_elapsed))
