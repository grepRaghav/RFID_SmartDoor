# After refactoring, this file is the entrypoint; logic lives in submodules.

"""Entry point for the AI RFID Smart Door application.

This module can be executed either as a script (``python app/main.py``) or
as a module (``python -m app.main``) from the project root.  When the
script is executed directly, the parent directory (the repository root) is
added to ``sys.path`` so that the ``app`` package can be imported.  Without
this adjustment a ``ModuleNotFoundError: No module named 'app'`` is raised
because Python only adds the script's directory to the import path.
"""

import os
import sys

# when running the file directly, the interpreter adds the ``app/``
# directory to sys.path which prevents imports from the package itself.  add
# the parent folder of ``app`` (the repo root) so that ``import app`` works.
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from app import gui
from app import serial_listener


def main():
    # start the background serial listening thread
    serial_listener.start_thread()

    # launch the GUI event loop
    gui.root.mainloop()


if __name__ == "__main__":
    main()
