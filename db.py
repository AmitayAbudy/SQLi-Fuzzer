import json
from treelib import Tree, Node

tree_list = []
all_strings = []

def init_stats(filename):
    """
    This function loads the statistics from the json file
    and returns dictionary that inclides two lists:
        one for the next available chars
        and the second for the probability of it.
    """
    with open(filename) as json_file:
        data = json.load(json_file)

    statistics = {}
    for chr, stats in data.items():
        statistics[chr] = (list(stats.keys()), list(stats.values()))

    return statistics


def new_string_tree(s, id):
    """
    This function creates new tree for a string beggining.
    The function returns the created tree.
    """
    new_tree = Tree()
    new_tree.create_node(s, id)

    tree_list.append(new_tree)
    all_strings.append(s)
    return new_tree


def add_son(father_id, son_string, son_id):
    """
    This function adds son to specific node, using father's id
    returns true for success, and false if it didn't find father_id.
    """
    for tree in tree_list:
        if tree.contains(father_id):
            tree.create_node(son_string, son_id, parent=father_id)
            all_strings.append(son_string)
            return True

    return False


def is_created(s):
    """
    This functon make sure that there are no repeated strings.
    Returns true or false to indicate existence
    """
    return s in all_strings


def get_value(id):
    """
    This function gets id and returns the data stored in the tree
    If id doesn't exist, function return False
    """
    for tree in tree_list:
        if tree.contains(id):
            return tree[id].tag

    return "False"

if __name__ == '__main__':
    print(init_stats("odds.json"))
