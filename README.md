# directoryTree
This package provides the possibility to print the tree of a directory by specifying several options.

## Usage
The method print_tree() handles all the possible options which are explained in the following:
- if no path is specified the methods takes the current working directory
- print_string = True means that the tree is printed directly to the console instead of being returned as a list of strings
- max_depth specifies the maximum depth of the tree
- directories = False means that directories are excluded
- files = False means that files are excluded
- excluded is a list of regexes matching the files/folders which should be excluded
- include takes a list of regexes matching the files/folders which should be in the tree. Files in a matched folder still need to match a regex as well.
- show_hidden = True means that hidden files (starting with a dot) are also printed
- absolute_path = True means that the absolute path of all the files/folders is printed
- relative_path = True means that the relative path of all the files/folders is printed \
  (note: if absolute and relative path are True the absolute path is printed)
- print_sum = True prints the number of files and directories in the tree

### Example usage
```python
from Tree import print_tree

if __name__ == '__main__':
    # prints the tree of the current working directory three options
    print_tree(relative_path=True, show_hidden=False, max_depth=5)
```
## Output

The generated output can look like this:
```
/Users/clara/Projekte/Directory
├──Tree.py
├──README.md
└──venv
    ├──bin
    │   ├──pip3.8
    │   ├──wheel3
    │   ├──activate.ps1
    │   ├──python3
    │   ├──wheel3.8
    │   ├──pip
    │   ├──activate.xsh
    │   ├──activate
    │   ├──pip-3.8
    │   └──activate.csh
    ├──pyvenv.cfg
    └──lib
        └──python3.8
4 directories, 20 files
```