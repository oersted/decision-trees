from collections import Counter
from math import log
from .tree import Tree

class ID3_Tree(Tree):
    def __init__(self):
        self.gains = {}
        self._gain_data = []
        super(ID3_Tree, self).__init__()

    def export(self, output_file_path):
        super(ID3_Tree, self).export(output_file_path)
        self._write('\n\n')
        for i in range(len(self._gain_data)):
            self._write(str(i + 1) + ':\n')
            for option in self._gain_data[i]:
                self._write(' * ' + option + ': ' + str(self._gain_data[i][option]) + '\n')
            self._write('\n')

    def _export(self, tree, indent):
        if len(tree.children) != 0:
            self._gain_data.append(tree.gains)
        super(ID3_Tree, self)._export(tree, indent)

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

    return (max_gain_attribute, gains)

def id3(data, target_attribute, attributes):
    tree = ID3_Tree()
    data = data[:]
    target_attrib_values = [record[target_attribute] for record in data]
    target_attrib_counter = Counter(target_attrib_values)
    most_common = target_attrib_counter.most_common(1)[0]

    if not data or len(attributes) == 0 or most_common[1] == len(target_attrib_values):
        tree.label = most_common[0]
        return tree
    else:
        best_attribute, tree.gains = choose_best_attribute(data, target_attribute, target_attrib_counter, attributes)
        tree.label = best_attribute
        best_attribute_options = list(set([record[best_attribute] for record in data]))
        for option in best_attribute_options:
            new_data = [record for record in data if record[best_attribute] == option]
            new_attributes = attributes[:]
            new_attributes.remove(best_attribute)
            subtree = id3(new_data, target_attribute, new_attributes)
            tree.children[option] = subtree

        return tree
