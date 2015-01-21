import sys, getopt, csv
from collections import Counter
from algorithms.id3 import id3, ID3_Tree

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

def count_target_attrib_values(data, target_attribute):
    target_attrib_values = [record[target_attribute] for record in data]
    return Counter(target_attrib_values)

def manual(data, attributes, target_attribute, new_tree):
    id3_attribute, threshold = id3(data, attributes, target_attribute,
        target_atrib_counter, new_tree)

    while True:
        sys.stdout.write("Choose the next attribute that will be used as the pivot:\n")
        sys.stdout.write("\t1. Choose attribute manually.\n")
        sys.stdout.write("\t2. Continue with ID3: %s\n" % id3_attribute)
        sys.stdout.write("\n")

        option = sys.stdin.readline()
        try:
            option = int(option)
        except:
            pass
        else:
            if option in (1,2):
                break

    if option == 1:
        while True:
            sys.stdout.write("Choose the next attribute that will be used as the pivot:\n")
            for i in range(len(attributes)):
                sys.stdout.write("%d. %s" % (i, attributes[i]))
            sys.stdout.write("\n")

            option = sys.stdin.readline()
            try:
                option = int(option)
            except:
                pass
            else:
                if option in range(len(attributes)):
                    break

        chosen_attribute = attributes[option]
        threshold = None
        if chosen_attribute[0] == '*':
            while True:
                sys.stdout.write(("Choose the threshold on which the "
                    "continuous attribute will be divided:\n"))
                sys.stdout.write("\n")

                threshold = sys.stdin.readline()
                try:
                    threshold = float(threshold)
                except:
                    pass
                else:
                    break

        return (chosen_attribute, threshold)
    else:
        return (id3_attribute, threshold)

def main():
    input_file_path, target_attribute, output_file_path, manual_mode = parse_opts()
    data, attributes = get_data(input_file_path)

    if attributes.count(target_attribute) != 1:
        sys.stderr.write("The target attribute doesn't exist.\n")
        sys.exit(2)

    attributes.remove(target_attribute)
    decision_tree = ID3_Tree(target_attribute)
    next_call = [(data, attributes, decision_tree, lambda x, y: x == y)]
    for new_parameters in next_call:
        data, attributes, new_tree, rule = new_parameters

        target_attrib_counter = count_target_attrib_values(data, target_attribute)
        most_common = target_attrib_counter.most_common(1)[0]

        if manual_mode:
            chosen_attribute, threshold = manual(data, attributes, target_attribute,
                target_attrib_counter, new_tree)
        else:
            chosen_attribute, threshold = id3(data, attributes, target_attribute,
                target_attrib_counter, new_tree)

        ID3_Tree.extend(data, attributes, target_attribute, chosen_attribute,
            threshold, new_tree, most_common, rule)

    decision_tree.render(output_file_path)

if __name__ == '__main__':
    main()
