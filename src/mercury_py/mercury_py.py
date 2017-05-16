#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from builtins import input

import sys
import csv
import json
import argparse

def filter_data_from_dict(json_data, fil):
    cleaned_data = ''
    if 'hash_type' in fil and fil['hash_type'] == 'int':
        cleaned_data = json_data[int(fil['name'])]
    if 'content_type' in fil and fil['content_type'] == 'int':
        cleaned_data = int(cleaned_data)
    return cleaned_data

def filter_data_from_list(json_data, filters):
    for fil in filters:
        if type(fil) is str or type(fil) is unicode:
            json_data = json_data[fil]
        elif type(fil) is dict:
            json_data = filter_data_from_dict(json_data, fil)
        elif type(fil) is list:
            json_data = filter_data_from_list(json_data, fil)
    return json_data

def extract_data_against_filter(raw_data, rules):
    cleaned_data = []
    parsed_json = json.loads(raw_data)
    if 'entry_point' in rules:
        parsed_json = filter_data_from_list(parsed_json, rules['entry_point'])
    for fil in rules['filter']:
        json_data = parsed_json
        if type(fil) is str or type(fil) is unicode:
            json_data = json_data[fil]
        elif type(fil) is dict:
            json_data = filter_data_from_dict(json_data, fil)
        elif type(fil) is list:
            json_data = filter_data_from_list(json_data, fil)
        cleaned_data.append(json_data)
    return cleaned_data

def read_csv(csv_path, delimiter, rules):
    cleaned_csv = []
    with open(csv_path, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter)
        reader.next()
        for row in reader:
            partial = []
            for key, rule in list(rules.items()):
                raw_data = row[int(key)]
                partial += extract_data_against_filter(raw_data, rule)
            cleaned_csv.append(partial)
    return cleaned_csv

def read_rule(rule_path):
    rules = []
    column_names = []
    with open(rule_path) as json_file:
        json_rules = json.load(json_file)
        rules = json_rules['rules']
        column_names = json_rules['column_names']
    return rules, column_names

def export_to_csv_file(csv_list, export_path):
    with open(export_path, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(csv_list)

def mercury_py():
    parser = argparse.ArgumentParser(description='Export JSON to CSV', prog='mercury-py')
    parser.add_argument('--csv', help='Path of csv file', default='example_csv.csv', action='store')
    parser.add_argument('--csv-delimiter', help='delimiter', default=',', action='store')
    parser.add_argument('--rule', help='JSON rule to extract json inside your csv file', default='example_rule.json', action='store')
    parser.add_argument('--export', help='Where you want to store exported data', default='exported_json.csv', action='store')

    args = vars(parser.parse_args())
    csv_path = args['csv']
    rule_path = args['rule']
    export_path = args['export']
    delimiter = str(args['csv_delimiter']).encode('utf-8')

    if not csv_path:
        csv_path = input('CSV File Path: ')

    if not rule_path:
        rule_path = input('JSON Rule File Path: ')

    if csv_path == '' or rule_path == '':
        print('Please enter csv path and rule path')
        sys.exit(1)

    rules, column_names = read_rule(rule_path)
    cleaned_csv = read_csv(csv_path, delimiter, rules)
    cleaned_csv.insert(0, column_names)
    export_to_csv_file(cleaned_csv, export_path)

if __name__ == '__main__':
    mercury_py()
