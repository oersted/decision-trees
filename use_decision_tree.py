from algorithms.base import DecisionTree
import sys

def parse_opts():
    usage = "use_decision_tree.py <inputfile>\n"
    input_file_path = None

    if len(sys.argv) == 2:
        input_file_path = sys.argv[1]
    else:
        sys.stderr.write(usage)
        sys.exit(2)

    return input_file_path

def main():
    input_file_path = parse_opts()
    tree = DecisionTree()
    tree.load(input_file_path)
    tree.use()

if __name__ == '__main__':
    main()