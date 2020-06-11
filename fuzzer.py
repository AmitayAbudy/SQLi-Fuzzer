import sys
import json

from sql_generator import *
from tester import payload_check


def main(URL):
    s_list = []
    for i in range(3):
        s_list.append(new_string())

    check_list = []
    for id, s in s_list:
        for i in range(3):
            check_list.append(add_command(id))
    ready = []

    for id, s in check_list:
        check = payload_check(URL, s)
        print(check, s)
        if check != "normal":
            for i in range(3):
                ready.append(add_comment(id))
    print("Part 2:")
    for id, s in ready:
        check = payload_check(URL, s)
        print(check, s)

    for tree in db.tree_list:
        with open('data.txt', 'w') as outfile:
            json.dump(tree.to_json(), outfile)

if __name__ == '__main__':
    URL = "http://localhost/bricks/login-1/index.php"
    if len(sys.argv) == 2:
        URL = sys.argv[1]

    main(URL)
