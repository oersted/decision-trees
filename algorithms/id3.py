from collections import Counter
from .base import DecisionTree
from . import utils

class InvalidDataError(Exception):
    pass

class ID3Tree(DecisionTree):
    def __init__(self, *args, **kwargs):
        self.gains = {}
        self._gain_string = ''
        super(ID3Tree, self).__init__(*args, **kwargs)

    def __str__(self):
        string = super(ID3Tree, self).__str__() + self._gain_string
        self._gain_string = ''
        return string

    def _render(self, indent):
        string = ''
        if len(self.children) != 0:
            string += str(self.__class__._next_tree_number) + ':\n'
            for option in self.gains:
                string += ' * ' + option + ': ' + str(self.gains[option]) + '\n'
            string += '\n'
        self._gain_string += string
        return super(ID3Tree, self)._render(indent)

def choose_attribute(data, attributes, target_name,
                         target_counter, use_gain_ratio=False, costs=None):
    target_entropy = utils.entropy(target_counter, len(data))
    max_gain_attribute = ""
    max_gain = None
    threshold = None
    max_threshold = None
    gains = {}
    for attribute in attributes:
        if utils.is_continuous_attribute(attribute):
            attrib_gain, threshold = utils.continuous_gain(data, target_name,
                target_entropy, attribute)
        else:
            attrib_gain = utils.gain(data, target_name, target_entropy, attribute)

        if use_gain_ratio and attrib_gain > 0:
            if utils.is_continuous_attribute(attribute):
                count = Counter()
                for record in data:
                    if float(record[attribute]) <= threshold:
                        count['<='] += 1
                count['>'] = len(data) - count['<=']
            else:
                count = Counter([record[attribute] for record in data])
            intrinsic_information = utils.entropy(count, len(data))
            attrib_gain = attrib_gain / intrinsic_information

        if costs:
            attrib_gain = attrib_gain**2/costs[attribute]

        if max_gain == None or attrib_gain > max_gain:
            max_gain_attribute = attribute
            max_gain = attrib_gain
            max_threshold = threshold
        gains[attribute] = attrib_gain

    return (max_gain_attribute, max_threshold, gains)
