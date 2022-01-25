# thermo_sample_manager_utils

Thermo Fisher SampleManager Utilities provides a set of tools aimed at system administrators. Provided so far is a structure.txt parser and comparison utility written in Python.

Requirements:
- asciitree: https://pypi.org/project/asciitree/
- lark-parser: https://github.com/lark-parser/lark
- Pandas
- Numpy 

The following are the commands that can be used from the command prompt:

To parse a structure.txt file and verify that there are no errors in the file:  
python structure.py parse structure.txt

To compare two structure.txt files and get the result as a tree diff in a text file:  
python compare structure1.txt structure2.txt -t output.txt

To compare two structure.txt files and get the result as a table in an Excel workbook:  
python compare structure1.txt structure2.txt -e output.xlsx

Notes:  
- Only sample structure.txt files have been included in this repository to avoid copyright issues. Nevertheless, the parser is able to correctly parse the structure.txt provided by the default installation and was also tested against a customized version with significant additions, deletions and modifications.  
- This is an initial version and more work is necessary to make it foolproof.  
- Views SQL statements are not parsed. This would have increased the complexity of this project with little added value. SQL statements are parsed as a single token composed of any text and ending with a semicolon.
