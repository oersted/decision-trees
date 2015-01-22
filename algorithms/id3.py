from collections import Counter
from .base import DecisionTree
from . import utils

costs = None
use_gain_ratio = False

class ID3Tree(DecisionTree):
    def __init__(self, *args, **kwargs):
        self.gains = {}
        super(ID3Tree, self).__init__(*args, **kwargs)

    def _post_render(self):
        string = ''
        if len(self.children) != 0:
            string += '\n'
            string += str(self.number) + ':\n'
            for option in self.gains:
                string += ' * ' + option + ': ' + str(self.gains[option]) + '\n'

        for child in self.children.values():
            string += child._post_render()

        return string

def choose_attribute(tree, data, attributes, target_name,
        target_counter):

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
    tree.gains = gains

    return (max_gain_attribute, max_threshold)
