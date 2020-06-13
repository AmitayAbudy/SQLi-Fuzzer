import sys, getopt
import json

from sql_generator import *
from tester import payload_check


# Parameters.
#   -u URL to check, default my test site "http://localhost/bricks/login-1/index.php"
#   -t Max total base strings, default 10
#   -c Max commands, default 7
#   -f odds file (in json format), default "odds.json"
#   -d debug mode, default False

url = "http://localhost/login-1/"
total_base_strings = 10
max_commands = 7
odds_file = "odds.json"
debug_mode = False

def init_args(argv):
    """
    This function initialize the args from cmd/Terminal
    """
    global url, total_base_strings, max_commands, odds_file, debug_mode
    try:
        opts, args = getopt.getopt(argv,"u:t:c:f:d")
    except getopt.GetoptError:
        print("fuzzer.py -u <url to check> -t <max base strings> " \
        "-c <max commands> -f <odds filename>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("fuzzer.py -u <url to check> -t <max base strings> " \
            "-c <max commands> -f <odds filename>")
            sys.exit()
        elif opt in "-u":
            url = arg
        elif opt in "-t":
            total_base_strings = arg
        elif opt in "-c":
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

def txt_results(tries, success):
    s = ""
    # Adding the fixed report info
    with open("sample_report.txt") as f:
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
        f.write(s)

    return s


def fuzzing():
    """
    This is the main function, it's fuzzing the given/default website with the
    specific parameters given and saves a full report file.
    """
    # Making the base strings
    s_list = []
    for i in range(total_base_strings):
        s_list.append(new_string())

    # adding the first command and check each result
    abnormal_strings = []
    for id, s in s_list:
        id, command_string = add_command(id)
        result = payload_check(url, command_string)
        if result != "normal":
            abnormal_strings.append(id, command_string)

def main(URL):
    check_list = []
    for id, s in s_list:
        for i in range(3):
            check_list.append(add_command(id))
    ready = []

    for id, s in check_list:
        check = payload_check(url, s)
        print(check, s)
        if check != "normal":
            for i in range(3):
                ready.append(add_comment(id))
    print("Part 2:")
    for id, s in ready:
        check = payload_check(url, s)
        print(check, s)

    for tree in db.tree_list:
        with open('data.txt', 'w') as outfile:
            json.dump(tree.to_json(), outfile)

if __name__ == '__main__':
    # init_args(sys.argv[1:])
    # print(url, total_base_strings, max_commands, odds_file, debug_mode)
    # main(URL)
    txt_results(11, 11)
