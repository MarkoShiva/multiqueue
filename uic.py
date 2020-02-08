from PySide2 import QtWidgets
from pyside2uic import compileUi
from xml.etree import ElementTree
from io import StringIO

def loadUiType(design):
    """
    PySide2 equivalent of PyQt5's `uic.loadUiType()` function.

    Compiles the given `.ui` design file in-memory and executes the
    resulting Python code. Returns form and base class.
    """
    parsed_xml   = ElementTree.parse(design)
    widget_class = parsed_xml.find('widget').get('class')
    form_class   = parsed_xml.find('class').text
    with open(design) as input:
        output = StringIO()
        compileUi(input, output, indent=0)
        source_code = output.getvalue()
        syntax_tree = compile(source_code, filename='<string>', mode='exec')
        scope  = {}
        exec(syntax_tree, scope)
        form_class = scope[f'Ui_{form_class}']
        base_class = eval(f'QtWidgets.{widget_class}')
    return (form_class, base_class)