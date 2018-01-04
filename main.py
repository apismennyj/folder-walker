import argparse
import os
import re
from pprint import pprint as pp
import csv
from utils import files_lookup


parser = argparse.ArgumentParser(
    description='The program gets a root folder (a positional command line parameter) and walks down the folder and for'
                ' each file and folder under this folder it stores its name, modification time and a MD5 checksum.'
                ' On the second run, without --init flag specify a folder name under the original root folder and the '
                'program should find all the occurrences of the given folder name and list all changes under this '
                'folder (print modified, removed, added).')

parser.add_argument('source_folder', help='Folder to start lookup routine')
parser.add_argument('--init', dest='init', action='store_const',
                    const=True,
                    help='Flag to start initial run, will clear ')

args = parser.parse_args()

is_initial_run = args.init
source_folder = os.path.abspath(args.source_folder.rstrip())

files_lookup(source_folder, is_initial_run)
