#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Expand shortened URLs present in a text file.

usage: expand_urls [-h] [-o OUTPUT] [-e ENCODING] [-v] input

positional arguments:
  input                 input file name

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name
  -e ENCODING, --encoding ENCODING
                        file encoding (default: utf-8)
  -v, --verbose         print expanded URLs
'''

from argparse import ArgumentParser
from os.path import basename, splitext
from re import findall

from requests import head
from requests.exceptions import ConnectionError

ENCODING = 'utf-8'

REGEX_URL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def expand_urls(input_name, output_name=None, encoding=ENCODING, verbose=False):
    '''
    Perform URL expansion.
    '''
    int_lines = 0
    dict_urls = {}
    set_urls  = set()

    if not output_name:
        name, ext = splitext(basename(input_name))
        output_name = name + '_EXPANDED' + ext

    print('Expanding URLs...')

    with open(input_name, 'rt', encoding=encoding, errors='ignore') as input_file:
        with open(output_name, 'w', newline='', encoding=encoding, errors='ignore') as output_file:
            for line in input_file:
                urls = findall(REGEX_URL, line)
                if urls:
                    for url in urls:
                        if url.count('.') == 1\
                        and url.split('.')[1].count('/') == 1:
                            expanded_url = url
                            if url not in set_urls:
                                try:
                                    expanded_url = head(url, allow_redirects=True).url
                                    print(url, '=>', expanded_url) if verbose else None
                                    dict_urls[url] = expanded_url
                                except ConnectionError:
                                    print('Warning: failed requesting URL "%s".' % url)
                                except Exception as e:
                                    print('Warning: %s.' % e)
                            if url in dict_urls:
                                line = line.replace(url, dict_urls[url])
                        set_urls.add(url)
                int_lines += 1
                output_file.write(line)
                print('Read %s lines.' % int_lines, end='\r')\
                if (int_lines/10000).is_integer() else None

    int_urls_total = len(set_urls)
    int_urls_short = len(dict_urls)

    print('\nRead', int_lines, 'total lines.\n'+
          str(int_urls_short), 'shortened URLs expanded.\n'+
          str(int_urls_total), 'total URLs in text.')

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument('input', action='store', help='input file name')
    parser.add_argument('-o', '--output', action='store', help='output file name')
    parser.add_argument('-e', '--encoding', action='store', help='file encoding (default: %s)' % ENCODING)
    parser.add_argument('-v', '--verbose', action='store_true', help='print expanded URLs')

    args = parser.parse_args()

    expand_urls(args.input,
                args.output,
                args.encoding,
                args.verbose)