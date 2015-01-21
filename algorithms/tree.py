from collections import Counter, deque
import xml.etree.ElementTree as ET
import sys

class DecisionTree(object):
    def __init__(self, label = None):
        self.label = label
        self.children = {}
        self._write = None
        self._next_tree_number = 1

    def extend(self, data, attribs, target_attrib, choose_attrib):
        loose_ends = deque()
        target_attrib_values = [record[target_attrib] for record in data]
        target_attrib_counter = Counter(target_attrib_values)
        most_common = target_attrib_counter.most_common(1)[0]

        if not data or len(attribs) == 0 or most_common[1] == len(target_attrib_values):
            self.label = most_common[0]
        else:
            chosen_attrib, threshold = choose_attrib(
                data, attribs, target_attrib, target_attrib_counter)
            self.label = chosen_attrib

            if threshold:
                option = chosen_attrib[1:5] + ' <= ' + str(threshold)
                new_tree = self.__class__()
                self.children[option] = new_tree
                rule = lambda x, y: float(x) <= threshold
                new_data, new_attribs = self._create_new_params(data, attribs, chosen_attrib, option, rule)
                loose_ends.append((new_tree, new_data, new_attribs))

                option = chosen_attrib[1:5] + ' > ' + str(threshold)
                new_tree = self.__class__()
                self.children[option] = new_tree
                rule = lambda x, y: float(x) > threshold
                new_data, new_attribs = self._create_new_params(data, attribs, chosen_attrib, option, rule)
                loose_ends.append((new_tree, new_data, new_attribs))
            else:
                # conversion to set used to remove duplicates
                chosen_attrib_options = list(set([record[chosen_attrib] for record in data]))
                for option in chosen_attrib_options:
                    new_tree = self.__class__()
                    self.children[option] = new_tree
                    new_data, new_attribs = self._create_new_params(
                        data, attribs, chosen_attrib, option)
                    loose_ends.append((new_tree, new_data, new_attribs))

        return loose_ends

    def _create_new_params(self, data, attribs, chosen_attrib, option, rule = lambda x, y: x == y):
        new_data = [record for record in data if rule(record[chosen_attrib], option)]
        new_attribs = attribs[:]
        new_attribs.remove(chosen_attrib)

        return (new_data, new_attribs)

    def _is_continuous_attribute(self, attribute):
        return attribute[0] == '*'

    def manual(self, data, attributes, target_attribute, target_attrib_counter):
        text = "Choose the next attribute that will be used as the pivot:\n"
        for i in range(len(attributes)):
            text += "\t%d. %s\n" % (i, attributes[i])
        text += "\n"
        fail_text = "That's not an option.\n\n"
        conversion = int
        attribs_range = range(len(attributes))
        condition = lambda x: x in attribs_range
        option = self.__class__.read_option(text, fail_text, conversion, condition)

        chosen_attribute = attributes[option]
        threshold = None
        if self._is_continuous_attribute(chosen_attribute):
            text = "Choose the threshold on which the continuous attribute will be divided:\n\n"
            conversion = float
            threshold = self.__class__.read_option(text, fail_text, conversion)

        return (chosen_attribute, threshold)

    @classmethod
    def read_option(self, text = None, fail_text = None, conversion = None, condition = None):
        while True:
            if text:
                sys.stdout.write(text)
            option = sys.stdin.readline()
            if conversion:
                try:
                    option = conversion(option)
                except:
                    if fail_text:
                        sys.stdout.write(fail_text)
                else:
                    if condition:
                        if condition(option):
                            break
                        else:
                            if fail_text:
                                sys.stdout.write(fail_text)
                    else:
                        break

        return option

    def use(self):
        if len(self.children) == 0:
            sys.stdout.write("\nResult: " + self.label + '\n')
        else:
            attrib = self.label
            text = "\nGive the value of attribute %s:\n" % attrib
            fail_text = "Not a valid value.\n"
            if self._is_continuous_attribute(attrib):
                conversion = float
            else:
                conversion = str
            condition = lambda key: key in self.children
            value = self.__class__.read_option(text, fail_text, conversion)
            if type(value) == str:
                value = value.strip('\n')

            if self._is_continuous_attribute(attrib):
                # There will always be only 2 children
                options = self.children.keys()
                if ' <= ' in options[0]:
                    threshold = float(option[0].split(' <= ')[1])
                    if value <= threshold:
                        self.children[options[0]].use()
                    else:
                        self.children[option[1]].use()
                else:
                    threshold = float(option[1].split(' <= ')[1])
                    if value <= threshold:
                        self.children[options[1]].use()
                    else:
                        self.children[option[0]].use()
            else:
                self.children[value].use()

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

    def render(self, output_file_path=None):
        if output_file_path:
            f = open(output_file_path, 'w')
            self._write = f.write
        else:
            self._write = sys.stdout.write

        self._render(self, '')
        self._next_tree_number = 1

    def _render(self, tree, indent):
        if len(tree.children) == 0:
            if tree.label:
                self._write(tree.label + '\n')
            else:
                self._write('(***)\n')
        else:
            if tree.label:
                self._write(tree.label + ' <' + str(self._next_tree_number) + '>'+ '\n')
            else:
                self._write('(***) <' + str(self._next_tree_number) + '>'+ '\n')
            self._next_tree_number += 1

            count = len(tree.children) - 1
            for option in tree.children:
                self._write(indent)
                if count == 0:
                    self._write('\\-')
                    new_indent = indent + (len(option)+5)*' '
                else:
                    self._write('|-')
                    new_indent = indent + '|' + (len(option)+4)*' '

                self._write(option + '-->')

                count -= 1
                self._render(tree.children[option], new_indent)