import sys, getopt
import json
import logging

from sql_generator import *
from tester import payload_check

logging.basicConfig(filename="logs/fuzzer.log", level=logging.DEBUG)
fuzzer_logger = logging.getLogger("Fuzzer")

url = "http://localhost/login-1/"
total_base_strings = 10
max_tries = 7
odds_file = "odds.json"
debug_mode = False

def init_args(argv):
    """
    This function initialize the args from cmd/Terminal
    """
    global url, total_base_strings, max_commands, odds_file, debug_mode
    with open("txt/help.txt") as f:
        help_lines = f.readlines()
        help_lines = "".join(help_lines)
    try:
        opts, args = getopt.getopt(argv,"u:b:t:f:d")
    except getopt.GetoptError:
        print("fuzzer.py -u <url to check> -b <max base strings> " \
        "-t <max tries for string> -f <odds filename>\n" + help_lines)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("fuzzer.py -u <url to check> -t <max base strings> " \
            "-c <max commands> -f <odds filename>\n" + help_lines)
            sys.exit()
        elif opt in "-u":
            url = arg
        elif opt in "-b":
            total_base_strings = arg
        elif opt in "-t":
            max_commands = arg
        elif opt in "-f":
            odds_file = arg
        elif opt in "-d":
            debug_mode = True

def change_info_in_string(s, info):
    """
    This function is an addon to the txt_results function.
    It help altering info inside the report format easier.
    """
    num_len = len(str(info))
    s = s[:39] + str(info) + s[39 + num_len:]
    return s

def txt_results(tries_num, success_num, strings_list):
    s = ""
    # Adding the fixed report info
    with open("txt/sample_report.txt") as f:
        lines = f.readlines()
    for l in lines[:5]:
        s += l
    # Adding the tries and success info
    s += change_info_in_string(lines[5], tries)
    s += change_info_in_string(lines[5], success)

    for l in lines[7:10]:
        s += l

    s += change_info_in_string(lines[10], total_base_strings)
    s += change_info_in_string(lines[11], max_commands)

    for l in lines[12:17]:
        s += l

    with open("report_file.txt", "w") as f:
        f.write(s + "\n")
        for tried_string in strings_list:
            f.write(tried_string + "\n")

    return s


def fuzzing():
    """
    This is the fuzzing function.
    It generates strings and tries them.
    The function prints a summarized report and returns the successful strings
    """
    garbage = [] # Stores the old, non-working strings
    s_list = [] # Stores the base strings
    abnormal = [] # Stores the strings with abnormal behaviours

    # Making the base strings
    for i in range(total_base_strings):
        s = create_string(5)
        if debug_mode:
            fuzzer_logger.debug("Base string: {}".format(s))
        s_list.append(s)

    # Testing every base string
    for s in s_list:
        c = payload_check(s, check_address)
        if debug_mode:
            fuzzer_logger.debug("Checked: {}, Result: {}".format(s, c))
        if c is not "normal":
            # tester.notify(c)
            abnormal.append(s)
            s_list.remove(s)

    # Adding commands to the "normal" base string to get different result
    for s in s_list:
        tries = 0
        if debug_mode:
            fuzzer_logger.debug("Upgrading \"normal\" strings:")
        while tries < max_tries:
            garbage.append(s)
            s = upgrade(s)
            c = check(s, check_address)
            if debug_mode:
                fuzzer_logger.debug("Checked: {}, Result: {}".format(s, c))
            if c is not "normal":
                # tester.notify(c)
                abnormal.append(s)
                s_list.remove(s)
                break

    # Trying to make error strings have a success
    if debug_mode:
        fuzzer_logger.debug("Checking abnormal strings")
    for s in abnormal_strings:
        garbage.append(s)
        s = input.upgrade()
        c = check(s, check_address)
        if debug_mode:
            fuzzer_logger.debug("Checked: {}, Result: {}".format(s, c))
        if c is "normal":
            # abnormal string has stopped working
            garbage.append(s)
            continue
        if c is "error":
            # Same result as before, still interesting
            error_list.append(s)
        if c is "success":
            # This is a perfect string, goes straight to save
            successful_list.append(s)

    # Trying to make error string be successful
    if debug_mode:
        fuzzer_logger.debug("Cheking error strings")
    for s in error_list:
        tries = 0
        while tries < max_tries_per_string:
            garbage.append(s)
            s = input.upgrade(s)
            c = tester.check(s, check_site)
            if debug_mode:
                fuzzer_logger.debug("Checked: {}, Result: {}".format(s, c))
            if c is "error":
                continue # nothing has changed, continue to check
            if c is "normal":
                garbage.append(s) # error string broke, throw it to garbage
                break
            if c is "success":
                successful_list.append(s) # the string is perfect!, Saving it...
                break

    total_tries = len(s_list) + len(garbage) + len(error_list) + len(successful_list)
    print(txt_results(total_tries, len(successful_list)))

    return successful_list



if __name__ == '__main__':
    init_args(sys.argv[1:])
    if debug_mode:
        fuzzer_logger.debug("URL: {}, Max base strings: {},"\
        "Max tries per string: {}, Odds file: {}, "\
        "Debug: {}".format(url, total_base_strings, max_tries, odds_file, debug_mode))
    # fuzzing()
