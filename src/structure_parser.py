# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 08:30:19 2022

@author: Hoshan, Tarik M

Parse structure.txt file using grammar defined in structure.lark
"""
import sys
import io

try:
    from lark import Lark
except ImportError:
    print("""Install the lark-parser library included under the lib/lark folder by issuing the following command:
        pip install --user lark_parser-0.12.0-py2.py3-none-any.whl""")
    sys.exit(1)

with open('structure.lark', 'r') as f_grammar:
    lark = Lark(f_grammar, start='structure')

def parse_structure(file_path):
    if type(file_path) is str:
        with open(file_path, 'r') as f_structure:
            text = f_structure.read()
    elif type(file_path) is io.TextIOWrapper:
        text = file_path.read()

    try:
        tree = lark.parse(text)
        return tree
    except Exception as ex:
        name = file_path if type(file_path) is str else file_path.name
        print(f'Incorrect structure of {name}:')
        print(ex)
        sys.exit(3)
    
if __name__ == '__main__':
    result = parse_structure('SampleStructureFiles/bad.txt')
