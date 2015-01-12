from collections import Counter
from math import log

class DecisionTree:
    def __init__(self):
        self.label = ""
        self.max_gain = 0
        self.gains = {}
        self.children = {}

def entropy(count, total):
    entropy = 0
    for value in count.most_common():
        p = value[1]/float(total)
        entropy -= p * log(p, 2)

    return entropy

def gain(data, target_attribute, target_attrib_entropy, attribute):
    attrib_gain = target_attrib_entropy
    attribute_values = [record[attribute] for record in data]
    total = len(attribute_values)
    count = Counter(attribute_values)
    for value in count.most_common():
        p = value[1]/float(total)
        attrib_values = [record[target_attribute] for record in data if record[attribute] == value[0]]
        attrib_gain -= p * entropy(Counter(attrib_values),len(attrib_values))

    return attrib_gain

def choose_best_attribute(data, target_attribute, target_atrib_counter, attributes):
    target_attrib_entropy = entropy(target_atrib_counter, len(data))
    max_gain_attribute = ""
    max_gain = None
    gains = {}
    for attribute in attributes:
        attrib_gain = gain(data, target_attribute, target_attrib_entropy, attribute)
        if max_gain == None or attrib_gain > max_gain:
            max_gain_attribute = attribute
            max_gain = attrib_gain
        gains[attribute] = attrib_gain

    return (max_gain_attribute, max_gain, gains)

def id3(data, target_attribute, attributes):
    tree = DecisionTree()
    data = data[:]
    target_attrib_values = [record[target_attribute] for record in data]
    target_attrib_counter = Counter(target_attrib_values)
    most_common = target_attrib_counter.most_common(1)[0]

    if not data or len(attributes) == 0 or most_common[1] == len(target_attrib_values):
        tree.label = most_common[0]
        return tree
    else:
        best_attribute, tree.max_gain, tree.gains = choose_best_attribute(data, target_attribute, target_attrib_counter, attributes)
        tree.label = best_attribute
        best_attribute_options = list(set([record[best_attribute] for record in data]))
        for option in best_attribute_options:
            new_data = [record for record in data if record[best_attribute] == option]
            new_attributes = attributes[:]
            new_attributes.remove(best_attribute)
            subtree = id3(new_data, target_attribute, new_attributes)
            tree.children[option] = subtree

        return tree

def use_decision_tree(record, tree):
    if len(tree.children) == 0:
        return tree.label
    else:
        label = tree.label
        if not label in record:
            return None
        option = record[label]
        new_record = record.copy()
        new_record.pop(label)
        new_tree = tree.children[option]
        return use_decision_tree(new_record, new_tree)