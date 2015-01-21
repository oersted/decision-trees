import sys, getopt, csv
from algorithms.tree import DecisionTree
from algorithms.id3 import ID3Tree

def parse_opts():
    usage = "decision_tree.py <inputfile> <target_attribute> [-o <outputfile>]\n"
    input_file_path = ''
    target_attribute = ''
    output_file_path = ''
    manual_mode = False

    try:
        opts, args = getopt.getopt(sys.argv, "o:ma:")
        if len(args) == 3:
           input_file_path = args[1]
           target_attribute = args[2]
        else:
            raise getopt.GetoptError("You must provide exactly 2 positional arguments.")
    except getopt.GetoptError:
        sys.stderr.write(usage)
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-o':
                output_file_path = arg
            elif opt == 'm':
                manual_mode = True
            else:
                sys.stderr.write(usage)
                sys.exit(2)

    return (input_file_path, target_attribute, output_file_path, manual_mode)

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

def choose_algorithm(data, attributes, target_attribute):
    text = "Choose the next attribute that will be used as the pivot:\n"
    text += "\t1. Choose attribute manually.\n"
    text += "\t2. Continue with ID3."
    text += "\n"
    fail_text = "That's not an option.\n\n"
    conversion = int
    condition = lambda x: x in (1,2)
    option = DecisionTree.read_option(text, fail_text, conversion, condition)

    if option == 1:
        new_tree = DecisionTree()
        return (new_tree, new_tree.manual)
    if option == 2:
        new_tree = ID3Tree()
        return (new_tree, new_tree.id3)

def main():
    input_file_path, target_attrib, output_file_path, manual_mode = parse_opts()
    data, attribs = get_data(input_file_path)

    if attribs.count(target_attrib) != 1:
        sys.stderr.write("The target attribute doesn't exist.\n")
        sys.exit(2)
    attribs.remove(target_attrib)

    if manual_mode:
        tree, choose_attrib = choose_algorithm(data, attribs, target_attrib)
    else:
        tree = ID3Tree()
        choose_attrib = tree.id3

    loose_ends = tree.extend(data, attribs, target_attrib, choose_attrib)
    for loose_end in loose_ends:
        new_tree, new_data, new_attribs = loose_end
        loose_ends.append(tree.extend(new_data, new_attribs, target_attrib, choose_attrib))

    tree.render(output_file_path)

if __name__ == '__main__':
    main()
