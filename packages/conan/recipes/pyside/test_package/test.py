try:
    from PySide2.QtWidgets import QApplication
except ImportError:
    import sys
    import pprint

    pprint.pprint(sys.path)
    raise
