import sys, getopt, csv
from algorithms.tree import DecisionTree
from algorithms.id3 import ID3Tree
import xml.etree.ElementTree as ET

def parse_opts():
    usage = ("decision_tree.py [OPTION]... [-o <outputfile>] [-s <savefile>]"
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
    gain_rate = False
    use = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:muc:rs:")
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
                ID3Tree.use_gain_ratio = True
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
    finally:
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
            costs[attribute_names[i]] = attribute_costs[i]
    finally:
        f.close()

    ID3Tree.use_costs = True
    ID3Tree.attribute_costs = costs


def choose_algorithm(data, attributes, target_attribute):
    text = "Choose the next attribute that will be used as the pivot (***):\n"
    text += "\t1. Choose attribute manually.\n"
    text += "\t2. Continue with ID3."
    text += "\n"
    fail_text = "That's not an option.\n\n"
    conversion = int
    condition = lambda x: x in (1,2)
    option = DecisionTree.read_option(text, fail_text, conversion, condition)

    if option == 1:
        return 'manual'
    if option == 2:
        return 'id3'

def main():
    input_file_path, target_attrib, output_file_path, save_file_path, costs_file, manual_mode, use = parse_opts()
    data, attribs = get_data(input_file_path)

    if costs_file is not None:
       get_costs(costs_file)

    if attribs.count(target_attrib) != 1:
        sys.stderr.write("The target attribute doesn't exist.\n")
        sys.exit(2)
    attribs.remove(target_attrib)

    tree = ID3Tree()
    if manual_mode:
        choose_attrib = choose_algorithm(data, attribs, target_attrib)
    else:
        choose_attrib = 'id3'

    loose_ends = tree.extend(data, attribs, target_attrib, getattr(tree, choose_attrib))
    while len(loose_ends) > 0:
        new_tree, new_data, new_attribs = loose_ends.pop()
        if manual_mode:
            tree.render()
            choose_attrib = choose_algorithm(data, attribs, target_attrib)
        loose_ends.extend(new_tree.extend(
            new_data, new_attribs, target_attrib, getattr(new_tree, choose_attrib)))

    tree.render(output_file_path)

    if save_file_path:
        tree.save(save_file_path)

    if use:
        tree.use()

if __name__ == '__main__':
    main()
