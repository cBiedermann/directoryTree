import os
import re
from enum import Enum


class Seperator(Enum):
    MIDDLE = '├──'
    LAST = '└──'
    TO_PARENT = '│   '
    SPACE = '    '


class Tree:

    def __init__(self, max_depth: int = 10,
                 directories: bool = True,
                 files: bool = True,
                 exclude: list = [], only: list = [], show_hidden: bool = True, full_path: bool = False,
                 print_sum: bool = True):

        # class variables
        self.max_depth = max_depth
        self.directories = directories
        self.files = files
        self.exclude = exclude
        self.only = only
        self.show_hidden = show_hidden
        self.full_path = full_path
        self.print_sum = print_sum

    def down(self, path: str, depth: int, last_elem) -> list:
        """
        method to get down in the tree
        :param path: of the current position
        :param depth: of the current position
        :param last_elem: bool list if there should be a space to the parent or not at the depth
        :return: string representation of current position as a list of string
        """
        str_representation = []
        # checking if the file/folder is already too deep
        if depth >= self.max_depth:
            return str_representation
        # just include the files/folder which are not excluded
        entries = [entry for entry in os.listdir(path) if not self.entry_matches(entry)]
        for entry in entries:
            # if file/folder should be included
            if self.only == [] or self.entry_matches(entry, included=True):
                last = entry == entries[-1]
                temp = last_elem.copy()
                if last:
                    temp[depth] = False
                str_representation.append(
                    self.get_string_representation(os.path.join(path, entry), depth, last, temp))
                if os.path.isdir(os.path.join(path, entry)):
                    str_representation += self.down(f'{path}{os.path.sep}{entry}', depth=depth + 1,
                                                    last_elem=temp)
        return str_representation

    def get_string_representation(self, path: str, depth: int, last: bool, last_elem) -> str:
        element: str = path if self.full_path else path.split(os.path.sep)[-1]
        representation = ''
        for i in range(depth):
            representation += Seperator.TO_PARENT.value if last_elem[i] else Seperator.SPACE.value
        return representation + str(Seperator.LAST.value if not last_elem[depth] else Seperator.MIDDLE.value) + element

    def entry_matches(self, entry: str, included: bool = False) -> bool:
        data = self.only if included else self.exclude
        for regex in data:
            if re.match(regex, entry):
                return True
        return False


def print_tree(path: str = '', print_string: bool = True, max_depth: int = 10,
               directories: bool = True,
               files: bool = True,
               exclude: list = [], only: list = [], show_hidden: bool = True, full_path: bool = False,
               print_sum: bool = True):
    """
    this method provides the functionality to print the working directory by setting multiple options
    :param path: directory which should be printed -> cwd if nothing is specified
    :param print_string: default prints the string -> False return the string in the end
    :param max_depth: default 10
    :param directories: directories are printed by default -> False if they should not be printed
    :param files: files are printed by default -> False if they should not be printed
    :param exclude: list of regexes -> files & folders which match will not be printed
    :param only: list of regexes -> only files & folder which match will be printed
    :param show_hidden: hidden folders & files are printed by default -> False to change
    :param full_path: the full path from the given path is printed
    :param print_sum: printing the number of directories and files in the end
    :return: tree as a string if print_string == False, otherwise nothing
    """
    if path == '':
        path = os.getcwd()
    if not show_hidden:
        exclude.append(r'^\..*')
    directory_tree = Tree(max_depth, directories, files, exclude, only, show_hidden, full_path,
                          print_sum)
    tree = [path] + directory_tree.down(path, 0, [True] * max_depth)
    if print_string:
        print(*tree, sep='\n')
    else:
        return tree


if __name__ == '__main__':
    print_tree('/Users/clara/Documents/Uni/4.Semester/LSP', show_hidden=False, max_depth=2)