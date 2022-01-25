#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 11:15:00 2022

@author: Hoshan, Tarik M

This module transforms the lark parse tree into a developer friendly data structure that
can be used to compare different versions of structure.txt files.
"""
from lark import Transformer, Token
from data_structures import  Structure, OptionSection, Option, FieldOption, FieldType, FieldUse, \
                    FieldDefinition, FieldLinksTo, TableDefinition, Collection, \
                    IndexDefinition, ViewDefinition, Sequence, NamedItemsDictionary,\
                    IndexFieldDefinition, FieldAlias, TableName

from structure_parser import parse_structure

class StructureDotTextTransformer(Transformer):

    def structure(self, nodes):
        assert(nodes[0].data == 'option_sections')
        options = NamedItemsDictionary({option.name: option for option in nodes[0].children})
        tables = nodes[1]['tables']
        views = nodes[1]['views']
        sequences = nodes[1]['sequences']
        structure_data = Structure(options, tables, views, sequences)
        return structure_data

    def option_section(self, nodes):
        assert(len(nodes) == 2)
        assert(nodes[0].type == 'SECTION_NAME')
        option_section_name = nodes[0].value
        option_set = NamedItemsDictionary({option_section.name: option_section for option_section in nodes[1].children})
        return OptionSection(option_section_name, option_set)

    def option(self, nodes):
        assert(len(nodes) <= 2)
        assert(nodes[0].type == 'OPTION_NAME')
        option_name = nodes[0].value
        if len(nodes) == 2:
            assert(nodes[1].type == 'OPTION_VALUE')
            option_value = nodes[1].value
        else:
            option_value = None

        return Option(option_name, option_value)

    def table_option(self, nodes):
        assert(len(nodes) <= 2)
        option_name = nodes[0].value
        if len(nodes) == 2:
            option_value = nodes[1].value
        else:
            option_value = None

        return Option(option_name, option_value)

    def entity_definitions(self, nodes):
        tables = NamedItemsDictionary({entity.name: entity for entity_type, entity in nodes if entity_type == 'table'})
        views = NamedItemsDictionary({entity.name: entity for entity_type, entity in nodes if entity_type == 'view'})
        sequences = NamedItemsDictionary({entity.name: entity for entity_type, entity in nodes if entity_type == 'sequence'})
        return {'tables': tables, 'views': views, 'sequences': sequences}

    def table_definition(self, nodes):
        table_name = nodes[0]['name']
        table_options = NamedItemsDictionary({option.name: option for option in nodes[0]['options']})
        field_definitions = NamedItemsDictionary({field_definition.name: field_definition for field_definition in nodes[1].children})
        collection_definitions = NamedItemsDictionary({collection_definition.name: collection_definition for collection_definition in nodes[2].children})
        index_definitions = NamedItemsDictionary({index_definition.name: index_definition for index_definition in nodes[3].children})
        table = TableDefinition(table_name, table_options, field_definitions, collection_definitions, index_definitions)
        return 'table', table

    def table_header(self, nodes):
        assert(nodes[0].type == 'TABLE')
        assert(nodes[1].type == 'TABLE_NAME')
        return {'name': nodes[1].value, 'options': nodes[2].children}

    def view_definition(self, nodes):
        view_name = nodes[0]['name']
        view_options = nodes[0]['options']
        view_on_tables = nodes[0]['on_tables']
        view = ViewDefinition(view_name, view_options, view_on_tables)
        return 'view', view

    def view_header(self, nodes):
        assert(len(nodes) <= 4)
        assert(nodes[0].type == 'VIEW')
        assert(nodes[1].type == 'VIEW_NAME')
        on_tables = nodes[3] if len(nodes) == 4 else None
        return {'name': nodes[1].value, 'options': nodes[2].children, 'on_tables': on_tables}

    def on_table(self, nodes):
        assert(all(map(lambda node: node.type == 'TABLE_NAME', nodes)))
        tables = NamedItemsDictionary({node.value: TableName(node.value) for node in nodes})
        return tables

    def sequence_clause(self, nodes):
        assert(nodes[0].type == 'SEQUENCE')
        assert(nodes[1].type == 'SEQUENCE_NAME')
        sequence_name = nodes[1].value
        assert(nodes[2].type == 'MAJOR')
        major = nodes[3].value
        assert(nodes[4].type == 'MINOR')
        minor = nodes[5].value
        sequence = Sequence(sequence_name, major, minor)
        return 'sequence', sequence

    def field_definition(self, nodes):
        assert(nodes[0].type == 'FIELD_NAME')
        name = nodes[0].value
        options = nodes[1]
        definition = FieldDefinition(name, options)
        return definition

    def field_options(self, nodes):
        return NamedItemsDictionary({node.name: node for node in nodes})

    def field_option(self, nodes):
        assert(len(nodes) <= 2)
        option_name = nodes[0].value
        if len(nodes) == 2:
            if type(nodes[1]) is Token:
                option_value = nodes[1].value
            else:
                option_value = nodes[1]
        else:
            option_value = None
        return FieldOption(option_name, option_value)

    def field_alias(self, nodes):
        assert(all(map(lambda node: node.type == 'FIELD_ALIAS', nodes)))
        aliases = NamedItemsDictionary({node.value: FieldAlias(node.value) for node in nodes})
        return aliases

    def field_type(self, nodes):
        field_type_name = nodes[0].value
        assert(len(nodes) <= 2)
        if len(nodes) == 2:
            assert(nodes[1].type == 'FIELD_SIZE')
            size = nodes[1].value
        else:
            size = None
        return FieldType(field_type_name, size)

    def field_used_for(self, nodes):
        return NamedItemsDictionary({field_use.name: field_use for field_use in nodes})

    def field_use(self, nodes):
        field_use_name = nodes[0].value
        assert(len(nodes) <= 2)
        if len(nodes) == 2:
            assert(nodes[1].type == 'FIELD_SIZE')
            size = nodes[1].value
        else:
            size = None
        return FieldUse(field_use_name, size)

    def field_links_to(self, nodes):
        assert(len(nodes) <= 3)
        table_name = nodes[0].value
        field_name = nodes[1].value
        if len(nodes) == 3:
            alias_name = nodes[2].value
        else:
            alias_name = None
        return FieldLinksTo(table_name, field_name, alias_name)

    def field_prompt_type(self, nodes):
        return nodes[0].value

    def collection_definition(self, nodes):
        assert(nodes[0].type == 'COLLECTION_NAME')
        collection_name = nodes[0].value
        assert(nodes[1].type == 'COLLECTION_ON')
        collection_on = nodes[1].value
        assert(nodes[2].type == 'COLLECTION_USING')
        collection_using = nodes[2].value
        return Collection(collection_name, collection_on, collection_using)

    def index_definition(self, nodes):
        assert(nodes[0].type == 'INDEX')
        assert(nodes[1].type == 'INDEX_NAME')
        index_name = nodes[1].value
        i = 2
        if type(nodes[i]) is Token and nodes[i].type == 'UNIQUE':
            unique_flag = True
            i+=1
        else:
            unique_flag = False

        index_fields = NamedItemsDictionary({index_field.name: index_field for index_field in nodes[i].children})
        i+=1
        assert(nodes[i].data == 'index_options')
        index_options = NamedItemsDictionary({node.name: node for node in nodes[i].children})

        return IndexDefinition(index_name, unique_flag, index_fields, index_options)

    def index_field_definition(self, nodes):
        assert(len(nodes) == 1)
        index_field_name = nodes[0].value
        return IndexFieldDefinition(index_field_name)

def parse_and_transform(file_path):
    tree = parse_structure(file_path)
    print('Transforming...')
    transformer = StructureDotTextTransformer()
    structure = transformer.transform(tree)
    return structure

if __name__ == '__main__':
    if 'tree' not in globals():
        print('parsing structure file...')
        tree = parse_structure('SampleStructureFiles/structure.txt')
    print('Transforming...')
    transformer = StructureDotTextTransformer()
    structure = transformer.transform(tree)