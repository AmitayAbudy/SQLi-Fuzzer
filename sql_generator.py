import random
import uuid
import db

opening_odds, sql_odds, commands_odds, comment_odds = db.init_stats("odds.json")

string_trees = []

def new_string():
    """
    This function creates a new opening string.
    the function stores the string in  a new tree, and saves the tree in string_trees
    The function returns the string id, and the string itself
    """
    id = uuid.uuid4()
    s = ""

    # creating the string
    for i in range(random.randrange(1, 4)):
        s += random.choice(opening_group)

    s += " "

    # making a tree for the string
    if db.is_created(s):
        return new_string() # Is there a better solution?

    string_trees.append(db.new_string_tree(s, id))

    return id, s

def add_command(id):
    """
    This function takes an id of an opening string, and creates a test string.
    The function stores the test string as a son in the tree
    The function returns the second id with the test string itself.
    """
    s_id = uuid.uuid4()
    s = db.get_value(id)

    s += random.choice(["AND", "OR", ""]) + " "
    s += random.choice(commands_group) + " "

    if db.is_created(s):
        return add_command(id) # Is there a better solution?

    db.add_son(id, s, s_id)

    return s_id, s

def add_comment(id):
    """
    The function gets the id of a string and adds a commnet to the string.
    The functon also saves the string as the son of the id node, in it's tree.
    The function returns the id and the result string
    """
    s_id = uuid.uuid4()
    s = db.get_value(id)

    s += random.choice(comment_group) + " "

    if db.is_created(s):
        return add_comment(id) # Is there a better solution?

    db.add_son(id, s, s_id)

    return s_id, s



if __name__ == '__main__':

    id, s = new_string()
    print(s)
    id1, s = add_command(id)
    print(s)
    id2, s = add_comment(id1)
    print(s)
