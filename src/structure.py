from structure_parser import parse_structure
from structure_transformer import parse_and_transform
from structure_comparison import compare
from generate_comparison_output import transform_to_ascii_tree, generate_data_frame
import argparse
from os import path
import sys

try:
    from asciitree import LeftAligned, BoxStyle
    from asciitree.drawing import BOX_HEAVY
    ascii_tree_lib_imported = True
except ImportError:
    print("""Install the asciitree library included under the lib/asciitree folder by issuing the following command:
        pip install --user asciitree-0.3.3.tar.gz""")
    ascii_tree_lib_imported = False

def check_file_exists(file_path):
    if not path.exists(file_path):
        print(f'File {file_path} does not exist.')
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Thermo SampleManager parsing and comparison utilities.')

    subparsers = parser.add_subparsers()

    parse_parser = subparsers.add_parser('parse', help='Parse a structure.txt file')
    parse_parser.add_argument('file', type=argparse.FileType('r'), metavar=('filename'), help='File to parse.')

    compare_parser = subparsers.add_parser('compare', help='\n'.join(['compare command:', \
                                                     'Example:', \
                                                     'python structure.py parse '
                                                     'python structure.py compare SampleStructureFile/small-1.txt SampleStructureFile/small-2.txt -t output.txt', \
                                                     'python structure.py compare SampleStructureFile/small-1.txt SampleStructureFile/small-2.txt -e output.xlsx']))
    compare_parser.add_argument('file1', type=argparse.FileType('r'), metavar='filename1', help='First file to compare')
    compare_parser.add_argument('file2', type=argparse.FileType('r'), metavar='filename1', help='Second file to compare')
    output_options = compare_parser.add_mutually_exclusive_group(required=True)
    output_options.add_argument('-e', '--excel', type=argparse.FileType('wb'), metavar='exceloutput', help='Excel output file')
    output_options.add_argument('-t', '--tree', type=argparse.FileType('w', encoding='utf-8'), metavar='treeoutput', help='Tree output text file')

    args = parser.parse_args()
    if hasattr(args, 'file'):
        print(f'Parsing {args.file.name}...')
        parse_structure(args.file)
        print(f'{args.file.name} has a correct structure.')
    elif hasattr(args, 'file1'):
        print(f'Parsing and transforming {args.file1.name}...')
        structure1 = parse_and_transform(args.file1)
        print(f'Parsing and transforming {args.file2.name}...')
        structure2 = parse_and_transform(args.file2)
        print('Comparing...')
        result = compare(structure1, structure2)
        if not args.excel is None:
            df = generate_data_frame(result)
            df.to_excel(args.excel, index=False)
            print(f'Saving to {args.excel.name}...')
            args.excel.close()
        elif not args.tree is None:
            if ascii_tree_lib_imported:
                print('Generating tree...')
                tree = transform_to_ascii_tree(result)
                print('Printing tree...')
                tr = LeftAligned(draw=BoxStyle(gfx=BOX_HEAVY, horiz_len=2))
                args.tree.write(tr(tree))
                args.tree.close()
            else:
                print('Missing asciitree library. Cannot print tree.')
            
    else:
        parser.print_help()





