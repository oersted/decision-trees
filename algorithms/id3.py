from collections import Counter
from .base import DecisionTree
from . import utils

class InvalidDataError(Exception):
    pass

class ID3Tree(DecisionTree):
    def __init__(self, *args, **kwargs):
        self.gains = {}
        self._gain_data = []
        super(ID3Tree, self).__init__(*args, **kwargs)

    def render(self, output_file_path = None):
        super(ID3Tree, self).render(output_file_path)
        self._write('\n\n')
        for i in range(len(self._gain_data)):
            if self._gain_data[i]:
                self._write(str(i + 1) + ':\n')
                for option in self._gain_data[i]:
                    self._write(
                        ' * ' + option + ': ' + str(self._gain_data[i][option]) + '\n')
                self._write('\n')
        self._gain_data = []

    def _render(self, tree, indent):
        if len(tree.children) != 0:
            self._gain_data.append(tree.gains)
        super(ID3Tree, self)._render(tree, indent)


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