from collections import Counter
import xml.etree.ElementTree as ET
import sys
from . import utils

class DecisionTree(object):
    _next_tree_number = 1

    def __init__(self, label = ''):
        self.label = label
        self.number = None
        self.children = {}

    def initialize(self, data, attribs, target_attrib, choose_attrib):
        loose_ends = []
        stop, label, counter = self._should_stop_recursion(data, attribs, target_attrib)
        if stop:
            self.label = label
        else:
            loose_ends = self.extend(data, attribs, target_attrib, counter, choose_attrib)
        return loose_ends

    def extend(self, data, attribs, target_attrib, target_attrib_counter, choose_attrib):
        loose_ends = []
        chosen_attrib, threshold = choose_attrib(
            self, data, attribs, target_attrib, target_attrib_counter)
        self.label = chosen_attrib

        if threshold:
            option = chosen_attrib[1:5] + ' <= ' + str(threshold)
            new_tree = self.__class__()
            self.children[option] = new_tree
            rule = lambda x, y: float(x) <= threshold
            new_data, new_attribs = self._create_new_params(
                data, attribs, chosen_attrib, option, rule)
            stop, label, counter = self._should_stop_recursion(new_data, new_attribs, target_attrib)
            if stop:
                new_tree.label = label
            else:
                loose_ends.append((self, option, new_tree, new_data, new_attribs, counter))

            option = chosen_attrib[1:5] + ' > ' + str(threshold)
            new_tree = self.__class__()
            self.children[option] = new_tree
            rule = lambda x, y: float(x) > threshold
            new_data, new_attribs = self._create_new_params(
                data, attribs, chosen_attrib, option, rule)
            stop, label, counter = self._should_stop_recursion(new_data, new_attribs, target_attrib)
            if stop:
                new_tree.label = label
            else:
                loose_ends.append((self, option, new_tree, new_data, new_attribs, counter))
        else:
            # conversion to set used to remove duplicates
            chosen_attrib_options = list(set([record[chosen_attrib] for record in data]))
            for option in chosen_attrib_options:
                new_tree = self.__class__()
                self.children[option] = new_tree
                new_data, new_attribs = self._create_new_params(
                    data, attribs, chosen_attrib, option)
                stop, label, counter = self._should_stop_recursion(new_data, new_attribs, target_attrib)
                if stop:
                    new_tree.label = label
                else:
                    loose_ends.append((self, option, new_tree, new_data, new_attribs, counter))

        return loose_ends

    def _should_stop_recursion(self, data, attribs, target_attrib):
        if not data:
            return (True, 'Unknown', None)
        else:
            target_attrib_values = [record[target_attrib] for record in data]
            target_attrib_counter = Counter(target_attrib_values)
            most_common = target_attrib_counter.most_common(1)[0]

            return (len(attribs) == 0 or most_common[1] == len(target_attrib_values),
                most_common[0] + ' %' + str((float(most_common[1])/len(target_attrib_values)) * 100),
                target_attrib_counter)

    def _create_new_params(self, data, attribs, chosen_attrib, option, rule = lambda x, y: x == y):
        new_data = [record for record in data if rule(record[chosen_attrib], option)]
        new_attribs = attribs[:]
        new_attribs.remove(chosen_attrib)

        return (new_data, new_attribs)

    def use(self, record):
        if len(self.children) == 0:
                return self
        else:
            try:
                option = record[self.label]

                if utils.is_continuous_attribute(self.label):
                    option = float(option)
                    # There will always be only 2 children
                    options = self.children.keys()
                    if ' <= ' in options[0]:
                        threshold = float(options[0].split(' <= ')[1])
                        if option <= threshold:
                            option = options[0] 
                        else:
                            option = options[1]
                    else:
                        threshold = float(options[1].split(' <= ')[1])
                        if option <= threshold:
                            option = options[1]
                        else:
                            option = options[0]

                child = self.children[option]
            except KeyError:
                raise utils.InvalidDataError()
            else:
                record.pop(self.label)
                if len(record) == 0:
                    return child
                else:
                    return child.use(record)

    def save(self, save_file_path):
        root = ET.Element('root', {'label': self.label})
        XMLTree = ET.ElementTree(root)
        for option in self.children:
            self.children[option]._save(root, option)

        f = open(save_file_path, 'w')
        f.write(ET.tostring(root))

    def _save(self, root, option):
        subtree = ET.SubElement(root, 'node', {'label': self.label, 'option': option})
        for option in self.children:
            self.children[option]._save(subtree, option)

    def load(self, input_file_path):
        try:
            XMLTree = ET.parse(input_file_path)
        except:
            sys.stderr.write("The input file couln't be opened.\n")
            sys.exit(2)
        else:
            root = XMLTree.getroot()
            self._load(root)

    def _load(self, XML_element):
        self.label = XML_element.attrib['label']
        for child in XML_element:
            subtree = DecisionTree(child.attrib['label'])
            self.children[child.attrib['option']] = subtree
            subtree._load(child)

    def __str__(self):
        string = '\n'
        string += self._render('')
        self.__class__._next_tree_number = 1
        string += self._post_render()
        string += '\n'
        return string

    def _render(self, indent):
        string = ''
        if len(self.children) == 0:
            string += self.label + '\n'
        else:
            string += self.label + ' <' + str(self.__class__._next_tree_number) + '>'+ '\n'
            self.number = self.__class__._next_tree_number
            self.__class__._next_tree_number += 1

            count = len(self.children) - 1
            for option in self.children:
                string += indent
                if count == 0:
                    string += '\\-'
                    new_indent = indent + (len(option)+5)*' '
                else:
                    string += '|-'
                    new_indent = indent + '|' + (len(option)+4)*' '

                string += option + '-->'

                count -= 1
                string += self.children[option]._render(new_indent)
        return string

    def _post_render(self):
        string = ''
        for option in self.children:
            string += self.children[option]._post_render()
        return string

def choose_attribute(tree, data, attributes, target_attribute, target_attrib_counter):
    from . import id3
    id3_tree = id3.ID3Tree()
    id3_attrib, threshold = id3.choose_attribute(
        id3_tree, data, attributes, target_attribute, target_attrib_counter)

    text = "\nChoose the next attribute that will be used as the pivot:\n"
    for i in range(len(attributes)):
        text += "\t%d. %s (%f)" % (i, attributes[i], id3_tree.gains[attributes[i]])
        if attributes[i] == id3_attrib:
            text += ' [ID3]'
        text += '\n'
    text += "\n"

    fail_text = "That's not an option.\n\n"
    conversion = int
    attribs_range = range(len(attributes))
    condition = lambda x: x in attribs_range
    option = utils.read_option(text, fail_text, conversion, condition)

    chosen_attribute = attributes[option]
    threshold = None
    if utils.is_continuous_attribute(chosen_attribute):
        text = "Choose the threshold on which the continuous attribute will be divided:\n\n"
        conversion = float
        threshold = utils.read_option(text, fail_text, conversion)

    return (chosen_attribute, threshold)
