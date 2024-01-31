import os

if os.name == "nt":
    for path in os.getenv("FN_PYTHON_DLL_DIRECTORIES", "").split(os.pathsep):
        try:
            # from Python 3.8 DLL loading is more restrictive, disallowing PATH, see https://bugs.python.org/issue43173
            os.add_dll_directory(path)
        except AttributeError:
            os.environ["PATH"] += os.pathsep + path
