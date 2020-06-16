import sys, getopt
import json
import logging
from datetime import date


fuzzer_logger = logging.getLogger("Fuzzer")

url = "http://localhost/login-1/"
total_base_strings = 10
max_tries = 7
odds_file = "Tools/Database/odds.json"
debug_mode = False

from Tools.sql_generator import *
from Tools.tester import payload_check

def init_args(argv):
    """
    This function initialize the args from cmd/Terminal
    """
    global url, total_base_strings, max_tries, odds_file, debug_mode
    with open("txt/help.txt") as f:
        help_lines = f.readlines()
        help_lines = "".join(help_lines)
    try:
        opts, args = getopt.getopt(argv,"u:b:t:f:d")
    except getopt.GetoptError:
        print("fuzzer.py -u <url to check> -b <max base strings> " \
        "-t <max tries for string> -f <odds filename> -d\n" + help_lines)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("fuzzer.py -u <url to check> -t <max base strings> " \
            "-c <max commands> -f <odds filename> -d\n" + help_lines)
            sys.exit()
        elif opt in "-u":
            url = arg
        elif opt in "-b":
            total_base_strings = int(arg)
        elif opt in "-t":
            max_tries = int(arg)
        elif opt in "-f":
            odds_file = arg
        elif opt in "-d":
            debug_mode = True
    init_stats(odds_file)

def change_info_in_string(s, info):
    """
    This function is an addon to the txt_results function.
    It help altering info inside the report format easier.
    """
    num_len = len(str(info))
    zero_index = s.find("0")

    s = s[:zero_index] + str(info) + s[zero_index + num_len:]
    return s

def txt_results():
    today = date.today()
    date_today = today.strftime("%m_%d_%y")
    filename = "{}_report_s{}_e{}.txt".format(date_today, len(successful_list), len(error_list))
    s = ""
    # Adding the fixed report info
    with open("txt/sample_report.txt") as f:
        lines = f.readlines()
    for l in lines[:5]:
        s += l
    # Adding the tries and success info
    total_tries = len(garbage) + len(error_list) + len(successful_list)
    s += change_info_in_string(lines[5], total_tries)
    s += change_info_in_string(lines[6], len(successful_list))
    s += change_info_in_string(lines[7], len(error_list))

    for l in lines[8:11]:
        s += l

    s += change_info_in_string(lines[11], total_base_strings)
    s += change_info_in_string(lines[12], max_tries)

    for l in lines[13:16]:
        s += l
    s += change_info_in_string(lines[16], filename)

    for l in lines[17:18]:
        s += l

    with open(filename, "w") as f:
        f.write(s)

        f.write("\nSuccessful Strings\n------------------\n")
        for id, tried_string in successful_list:
            f.write(tried_string + "\n")

        f.write("\nError Strings\n-------------\n")
        for id, tried_string in error_list:
            f.write(tried_string + "\n")

        f.write("\nNone Effective Strings\n----------------------\n")
        for id, tried_string in garbage:
            f.write(tried_string + "\n")

    return s


def fuzzing():
    """
    This is the fuzzing function.
    It generates strings and tries them.
    The function prints a summarized report and returns the successful strings
    """
    global garbage, error_list, successful_list
    s_list = [] # Stores the base strings
    garbage = [] # Stores the old, non-working strings
    abnormal = [] # Stores the strings with abnormal behaviours
    error_list = []
    successful_list = []

    # Making the base strings
    print("Making the base strings")
    for i in range(total_base_strings):
        id, s = create_string()
        fuzzer_logger.info(" Base string: {}, id: {}".format(s, id))
        s_list.append((id, s))

    print("Checking strings...")
    # Testing every base string
    for id, s in s_list:
        check = payload_check(url, s)
        fuzzer_logger.info(" Checked: {}, Result: {}".format(s, check))
        if check != "normal":
            abnormal.append((id, s))
    # Removing abnormal strings from s_list
    s_list = [(id,s) for id, s in s_list if (id,s) not in abnormal]


    print("First results:\n  Tried strings: {}\n"\
    "  Abnormal Strings: {}".format(str(len(abnormal) + len(s_list)), len(abnormal)))

    print("Trying to upgrade the \"normal\" strings")
    # Adding commands to the "normal" base string to get different result
    if debug_mode:
        fuzzer_logger.info(" Upgrading \"normal\" strings")
    for id, s in s_list:
        tries = 0
        fuzzer_logger.info(" Upgrading \"normal\" string: {}".format(s))
        while tries < max_tries:
            tries += 1
            garbage.append((id,s))
            id, s = upgrade(id)
            check = payload_check(url, s)
            fuzzer_logger.info("   Checked: {}, Result: {}".format(s, check))
            if check != "normal":
                abnormal.append((id,s))
                break

    print("Adding another command to abnormal strings")
    # Upgrading abnormal strings to try and make them better
    if debug_mode:
        fuzzer_logger.info(" Checking abnormal strings")
    for id, s in abnormal:
        garbage.append((id, s))
        id, s = upgrade(id)
        check = payload_check(url, s)
        fuzzer_logger.info(" Checked: {}, Result: {}".format(s, check))
        if check == "normal":
            # abnormal string has stopped working
            garbage.append((id, s))
            continue
        if check == "error":
            # Same result as before, still interesting
            error_list.append((id, s))
        if check == "success":
            # This is a perfect string, goes straight to save
            successful_list.append((id, s))

    error_list += abnormal
    print("Now checking all the strings that made errors")
    # Trying to make error string be successful
    fuzzer_logger.info(" Adding finishing touches(comments) to error strings")
    for id, s in error_list:
        tries = 0
        while tries < max_tries:
            tries += 1
            garbage.append((id, s))
            id, s = finishing_touches(id)
            check = payload_check(url, s)
            fuzzer_logger.info(" Checked: {}, Result: {}".format(s, check))
            if check == "error":
                continue # nothing has changed, continue to check
            if check == "normal":
                garbage.append((id, s)) # error string broke, throw it to garbage
                break
            if check == "success":
                successful_list.append((id, s)) # the string is perfect!, Saving it...
                break

    print(txt_results())
    return successful_list



if __name__ == '__main__':
    init_args(sys.argv[1:])

    logging.basicConfig(filename="" if debug_mode else "logs/fuzzer.log", level=logging.DEBUG)
    fuzzer_logger.debug("URL: {}, Max base strings: {},"\
    "Max tries per string: {}, Odds file: {}, "\
    "Debug: {}".format(url, total_base_strings, max_tries, odds_file, debug_mode))

    fuzzing()