import numpy as np
import uuid
import db
# from health import calculate_final_stats
MAX_RECURSION = 5
MAX_REPS = 10
# automate this as well
opening_chars = ["\'", "\"", ")", "1"]
comment_chars = ["#", "--", "'vRxe'='vRxe"]
string_trees = []

stats = db.init_stats("odds.json")

def is_duplicated(s):
    """
    This function check if the given s has more than 3 same chars at the end of it.
    returns True or False
    """
    if len(s) < 2:
        return False
    return s[-1] == s[-2]

def create_string(call_time=0):
    """
    This function creates a new string with an opening and a command.
    The function returns the id and the string
    """
    id = uuid.uuid4()
    s = np.random.choice(opening_chars)
    # automate this as well
    current_char = s
    while current_char in opening_chars:
        cmd = np.random.choice(stats[current_char][0], replace=True, p=stats[current_char][1])
        if cmd not in opening_chars:
            if db.is_created(s) and call_time < MAX_RECURSION: # Avoid duplicates
                return create_string(call_time+1)
            string_trees.append(db.new_string_tree(s, id))
            new_id = uuid.uuid4()
            s += " " + cmd
            db.add_son(id, s, new_id)
            return new_id, s
        if not is_duplicated(s):
            s += cmd


def upgrade(id, call_time=0):
    """
    This function adds another command to a string.
    The function gets the string's specific id
    and returns the new id with the string.
    If the given string ends with comment, will return the same string
    """
    new_id = uuid.uuid4()
    s = db.get_value(id)
    current_char = s.split()[-1]
    if current_char in comment_chars:
        return id, s

    cmd = np.random.choice(stats[current_char][0], replace=True, p=stats[current_char][1])
    # trying to avoid finished string (avoiding comments)
    count = 0
    while cmd in comment_chars:
        count += 1
        if count > MAX_REPS:
            s += " " + cmd
            if db.is_created(s) and call_time < MAX_RECURSION: # Avoid duplicates
                return upgrade(id, call_time+1)
            db.add_son(id, s, new_id)
            return new_id, s
        cmd = np.random.choice(stats[current_char][0], replace=True, p=stats[current_char][1])

    s += " " + cmd
    if db.is_created(s) and call_time < MAX_RECURSION: # Avoid duplicates
        return upgrade(id, call_time+1)

    db.add_son(id, s, new_id)
    return new_id, s

def finishing_touches(id):
    """
    This function gets a string id and adds a comment to the string.
    The function returns the new string and the new id.
    If is not possible to add a comment, the function adds a command and returns.
    """
    new_id = uuid.uuid4()
    s = db.get_value(id)
    current_char = s.split()[-1]
    if current_char in comment_chars:
        return id, s

    cmd = np.random.choice(stats[current_char][0], replace=True, p=stats[current_char][1])

    count = 0
    while cmd not in comment_chars:
        count += 1
        if count > MAX_REPS:
            s += " " + cmd
            db.add_son(id, s, new_id)
            return new_id, s
        cmd = np.random.choice(stats[current_char][0], replace=True, p=stats[current_char][1])

    s += " " + cmd
    db.add_son(id, s, new_id)
    return new_id, s


def notify(id):
    pass


if __name__ == '__main__':
    print(create_string()[1])
