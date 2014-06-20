from myraid.parser import Parser
from rply import ParsingError
from rpython.rlib import rstring
import sys
import os
import re
from myraid.memory.memory import stack
from myraid import compiler
def run(filename, name):
	codes = [];
	while True:
		read = os.read(filename, 4096);
		if len(read) == 0:
			break
		codes += read
	os.close(filename)
	contents = ""
	for line in codes:
		contents  = contents + line;
	codes = contents;
	codes = codes.split("\n");
	_codes = [];
	for function in codes:
		if function:
			_codes.append(function);
	print _codes;		
	i = 0;
	for line in _codes:
		i+=1;
		#try:
		Parser._parse(line);
	compiler.Compiler.compile(None, stack);	
		#except Exception as e:
		#	print "A problem occured parsing line", str(i), '"'+line+'".';

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1
    try:
        run(os.open(filename, os.O_RDONLY, 0777), filename)
    except OSError:
        print "Could not open file. Reason: Non existent file"
    return 0

def target(*args):
    return entry_point, None;

if __name__ == "__main__":
    entry_point(sys.argv)
