from luqum.parser import parser
from luqum.tree import *
import json

query = '("H.B. Fuller" OR "HB fuller" OR "Arkema" OR (headline:("RPM")) OR "Saint-Gobain" OR "saint gobain" OR (PPG AND coatings) OR "Albemarle" OR "ITW" OR "Hitachi" OR "3M") NOT ("Albemarle County" OR "Albemarle Rd" OR "Albemarle Sound" OR "pamlico sounds" OR "Albemarle sounds")'

tree = parser.parse(query)
print("AST Type:", type(tree).__name__)
print("AST:", tree)
print("\nTree structure:")

def print_tree(node, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{type(node).__name__}: {node}")
    if hasattr(node, 'children'):
        for child in node.children:
            print_tree(child, indent + 1)

print_tree(tree)
