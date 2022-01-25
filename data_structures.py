# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 13:32:28 2022

@author: Hoshan, Tarik M

Structures used to store elements parsed from structure.txt
"""

class NamedItem:
    def __init__(self, name, property_names):
        self.__name = name
        self.__property_names = property_names

    @property
    def name(self):
        return self.__name

    @property
    def property_names(self):
        return self.__property_names

    @property
    def is_named_item(self):
        return True
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return str(self.__name) if self.__name is not None else 'NamedItem'

class Structure(NamedItem):
    def __init__(self, option_sections, tables, views, sequences):
        super().__init__(None, ['tables', 'views', 'sequences', 'option_sections'])
        self.__option_sections = option_sections
        self.__tables = tables
        self.__views = views
        self.__sequences = sequences

    @property
    def option_sections(self):
        return self.__option_sections

    @property
    def tables(self):
        return self.__tables

    @property
    def views(self):
        return self.__views

    @property
    def sequences(self):
        return self.__sequences

class TableDefinition(NamedItem):
    def __init__(self, name, options, field_definitions, collection_definitions, index_definitions):
        super().__init__(name, ['options', 'field_definitions', 'collection_definitions', 'index_definitions'])
        self.__options = options
        self.__field_definitions = field_definitions
        self.__collection_definitions = collection_definitions
        self.__index_definitions = index_definitions

    @property
    def options(self):
        return self.__options

    @property
    def field_definitions(self):
        return self.__field_definitions

    @property
    def collection_definitions(self):
        return self.__collection_definitions

    @property
    def index_definitions(self):
        return self.__index_definitions

class ViewDefinition(NamedItem):
    def __init__(self, name, options, on_tables):
        super().__init__(name, ['options', 'on_tables'])
        self.__options = options
        self.__on_tables = on_tables

    @property
    def options(self):
        return self.__options

    @property
    def on_tables(self):
        return self.__on_tables

class Sequence(NamedItem):
    def __init__(self, name, major, minor):
        super().__init__(name, ['major', 'minor'])
        self.__major = major
        self.__minor = minor

    @property
    def major(self):
        return self.__major

    @property
    def minor(self):
        return self.__minor

class FieldDefinition(NamedItem):
    def __init__(self, name, options):
        super().__init__(name, ['options'])
        self.__options = options

    @property
    def options(self):
        return self.__options

class FieldType(NamedItem):
    def __init__(self, data_type, size):
        super().__init__(data_type, ['data_type', 'size'])
        self.__size = size

    @property
    def data_type(self):
        return self.name

    @property
    def size(self):
        return self.__size

class FieldOption(NamedItem):
    def __init__(self, name, value):
        super().__init__(name, ['value'])
        self.__value = value

    @property
    def value(self):
        return self.__value

class FieldUse(NamedItem):
    def __init__(self, name, size):
        super().__init__(name, ['size'])
        self.__size = size

    @property
    def size(self):
        return self.__size

class FieldLinksTo(NamedItem):
    def __init__(self, table, field, alias):
        super().__init__(str((table, field)).lower(), ['table', 'field', 'alias'])
        self.__table = table
        self.__field = field
        self.__alias = alias

    @property
    def table(self):
        return self.__table

    @property
    def field(self):
        return self.__field

    @property
    def alias(self):
        return self.__alias

class Option(NamedItem):
    def __init__(self, name, value):
        super().__init__(name, ['value'])
        self.__value = value

    @property
    def value(self):
        return self.__value

class OptionSection(NamedItem):
    def __init__(self, name, options):
        super().__init__(name, ['options'])
        self.__options = options

    @property
    def options(self):
        return self.__options

class Collection(NamedItem):
    def __init__(self, name, collection_on, collection_using):
        super().__init__(name, ['collection_on', 'collection_using'])
        self.__collection_on = collection_on
        self.__collection_using = collection_using

    @property
    def collection_on(self):
        return  self.__collection_on

    @property
    def collection_using(self):
        return self.__collection_using

class IndexDefinition(NamedItem):
    def __init__(self, name, unique, fields, options):
        super().__init__(name, ['unique', 'fields', 'options'])
        self.__unique = unique
        self.__fields = fields
        self.__options = options

    @property
    def unique(self):
        return self.__unique

    @property
    def fields(self):
        return self.__fields

    @property
    def options(self):
        return self.__options

class Differences(NamedItem):
    def __init__(self, new, deleted, different):
        super().__init__(None, ['new', 'deleted', 'different'])
        self.__new = new
        self.__deleted = deleted
        self.__different = different

    @property
    def new(self):
        return self.__new

    @property
    def deleted(self):
        return self.__deleted

    @property
    def different(self):
        return self.__different
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        n_new = len(self.new)
        n_deleted = len(self.deleted)
        n_different = len(self.different) if type(self.different) is not str and hasattr(self.different, '__len__') else 1
        return f'Differences (new: {n_new}, deleted: {n_deleted}, different: {n_different})'

class Difference(NamedItem):
    def __init__(self, old_value, new_value):
        super().__init__(None, ['old_value', 'new_value'])
        self.__old_value = old_value
        self.__new_value = new_value

    @property
    def old_value(self):
        return self.__old_value

    @property
    def new_value(self):
        return self.__new_value
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        str_old_value = 'N/A' if self.__old_value is None else str(self.__old_value)
        str_new_value = 'N/A' if self.__new_value is None else str(self.__new_value)
        return f'Old Value: {str_old_value}, New Value: {str_new_value}'

class IndexFieldDefinition(NamedItem):
    def __init__(self, name):
        super().__init__(name, ['name'])

class FieldAlias(NamedItem):
    def __init__(self, name):
        super().__init__(name, ['name'])

class TableName(NamedItem):
    def __init__(self, name):
        super().__init__(name, ['name'])

class NamedItemsDictionary(dict):
    def __init__(self, s):
        check_all_named_items(s)
        super().__init__(s)

    @property
    def names(self):
        return frozenset([item.name for item in self.values()])

    @property
    def is_named_items_dictionary(self):
        return True

def check_all_named_items(items):
    no_names = [item for item in items.values() if not hasattr(item, 'name')]
    if len(no_names) > 0:
        message = f'Items with no names: {no_names}'
        print(message)
        raise(Exception(message))


