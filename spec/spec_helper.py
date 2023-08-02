import os
import sys
from importlib import import_module

# Path to the pre-resolved locked set of modules
locked_modules_path = os.path.expanduser('~/.bundle/environment')

if os.path.isfile(locked_modules_path):
    try:
        # Try to import the pre-resolved locked set of modules
        import_module(locked_modules_path)
    except ImportError as e:
        print(f"Unable to import locked modules from {locked_modules_path}. Error: {str(e)}")
else:
    print(f"No locked module file found at {locked_modules_path}. Continuing without it.")

# All imports should be done manually

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')

# Add the library path to the system path
lib_path = os.path.join(PROJECT_ROOT, 'lib')
if os.path.isdir(lib_path):
    sys.path.append(lib_path)
else:
    print(f"Library path {lib_path} does not exist. Please ensure it is correct.")

# The import statement equivalent of require in Python
try:
    from quality_measure_engine import *
except ImportError as e:
    print(f"Unable to import the Quality Measure Engine. Error: {str(e)}")
    sys.exit(1)  # Exit the script since the engine couldn't be imported
