#!/bin/bash

# https://pythonhosted.org/PyInstaller/usage.html
# --onedir "./src/main.py" \
# --additional-hooks-dir="/usr/local/lib/python3.7/site-packages/PyInstaller/hooks" \
: <<'END'
--add-data="./src/main.py:src" \
--add-data="./src/core:src/core" \
--add-data="./src/modules:src/modules" \
--add-data="./src/canary_gui.py:src" \
--add-data="./src/resources:src/resources" \
--hidden-import="sqlite3" \
--hidden-import="requests" \
--hidden-import="bs4" \
--hidden-import="lxml.html" \
--exclude numpy \
--exclude win32com \
--exclude cryptography \
--debug \

END


OS=$(uname -a | cut -d " " -f 1)

pyinstaller --specpath . \
            --name "canary" \
            --log-level="DEBUG" \
            --noupx \
            --onefile "main.py" \
            --add-data="canary_gui.py:." \
            --add-data="app/resources:./app/resources" \
            --additional-hooks-dir="./specs/hooks" \
            --hidden-import="bottle_websocket" \
            --hidden-import="pandas._libs.tslibs.timedeltas" \
            --clean


# mv ./dist/* ../dist/
# rm -r ./build ./dist