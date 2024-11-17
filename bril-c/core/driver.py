import sys
import json
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from antlr4.tree.Trees import Trees
from CToBrilVisitor import CToBrilVisitor
from SemAnalysisVisitor import SemAnalysisVisitor

def main(argv):
    debug_mode = "-D" in argv
    if debug_mode:
        argv.remove("-D")

    # Source Code -> [Lexer and Parser] -> AST -> [SemAnalyze] -> [CodeGen] -> Bril IR
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()

    if debug_mode:
        print("Syntax Tree:")
        print(Trees.toStringTree(tree, None, parser))

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        # SemAnalyze
        if debug_mode:
            print("\nSemAnalyze:")
        sem_analysis = SemAnalysisVisitor(debug_mode=debug_mode)
        sem_analysis.visit(tree)

        # CodeGen
        if debug_mode:
            print("\nCodeGen:")
        code_gen = CToBrilVisitor(debug_mode=debug_mode)
        code_gen.visit(tree)

        if debug_mode:
            print("\nGenerated Bril Program:")
        
        json.dump(code_gen.bril_program, sys.stdout, indent=2)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 driver.py [-D] <c-source-file>")
    else:
        main(sys.argv)

