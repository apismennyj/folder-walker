import argparse
import os
import re
from pprint import pprint as pp
import hashlib
import sys
import time
from datetime import datetime
from elasticsearch import Elasticsearch
import json
from pprint import pprint
from elasticsearch.exceptions import NotFoundError

ELASTIC = {
    'host': 'localhost',
    'port': 9200,
    'index': 'folder-walker',
    'doc_type': 'files'
}

es = Elasticsearch([{'host': ELASTIC['host'], 'port': ELASTIC['port']}])


def colored(str, color):
    colors = {
        'red': '\033[1;31m',
        'blue': '\033[1;34m',
        'cyan': '\033[1;36m',
        'green': '\033[0;32m',
        'reset': '\033[0;0m',
        'bold': '\033[;1m',
        'reverse': '\033[;7m'
    }

    return "{}{}{}".format(colors.get(color, 'reset'), str, colors['reset'])


def files_lookup(parent_folder, is_init):
    if not os.path.exists(parent_folder):
        print('Folder {} does not exists'.format(parent_folder))
        return False

    if is_init:
        for current_directory in os.walk(parent_folder):

            print("\n{} (Files count: {}) :\n".format(current_directory[0], len(current_directory[2])))

            for current_file in current_directory[2]:

                complete_file_path = os.path.join(current_directory[0], current_file)
                modification_time_raw = os.path.getmtime(complete_file_path)
                modification_time_readable = datetime.fromtimestamp(modification_time_raw).__str__()

                if os.access(complete_file_path, os.R_OK):
                    md5_hash = hashlib.md5(open(complete_file_path, 'rb').read()).hexdigest()
                else:
                    md5_hash = colored("File isn't readable", 'red')

                print("{:<35}{:<21}{}".format(current_file, modification_time_readable, md5_hash))
                es.indices.delete(index=ELASTIC['index'], ignore=[400, 404])
                es.index(index="test-index", doc_type='files', id=complete_file_path,
                         body={'name': current_file,
                               'path': complete_file_path,
                               'mtime': modification_time_readable,
                               'hash': md5_hash})
    else:
        for current_directory in os.walk(parent_folder):

            print("\n{} (Files count: {}) :\n".format(current_directory[0], len(current_directory[2])))

            for current_file in current_directory[2]:

                complete_file_path = os.path.join(current_directory[0], current_file)
                modification_time_raw = os.path.getmtime(complete_file_path)
                modification_time_readable = datetime.fromtimestamp(modification_time_raw).__str__()

                if os.access(complete_file_path, os.R_OK):
                    md5_hash = hashlib.md5(open(complete_file_path, 'rb').read()).hexdigest()
                else:
                    md5_hash = colored("File isn't readable", 'red')

                print(colored(complete_file_path, 'cyan'))

                # First thing - try to get existing file from ES
                try:
                    # result = es.get(index='test-index', doc_type='files', id=complete_file_path)
                    result = es.search(index='test-index', body={"query": {"term": {"path": complete_file_path}}})
                except NotFoundError:
                    print("{:<20} {:<35}{:<21}{}".format(colored('ADDED', 'green'), current_file,
                                                         modification_time_readable, md5_hash))
                else:
                    # result = es.search(index="test-index", body={"query": {"match": {'name': current_file, 'path': complete_file_path, 'mtime': modification_time_readable, 'hash': md5_hash}}})
                    print(result)
                    result = es.search(index="test-index", body={"query": {"multi_match": {"fields": ['_all'],
                                                                                           "query": complete_file_path + modification_time_readable + md5_hash,
                                                                                           "fuzziness": "AUTO"
                                                                                           }
                                                                           }
                                                                 })
                    # pprint(result)
                    pass
                    # pprint('result')
                    # pprint(result)

                # result = es.get(index='test-index', doc_type='files', id=complete_file_path)

    return True
