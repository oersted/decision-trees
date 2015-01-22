import sys, getopt, csv
from algorithms import base
from algorithms import id3
from algorithms import utils
import xml.etree.ElementTree as ET
from math import log10, floor, ceil

def parse_opts():
    usage = ("decision_tree.py [OPTION]... [-o <outputfile>] [-s <savefile>] "
        "[-c <costs_file>] [-m] [-r] [-u] <inputfile> <target_attribute>\n"
        "  -o     use <outputfile> instead stdin\n"
        "  -s     save resulting tree in <savefile> as XML\n"
        "  -c     take into account attribute costs in <costs_file> to select the best attribute\n"
        "  -m     use manual mode\n"
        "  -r     use gain ratio value instead of gain only to select the best attribute\n"
        "  -u     use decision tree after creating it\n")
    input_file_path = ''
    target_attribute = ''
    output_file_path = ''
    save_file_path = None
    costs_file = None
    manual_mode = False
    use = False

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "o:muc:rs:")
        if len(args) == 2:
           input_file_path = args[0]
           target_attribute = args[1]
        else:
            raise getopt.GetoptError("You must provide exactly 2 positional arguments.")
    except getopt.GetoptError:
        sys.stderr.write(usage)
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-o':
                output_file_path = arg
            elif opt == '-m':
                manual_mode = True
            elif opt == '-s':
                save_file_path = arg
            elif opt == '-u':
                use = True
            elif opt == '-c':
                costs_file = arg
            elif opt == '-r':
                # TODO
                pass
            else:
                sys.stderr.write(usage)
                sys.exit(2)

    return (input_file_path, target_attribute, output_file_path, save_file_path, costs_file,
        manual_mode, use)

def get_data(input_file_path):
    data = []

    try:
        f = open(input_file_path, 'r')
    except:
        sys.stderr.write("The input file couln't be opened.\n")
        sys.exit(2)
    else:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            record = {}
            for i in range(len(header)):
                record[header[i]] = row[i]
            data.append(record)
        f.close()

    return (data, header)

def get_costs(file_name):
    costs = {}
    try:
        f = open(file_name, 'r')
    except:
        sys.stderr.write("The costs file couln't be opened.\n")
        sys.exit(2)
    else:
        reader = csv.reader(f)
        attribute_names = next(reader)
        attribute_costs = next(reader)
        for i in range(len(attribute_names)):
            try:
                costs[attribute_names[i]] = float(attribute_costs[i])
            except ValueError:
                    sys.stderr.write("The costs file data is not valid.\n")
                    sys.exit(2)
        f.close()

    ID3Tree.use_costs = True
    ID3Tree.attribute_costs = costs


def get_algorithm(data, attributes, target_attribute):
    text = "\nChoose the next attribute that will be used as the pivot:\n"
    text += "\t1. Choose attribute manually.\n"
    text += "\t2. Use ID3.\n"
    text += "\t3. Continue with ID3.\n"
    text += "\n"
    fail_text = "That's not an option.\n\n"
    conversion = int
    condition = lambda x: x in (1,2,3)
    option = utils.read_option(text, fail_text, conversion, condition)

    if option == 1:
        return (base.choose_attribute, base.DecisionTree, True)
    elif option == 2:
        return (id3.choose_attribute, id3.ID3Tree, True)
    elif option == 3:
        return (id3.choose_attribute, id3.ID3Tree, False)

def render(tree, output_file_path = None):
    if output_file_path:
        f = open(output_file_path, 'w')
        f.write(str(tree))
        f.close()
    else:
        sys.stdout.write(str(tree))

def process_continous_target_attrib(data, target_attrib):
    data.sort(key=lambda record: float(record[target_attrib]))
    group_count = 1 + 3.322 * log10(len(data)) # Struges
    max_value = int(ceil(float(data[-1][target_attrib])))
    min_value = int(floor(float(data[0][target_attrib])))
    target_range = max_value - min_value
    range_width = int(target_range/group_count)

    i = 0
    for r in range(min_value, max_value, range_width):
        while i < len(data) and r <= float(data[i][target_attrib]) < r + range_width:
            data[i][target_attrib] = '(%d,%d)' % (r, r + range_width)
            i += 1

    return data

def main():
    input_file_path, target_attrib, output_file_path, save_file_path, costs_file, manual_mode, use = parse_opts()
    data, attribs = get_data(input_file_path)

    if costs_file is not None:
       get_costs(costs_file)

    if attribs.count(target_attrib) != 1:
        sys.stderr.write("The target attribute doesn't exist.\n")
        sys.exit(2)
    attribs.remove(target_attrib)

    if utils.is_continuous_attribute(target_attrib):
        process_continous_target_attrib(data, target_attrib)

    if manual_mode:
        choose_attribute, tree_type, manual_mode = get_algorithm(data, attribs, target_attrib)
    else:
        choose_attribute = id3.choose_attribute
        tree_type = id3.ID3Tree

    tree = tree_type()
    loose_ends = tree.first_extend(data, attribs, target_attrib, choose_attribute)
    while len(loose_ends) > 0:
        parent, option, new_tree, new_data, new_attribs, counter = loose_ends.pop()
        if manual_mode:
            new_tree.label += ' <--'
            render(tree)
            choose_attribute, tree_type, manual_mode = get_algorithm(data, attribs, target_attrib)
        if not isinstance(new_tree, tree_type):
            new_tree = tree_type(new_tree.label)
            parent.children[option] = new_tree
        loose_ends.extend(new_tree.extend(
            new_data, new_attribs, target_attrib, counter, choose_attribute))
    render(tree, output_file_path)

    if save_file_path:
        tree.save(save_file_path)

    if use:
        tree.use()

if __name__ == '__main__':
    main()
