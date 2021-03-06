from algorithms.base import DecisionTree
from algorithms import utils
import sys, csv, getopt

def parse_opts():
    usage = ("use_decision_tree.py [-m <datafile>] [-t <target>] [-v] <inputfile>\n"
        "  -m     process multiple data records stored in <datafile>\n"
        "  -t     <target> will be used to refer to the target attribute instead of 'Result'\n"
        "  -v     show graphic representation of decision tree\n")
    input_file_path = None
    data_file_path = None
    target_attribute = None
    verbose = False

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "m:t:v")
        if len(args) == 1:
           input_file_path = args[0]
        else:
            raise getopt.GetoptError("You must provide exactly 1 positional argument.\n")
    except getopt.GetoptError as e:
        sys.stderr.write(str(e))
        sys.stderr.write(usage)
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-m':
                data_file_path = arg
            elif opt == '-t':
                target_attribute = arg
            elif opt == '-v':
                verbose = True
            else:
                sys.stderr.write(usage)
                sys.exit(2)

    return (input_file_path, data_file_path, target_attribute, verbose)

def process_data_file(data_file_path, tree, target_attribute):
    try:
        f = open(data_file_path, 'r')
    except:
        sys.stderr.write("The data file couldn't be opened.\n")
        sys.exit(2)
    else:
        reader = csv.reader(f)

        try:
            header = next(reader)
        except:
            sys.stderr.write("Empty data file.\n")
            sys.exit(2)

        target_name = "Result"
        if target_attribute:
            target_name = target_attribute

        data = []
        for row in reader:
            record = {}
            for i in range(len(header)):
                record[header[i]] = row[i]

            result = tree.use(record.copy())
            if len(result.children) != 0:
                sys.stderr.write("Not enough data.\n")
                sys.exit(2)
            else:
                record[target_name] = result.label
                data.append(record)
        f.close()

        try:
            f = open(data_file_path, 'w')
        except:
            sys.stderr.write("Couldn't write into the data file.\n")
            sys.exit(2)
        else:
            writer = csv.writer(f)

            header.append(target_name)
            writer.writerow(header)

            for record in data:
                row = [None] * len(header)
                for i in range(len(header)):
                    row[i] = record[header[i]]
                writer.writerow(row)
            f.close()

def main():
    input_file_path, data_file_path, target_attribute, verbose = parse_opts()
    tree = DecisionTree()
    tree.load(input_file_path)
    if verbose:
        sys.stdout.write(str(tree))
    if data_file_path:
        process_data_file(data_file_path, tree, target_attribute)
    else:
        utils.manual_use(tree, target_attribute)

if __name__ == '__main__':
    main()