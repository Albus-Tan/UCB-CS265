import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from antlr4.tree.Trees import Trees

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()
    print(Trees.toStringTree(tree, None, parser))

if __name__ == '__main__':
    main(sys.argv)

