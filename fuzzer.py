import sys

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

    for id, s in check_list:
        check = payload_check(URL, s)
        if check != normal:
            print(check, s)

if __name__ == '__main__':
    URL = "http://localhost/bricks/login-1/index.php"
    if len(sys.argv) == 2:
        URL = sys.argv[1]

    main(URL)
