SHORT GUIDE
~~~~~~~~~~~
create_decision_tree.py [OPTION]... [-o <outputfile>] [-s <savefile>]
                        [-c <costs_file>] [-m] [-r] [-u]
                        <inputfile> <target_attribute>
                        
  -o     use <outputfile> instead stdin
  -s     save resulting tree in <savefile> as XML
  -c     take into account attribute costs in <costs_file> to select
         the best attribute
  -m     use manual mode
  -r     use gain ratio value instead of gain only to select the best
         attribute
  -u     use decision tree after creating it


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
use_decision_tree.py [-m <datafile>] [-t <target>] [-v] <inputfile>
  -m     process multiple data records stored in <datafile>
  -t     <target> will be used to refer to the target attribute instead
         of 'Result'
  -v     show graphic representation of decision tree


INTRODUCTION
~~~~~~~~~~~~
This program makes decision trees based in the provided data using for
that purpose the ID3 algorithm with some extras.


create_decision_tree.py
~~~~~~~~~~~~~~~~~~~~~~~

GENERAL USAGE
~~~~~~~~~~~~~
This program takes as parameter the <inputfile> and the 
<target_attribute>. The first one have to be a csv file, with the name 
of the attributes in the first line, and the values of this attributes 
in the next lines. The second parameter should be the name of one of 
the attributes in the <inputfile>.

One of the most important extras added to the ID3 algorithm is the 
capability to work with continuous values for the attributes. In order 
the application to know that the values of a given attribute should be 
interpreted as continuous placing a '*' before the attribute name in 
<inputfile> is necessary. The target attribute may be also a
continuous value, but in this case it would be necessary also to write 
the '*' before <target_attribute> when executing the command (remember 
that in Linux command line '*' has a special meaning and that it 
should be escaped using '\' or giving the full parameter between
quotes). 

OPTIONS
~~~~~~~
-o  this parameter redirects the standard output to the given
    <outputfile>.
  
-s  this parameter causes the created tree to be saved in a XML file 
    <savefile>, allowing using it later to make decisions with the 
    use_decision_tree.py program.
    
-c  this parametere activates an extra feature of the ID3 algorithm 
    which consists on taking into account not only the information gain
    but also the attribute cost when computing the tree. This can cause
    a complete tree transformation in some cases.
    
    The cost of each attribute would be read from the <costs_file>. 
    This file would be also a csv file, with attribute names in the 
    first line and costs in the second one.
    
-m  this parameters causes the program to enter in manual mode. In 
    this mode the user would be asked to select to continue with the 
    selected value or to use a custom one in each step of the tree 
    creation process.
    
    In any step of the process the user would be allowed to end the 
    manual mode, allowing the algorithm to generate the remining tree 
    automatically.
    
-r  this parameter causes to use information relation value to compute 
    the best parameter instead of using only the information gain.
    
    Information relation is more appropriate in some cases as it takes 
    into account not only the information gain for a given attribute, 
    but also the information needed to chose one value between all the 
    possible values for the attribute. That is why it can be more 
    accurate in some situations.
    
-u  when provided with this parameter instead of ending when the tree 
    is generated the program will allow to use the created tree like 
    when use_decision_tree.py is invoked.

use_decision_tree.py
~~~~~~~~~~~~~~~~~~~~

GENERAL USAGE
~~~~~~~~~~~~~

This program allow to use the stored XML trees to make decisions. It
adds some extra functionalities to the -u parameter of
create_decision_tree.py.

The main extra functionality is allowing to test the tree with many 
data groups automatically. The data must be provided also in csv 
files. Each line represents an independent group of data, and the 
result will be append in the same line after all the entries. 

OPTIONS
~~~~~~~
 
-m  this option activates the extra functionality an expects <datafile>
    csv file as parameter.

-t  changes the name of the Result column in the <datafile>. If this 
    parameter is not specified "Result" will be used instead.
    
-v  it causes the program to print the decision tree in the standard
    output.
