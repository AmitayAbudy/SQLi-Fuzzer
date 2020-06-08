import random
import uuid

opening_group = ["\'", "\"", ")"]
commands_group = ["1=1", "SLEEP(5)", "1=0"]
comment_group = ["--", ";", "/*"]

open_strings = {} # This dict contains all the generated strings
command_strings = {}

def new_string():
    """
    This function creates a new opening string.
    The function returns the string id, and the string itself
    """
    id = uuid.uuid4()
    s = ""

    for i in range(random.randrange(1, 4)):
        s += random.choice(opening_group)

    s += " "

    for check_id in open_strings.keys(): # Temporary solution! Needs more work
        if s == open_strings[check_id]:
            return new_string()

    open_strings[id] = s
    command_strings[id] = {}

    return id, s

def add_command(id):
    """
    This function takes an id of an opening string, and creates a test string.
    The function stores the test string with the same id in command_strings
    and using a new id for the second dict.
    The function returns the second id with the test string itself.
    """
    second_id = uuid.uuid4()
    s = open_strings[id]

    s += random.choice(["AND", "OR", ""]) + " "
    s += random.choice(commands_group) + " "

    command_dict = command_strings[id]

    for check_id in command_dict.keys(): # Temporary solution! Needs more work
        if s == command_dict[check_id]:
            return add_command(id)

    command_dict[second_id] = s
    return second_id, s


def create():
    s = ""
    s += random.choice(opening_group) + " "
    s += random.choice(commands_group) + " "
    s += random.choice(comment_group)
    return s

if __name__ == '__main__':
    pass
