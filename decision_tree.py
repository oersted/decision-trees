import sys, getopt, csv
from algorithms.id3 import id3

def parse_opts():
    usage = (
        "decision_tree.py <inputfile> <target_attribute> [-o <outputfile>]\n"
        "decision_tree.py -h [<option>]\n"
    )
    input_file_path = ''
    target_attribute = ''
    output_file_path = ''

    try:
        opts, args = getopt.getopt(sys.argv, "o:")
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

    return (input_file_path, target_attribute, output_file_path)

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

def main():
    input_file_path, target_attribute, output_file_path = parse_opts()
    data, attributes = get_data(input_file_path)

    if attributes.count(target_attribute) != 1:
        sys.stderr.write("The target attribute doesn't exist.\n")
        sys.exit(2)

    attributes.remove(target_attribute)
    decision_tree = id3(data, target_attribute, attributes)

    decision_tree.export(output_file_path)

if __name__ == '__main__':
    main()
