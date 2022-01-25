# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 10:35:05 2022

@author: Hoshan, Tarik M

Recursively prints the comparison results

"""
from structure_comparison import compare
from data_structures import Difference, Differences
from structure_transformer import parse_and_transform
import pandas as pd
import numpy as np
from collections import OrderedDict

try:
    from asciitree import LeftAligned, BoxStyle
    from asciitree.drawing import BOX_HEAVY
    ascii_tree_lib_imported = True
except ImportError:
    print("""Install the asciitree library included under the lib/asciitree folder by issuing the following command:
        pip install --user asciitree-0.3.3.tar.gz""")
    ascii_tree_lib_imported = False

def transform_to_ascii_tree(result):
    if type(result) is dict:
        return OrderedDict([(key, transform_to_ascii_tree(value)) for key, value in result.items()])
    elif str(type(result)) == str(Differences):
        differences = OrderedDict([])
        if len(result.new) > 0:
            differences['new'] = OrderedDict([(name, {}) for name in result.new])
        if len(result.deleted) > 0:
            differences['deleted'] = OrderedDict([(name, {}) for name in result.deleted])
        if len(result.different) > 0:
            differences['different'] = OrderedDict([(key, transform_to_ascii_tree(value)) for key, value in result.different.items()])
        return differences
    elif str(type(result)) == str(Difference):
        return {f'Original Value: {result.old_value}, New Value: {result.new_value}': {}}
    else:
        raise(Exception(f'Unhandled type: {type(result)}'))

def depth(result):
    if type(result) is dict:
        return 1 + max((depth(value) for value in result.values()))
    elif str(type(result)) == str(Differences):
        max_depth = 0
        if len(result.new) > 0:
            max_depth = 2
        if len(result.deleted) > 0:
            max_depth = 2
        if len(result.different) > 0:
            max_depth = 1 + max((depth(value) for value in result.different.values()))
        return max_depth
    elif str(type(result)) == str(Difference):
        return 1
    else:
        raise(Exception(f'Unhandled type: {type(result)}'))

def generate_table(result):
    if type(result) is dict:
        for key, subresult in result.items():
            if str(type(subresult)) == str(Differences):
                for deleted_entity in subresult.deleted:
                    yield (key, deleted_entity, 'Deleted')
                for new_entity in subresult.new:
                    yield (key, new_entity, 'New')
                for name, entity in subresult.different.items():
                    for row in generate_table(entity):
                        yield (key, name, *row)
            else:
                for row in generate_table(subresult):
                    yield (key, *row)
    elif type(result) is frozenset:
        for subresult in result:
            for row in generate_table(subresult):
                yield row
    else:
        yield('Modified',)

def generate_data_frame(result):
    data = list(generate_table(result))
    assert(all(map(lambda row: row[-1] in ['New', 'Deleted', 'Modified'], data)))
    n_columns = max(map(lambda row: len(row), data))
    data = [(*row[0:-1], *((None,) * (n_columns - len(row))), row[-1]) for row in data]
    columns = [f'Level {i+1}' for i in range(n_columns-1)] + ['Status']
    df = pd.DataFrame(data=data, columns=columns)
    df.replace(to_replace=[None], value=np.nan, inplace=True)
    return df

if __name__ == '__main__':
    file_path1 = 'SampleStructureFiles/vanilla-structure.txt'
    file_path2 = 'SampleStructureFiles/structure.txt'

    if not 'structure1' in globals():
        print(f'parsing {file_path1}...')
        structure1 = parse_and_transform(file_path1)

    if not 'structure2' in globals():
        print(f'parsing {file_path2}...')
        structure2 = parse_and_transform(file_path2)

    result = compare(structure1, structure2)

    print('Generating tree...')
    tree = transform_to_ascii_tree(result)
    print('Printing tree...')
    tr = LeftAligned(draw=BoxStyle(gfx=BOX_HEAVY, horiz_len=2))
    print(tr(tree))

    df = generate_data_frame(result)
    print(df)



