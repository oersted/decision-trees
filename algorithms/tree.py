import sys

class Tree(object):
    def __init__(self, label = None):
        self.label = label
        self.children = {}
        self._write = None
        self._next_tree_number = 1

    def render(self, output_file_path=None):
        if output_file_path:
            f = open(output_file_path, 'w')
            self._write = f.write
        else:
            self._write = sys.stdout.write

        self._render(self, '')
        self._next_tree_number = 1

        if output_file_path:
            f.close()

    def _render(self, tree, indent):
        if len(tree.children) == 0:
            self._write(tree.label + '\n')
        else:
            self._write(tree.label + ' <' + str(self._next_tree_number) + '>'+ '\n')
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

    @classmethod
    def extend(data, attributes, target_attribute, chosen_attribute, threshold,
        tree, most_common, rule = lambda x, y: x == y):
        next_call = []
        data = [record for record in data if rule(record[chosen_attribute], option)]

        attributes = attributes[:]
        new_attributes.remove(chosen_attribute)

        tree.label(chosen_attribute)
        new_tree = ID3_Tree()

        if not data or len(attributes) == 0 or most_common[1] == len(target_attrib_values):
            tree.label = most_common[0]
        else:
            if threshold != None:
                option = chosen_attribute[1:5] + ' <= ' + str(threshold)
                tree.children[option] = new_tree
                rule = lambda x, y: float(x) <= threshold
                next_call.append((data, attributes, new_tree, rule))

                option = chosen_attribute[1:5] + ' > ' + str(threshold)
                tree.children[option] = new_tree
                rule = lambda x, y: float(x) > threshold
                next_call.append((data, attributes, new_tree, rule))
            else:
                # conversion to set used to remove duplicates
                chosen_attribute_options = list(set(
                    [record[chosen_attribute] for record in data]))
                for option in best_attribute_options:
                    next_call.append((data, attributes, new_tree))

        return next_call
