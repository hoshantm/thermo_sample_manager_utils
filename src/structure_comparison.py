# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 13:22:14 2022

@author: Hoshan, Tarik M

Recursively compare structure trees and store the results in a data structure for later reporting

"""

from data_structures import  Differences, Difference
from structure_transformer import parse_and_transform

def compare(item1, item2):
    if hasattr(item1, 'is_named_items_dictionary') and hasattr(item2, 'is_named_items_dictionary'):
        new_item_names = item2.names - item1.names
        deleted_item_names = item1.names - item2.names
        common_items = item1.names.intersection(item2.names)
        item1_common_items = {item.name: item for item in item1.values() if item.name in common_items}
        item2_common_items = {item.name: item for item in item2.values() if item.name in common_items}
        differences = {common_item: compare(item1_common_items[common_item], item2_common_items[common_item]) for common_item in common_items}

        differences = {k: v for k, v in differences.items() if v is not None}
        if len(new_item_names) == 0 and len(deleted_item_names) == 0 and len(differences) == 0:
            return None
        else:
            return Differences(new_item_names, deleted_item_names, differences)

    elif hasattr(item1, 'is_named_item') and hasattr(item2, 'is_named_item'):
        differences = {attribute_name: compare(getattr(item1, attribute_name), getattr(item2, attribute_name)) for attribute_name in item1.property_names}
        differences = {k: v for k, v in differences.items() if v is not None}
        if len(differences) == 0:
            differences = None
        return differences
    else:
        return Difference(item1, item2) if item1 != item2 else None

if __name__ == '__main__':
    file_path1 = 'SampleStructureFiles/structure.txt'
    file_path2 = 'SampleStructureFiles/structure2.txt'

    if not 'structure1' in globals():
        print(f'parsing {file_path1}...')
        structure1 = parse_and_transform(file_path1)

    if not 'structure2' in globals():
        print(f'parsing {file_path2}...')
        structure2 = parse_and_transform(file_path2)

    result = compare(structure1, structure2)
    print(result)







