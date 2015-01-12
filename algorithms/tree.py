import sys

class Tree(object):
    def __init__(self):
        self.label = ""
        self.children = {}
        self._write = None
        self._next_tree_number = 1

    def export(self, output_file_path):
        if output_file_path:
            f = open(output_file_path, 'w')
            self._write = f.write
        else:
            self._write = sys.stdout.write

        self._export(self, '')
        self._next_tree_number = 1

        if output_file_path:
            f.close()

    def _export(self, tree, indent):
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
	        	self._export(tree.children[option], new_indent)