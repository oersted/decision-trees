from math import log
from collections import Counter
from .tree import DecisionTree

class InvalidDataError(Exception):
    pass

class ID3Tree(DecisionTree):
    attribute_costs = {}
    use_costs = False
    use_gain_ratio = False

    def __init__(self, *args, **kwargs):
        self.gains = {}
        self._gain_string = ''
        super(ID3Tree, self).__init__(*args, **kwargs)

    def choose_attrib(self, *args):
        return self.id3(*args)

    def id3(self, data, attributes, target_attribute, target_atrib_counter):
        target_attrib_entropy = self._entropy(target_atrib_counter, len(data))
        max_gain_attribute = ""
        max_gain = None
        threshold = None
        max_threshold = None
        for attribute in attributes:
            if self._is_continuous_attribute(attribute):
                attrib_gain, threshold = self._continuous_gain(data, target_attribute,
                    target_attrib_entropy, attribute)
            else:
                attrib_gain = self._gain(data, target_attribute, target_attrib_entropy, attribute)

            if ID3Tree.use_gain_ratio and attrib_gain > 0:
                if self._is_continuous_attribute(attribute):
                    count = Counter()
                    for record in data:
                        if float(record[attribute]) <= threshold:
                            count['<='] += 1
                    count['>'] = len(data) - count['<=']
                else:
                    count = Counter([record[attribute] for record in data])
                intrinsic_information = self._entropy(count, len(data))
                attrib_gain = attrib_gain / intrinsic_information

            if ID3Tree.use_costs:
                attrib_gain = attrib_gain**2/ID3Tree.attribute_costs[attribute]

            if max_gain == None or attrib_gain > max_gain:
                max_gain_attribute = attribute
                max_gain = attrib_gain
                max_threshold = threshold
            self.gains[attribute] = attrib_gain

        return (max_gain_attribute, max_threshold)

    def _entropy(self, count, total):
        entropy = 0
        for key in count:
            if count[key] != 0:
                p = count[key]/float(total)
                entropy -= p * log(p, 2)

        return entropy

    def _continuous_gain(self, data, target_attribute, target_attrib_entropy, attribute):
        try:
            local_data = [(float(record[attribute]), record[target_attribute]) for record in data]
        except ValueError:
            raise InvalidDataError("Unable to convert continuous data to float values.")
        local_data.sort(key=lambda x: x[0])
        smaller_values = Counter()
        bigger_values = Counter(record[1] for record in local_data)

        min_entropy = 1.0
        threshold = None
        count = 0
        total = len(local_data)

        for n in range(0, total - 1):
            count += 1
            smaller_values[local_data[n][1]] += 1
            bigger_values[local_data[n][1]] -= 1

            if local_data[n][0] != local_data[n+1][0]:
                p = count/total
                new_entropy = p * self._entropy(smaller_values, count)
                new_entropy += (1-p) * self._entropy(bigger_values, total-count)
                if new_entropy < min_entropy:
                    min_entropy = new_entropy
                    threshold = local_data[n][0]

        return (target_attrib_entropy - min_entropy, threshold)

    def _gain(self, data, target_attribute, target_attrib_entropy, attribute):
        attrib_gain = target_attrib_entropy
        attribute_values = [record[attribute] for record in data]
        total = len(attribute_values)
        count = Counter(attribute_values)
        for key in count:
            p = count[key]/float(total)
            attrib_values = [record[target_attribute] for record in data if record[attribute] == key]
            attrib_gain -= p * self._entropy(Counter(attrib_values),len(attrib_values))

        return attrib_gain

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
