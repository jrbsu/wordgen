import argparse

parser = argparse.ArgumentParser(description="Word database generator",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--force", action="store_true", help="force an update even if there is no change")
parser.add_argument("-l", "--local", action="store_true", help="use local TSV file for debugging purposes")
parser.add_argument("-q", "--quick", action="store_true", help="quick mode - only update new words")
args = vars(parser.parse_args())
force = args["force"]
local = args["local"]
quick = args["quick"]

'''
These currently do nothing.

parser.add_argument("-v", "--verbose", action="store_true", help="verbose mode")
verbose = args["verbose"]
'''