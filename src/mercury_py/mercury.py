#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from builtins import str
from builtins import int
from builtins import input

import sys
import csv
import json
import argparse

global rule
global clean_csv = []

def filter_data_from_object(json_data, fil):
    cleaned_data = ''
    if (fil['name'] in json_data) and ('hash_type' in fil):
        if fil['hash_type'] == 'int':
            cleaned_data = json_data[int(fil['name'])]
        if (fil['content_type'] == 'int') and (cleaned_data != ''):
            cleaned_data = int(cleaned_data)
    return cleaned_data

def filter_data_from_list(json_data, filters):
    cleaned_data = ''
    for fil in filters:
        if type(fil) == str:
            cleaned_data = json_data[fil]
        else if type(fil) == dict:
            cleaned_data = filter_data_from_object(json_data, fil)
        else if type(fil) == list:
            cleaned_data = filter_data_from_list(json_data, fil)
    return cleaned_data

def extract_data_against_filter(raw_data, fil):
    cleaned_data = []
    parsed_json = json.loads(raw_data)
    for value in list(fil.items()):
        cleaned_data.append(filter_data_from_list(parsed_json, [value]))

def read_csv(csv_path):
    with open(csv_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        reader.next()
        for key, value in list(rule.items()):
            for row in reader:
                raw_data = row[int(key)]
                clean_csv.append(extract_data_against_filter(raw_data, value))

def read_rule(rule_path):
    with open(rule_path) as json_file:
        rule = json.load(json_file)

def export_to_csv_file(csv_list, export_path):
    with open(export_path, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(csv_list)

def main():
    parser = argparse.ArgumentParser(description='Export JSON to CSV', prog='mercury-py')
    parser.add_argument('--csv', help='Path of csv file', default=None, action='store')
    parser.add_argument('--rule', help='JSON rule to extract json inside your csv file', default=None, action='store')
    parser.add_argument('--export', help='Where you want to store exported data', default=None, action='store')

    args = vars(parser.parse_args())
    csv_path = args['csv']
    rule_path = args['rule']
    export_path = args['export']

    if not csv_path:
        csv_path = input('CSV File Path: ')

    if not rule_path:
        rule_path = input('JSON Rule File Path: ')

    if not export_path:
        export_path = 'exported_json.csv'

    if csv_path == '' or rule_path == '':
        print('Please enter csv path and rule path')
        sys.exit(1)

    read_rule(rule_path)
    read_csv(csv_path)
    export_to_csv_file(clean_csv, export_path):

if __name__ == '__main__':
    main()
