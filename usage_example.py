import argparse

from git_diff_lines import git_diff_lines
from pprint import pprint

parser = argparse.ArgumentParser(description='Get the lines of the given diff - example')
parser.add_argument('path', help='path to the git repo')
parser.add_argument('compared_to', help='git diff <<compared_to>>')
args = parser.parse_args()

pprint(git_diff_lines(compared_to=args.compared_to, path_to_repo=args.path))