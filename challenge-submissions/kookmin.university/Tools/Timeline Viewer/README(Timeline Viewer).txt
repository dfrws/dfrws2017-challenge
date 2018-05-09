***********************Timeline Viewer***********************
- input: CSV file(output of JSON Parser, SQLite Databases Extractor, Google OnHub Log Parser)
- ouput: Timeline view

[Source Code Building Instructions]
Program needed to build source code:
- Python 2.x 32 or 64 bit (Implemented environment: Python 2.7.14 32bit)
- IDE (ex, Visual Studion, PyCharm)

Library need to build source code:
- PyQt4 for Python 2.7 
  * You can download here(https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/)
  * File Name: PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe
- matplotlib, numpy
  * You have to install 32-bit version.
  * You can install libraries using pip (Command: pip install [library name])
  * If you don't use pip command in command line, you have to set environment variable. Add 'C:\Python27\Scripts' in System Path.

[How To Use]
1. Implement source code or exe file.

2. Open 'File' or 'Directory' under 'Open' button in menu bar.
   - After choosing file or directory, 'Duration' is displayed.

3. Choose 'Date' that you want to see. Then you will see visualization result.

* The default time zone is UTC +00:00 but this can be changed for convenience at any time (before or after visualization process).
* Mouse-over each marker to view detailed information.
* Use ZOOM, PAN, HOME button.
  - ZOOM: expand canvas. click ZOOM button and drag canvas that you want to expand.
  - PAN: move canvas(up, down, left, right). After click PAN button, click and drang the canvas.
  - HOME: undo ZOOM and PAN function.