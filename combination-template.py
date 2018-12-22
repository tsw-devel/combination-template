#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import string
import re
import json
import itertools
from argparse import ArgumentParser
from collections import OrderedDict

import chardet
import jinja2

REQUIREMENTS_KEYS = ('template', 'data', 'output')

def get_line_feed_code(path):
    with open(path, mode='rb') as f:
        rawdata = f.read()
        if b'\r\n' in rawdata:
            return '\r\n'
        else:
            return '\n'


def get_encoding(path):
    with open(path, mode='rb') as f:
        dat = chardet.detect(f.read())
    return dat['encoding']


def check_requirement_keys(keys):
    for i in REQUIREMENTS_KEYS:
        if not i in keys:
            print('{} Not found'.format(i))
            return False
    return True


def check_option_keys(key, reg_str, dict_dat):
    if key in dict_dat.keys():
        p = re.compile(reg_str, re.IGNORECASE)
        if p.match(dict_dat[key]) != None:
            return True
    return False


def get_j2env():
    j2env = jinja2.Environment()
    j2env.trim_blocks = True
    j2env.lstrip_blocks = True
    return j2env

def generate(json_path, verbose=False):
    auto_increment_id = False
    try:
        with open(json_path, 'r') as f:
            json_odict = json.load(f, object_pairs_hook=OrderedDict)
    except OSError:
        return 1

    if not check_requirement_keys(json_odict.keys()):
        return 1

    template_path = json_odict['template']
    insertion_dict = json_odict['data']
    output_dir = json_odict['output']
    is_jinja2 = check_option_keys('format', 'jinja2|j2|jinja',  json_odict)
    if 'auto_id' in json_odict.keys() and isinstance(json_odict['auto_id'], bool):
        auto_increment_id = True

    try:
        encoding = get_encoding(template_path)
        line_feed_code = get_line_feed_code(template_path)
        with open(template_path, encoding=encoding) as fr:
            if is_jinja2:
                j2env = get_j2env()
                tmpl = j2env.from_string(fr.read())
            else:
                tmpl = string.Template(fr.read())
    except (OSError, TypeError):
        print('Not found template file {}'.format(template_path))
        return 1
    except jinja2.exceptions.TemplateSyntaxError:
        print('Jinja2 syntax error {}'.format(template_path))
        return 1

    data_list = []
    for i in insertion_dict.values():
        if not isinstance(i, list):
            data = []
            data.append(i)
        else:
            data = i
        data_list.append(data)

    product_elems = tuple(itertools.product(*data_list))
    product_keys = tuple(insertion_dict.keys())
    product_digit = len(str(len(product_elems)))
    error_occur = False
    create_id = 0
    for product_elem in product_elems:
        product_elem_dict = OrderedDict(zip(product_keys , product_elem))
        if is_jinja2:
            gen = tmpl.render(product_elem_dict)
        else:
            gen = tmpl.safe_substitute(product_elem_dict)

        base, ext = os.path.splitext(template_path)
        base = os.path.basename(base)
        if auto_increment_id:
            base = '{}{}'.format(base, str(create_id).zfill(product_digit))
        create_id += 1
        for key, val in product_elem_dict.items():
            base+='_{}-{}'.format(key, val)

        outputfile_path = os.path.join(output_dir, base + ext)

        try:
            with open(outputfile_path, mode='w', encoding=encoding, newline=line_feed_code) as fw:
                fw.write(gen)
                print ('generate OK > {}'.format(outputfile_path))
        except OSError:
            print ('generate NG (write failed) > {}'.format(outputfile_path))
            error_occur = True
            continue

    return 1 if error_occur else 0


def parse():
    desc = 'Simple combination template engine.'
    argparser = ArgumentParser(description=desc)
    argparser.add_argument('FILE', type=str,
                           help='json template file')
    argparser.add_argument('-v', '--verbose',
                           action='store_const',
                           const=True,
                           default=False,
                           help='print verbose message')
    args = argparser.parse_args()
    return args


if __name__ == '__main__':
    result = parse()
    sys.exit( generate(result.FILE, result.verbose ) )
