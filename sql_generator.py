import random

opening_group = ["\'", "\"", ")", "("]
commands_group = ["OR 1=1", "SLEEP(5)"]
comment_group = ["--", ";", "/*"]

def create():
    s = ""
    s += random.choice(opening_group) + " "
    s += random.choice(commands_group) + " "
    s += random.choice(comment_group)
    return s

if __name__ == '__main__':
    print(create())
