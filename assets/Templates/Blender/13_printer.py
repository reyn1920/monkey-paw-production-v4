import sys
import ast


class Printer(ast.NodeVisitor):

    def __init__(self, file=sys.stdout, indent="  "):
        self.indentation = 0
        self.indent_with = indent
        self.f = file

    # overridden to make the API obvious
    def visit(self, node):
        super().visit(node)

    def write(self, text):
        self.f.write(str(text))

    def generic_visit(self, node):

        if isinstance(node, list):
            nodestart = "["
# BRACKET_SURGEON: disabled
#             nodeend = "]"
            children = [("", child) for child in node]
        else:
            nodestart = type(node).__name__ + "("
# BRACKET_SURGEON: disabled
#             nodeend = ")"
            children = [(name + "=", value) for name, value in ast.iter_fields(node)]

        if len(children) > 1:
            self.indentation += 1

        self.write(nodestart)
        for i, pair in enumerate(children):
            attr, child = pair
            if len(children) > 1:
                self.write("\n" + self.indent_with * self.indentation)
            if isinstance(child, (ast.AST, list)):
                self.write(attr)
                self.visit(child)
            else:
                self.write(attr + repr(child))

            if i != len(children) - 1:
                self.write(",")
        self.write(nodeend)

        if len(children) > 1:
            self.indentation -= 1