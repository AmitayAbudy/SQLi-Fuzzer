import sys

from sql_generator import create
from tester import payload_check


def main(URL):
    s = create()
    print(payload_check(URL, s))

if __name__ == '__main__':
    URL = "http://localhost/bricks/login-1/index.php"
    if len(sys.argv) == 2:
        URL = sys.argv[1]

    main(URL)
