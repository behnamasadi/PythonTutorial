#################################### Command Line Arguments ####################################

#example of call: python command_line_atgv.py -n=3
import sys
#print(sys.argv) #this will give us 


#################################### argparse ####################################
#https://docs.python.org/3/library/argparse.html#module-argparse
#The argparse module provides a mechanism to process command line arguments. It should always be preferred over directly processing sys.argv manually.


import argparse
parser = argparse.ArgumentParser(description='Some general help message regarding processing flags and command line arguments.')

# This will add a flag withou parameters, that means user may or may not provide -o
parser.add_argument("-o", action="store_true", help="-o is for option, user may or may not provide -o")
parser.add_argument('-f', '--file', required=False,  default="file.xml", help="path to xml")
args = parser.parse_args()

if args.o:
        print("options are given")

config_file = args.file
print(config_file)
