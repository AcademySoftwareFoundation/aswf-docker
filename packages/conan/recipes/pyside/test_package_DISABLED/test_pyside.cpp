#include "QtGui/pyside6_qtgui_python.h"
#include "QtWidgets/pyside6_qtwidgets_python.h"

#include "autodecref.h" // from shiboken
#include "sbkmodule.h"


void initPySide()
{
    Shiboken::AutoDecRef requiredCoreModule(Shiboken::Module::import("PySide6.QtCore"));
    if (requiredCoreModule.isNull()) {
        PyErr_SetString(PyExc_ImportError,"could not import PySide6.QtCore");
    }
    else {
        Shiboken::AutoDecRef requiredWidgetsModule(Shiboken::Module::import("PySide6.QtWidgets"));
        if (requiredWidgetsModule.isNull()) {
            PyErr_SetString(PyExc_ImportError,"could not import PySide6.QtWidgets");
        }
    }
}
