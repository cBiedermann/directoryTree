import os
import re
from enum import Enum


class Seperator(Enum):
    MIDDLE = '├──'
    LAST = '└──'
    TO_PARENT = '│   '
    SPACE = '    '


class Tree:

    def __init__(self, start_path, max_depth: int = 10, directories: bool = True, files: bool = True, exclude: list = [],
                 include: list = [], show_hidden: bool = True, absolute_path: bool = False,
                 relative_path: bool = False, print_sum: bool = True):

        # class variables
        self.start_path = start_path
        self.max_depth = max_depth
        self.directories = directories
        self.files = files
        self.exclude = exclude
        self.include = include
        self.show_hidden = show_hidden
        self.absolute_path = absolute_path
        self.relative_path = relative_path
        self.print_sum = print_sum
        self.dicts = 0
        self.f = 0

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
        entries = [entry for entry in os.listdir(path) if
                   not self.entry_matches(entry) and self.entry_matches(entry, included=True)]
        for entry in entries:
            last = entry == entries[-1]
            temp = last_elem.copy()
            if last:
                temp[depth] = False
            if os.path.isfile(os.path.join(path, entry)) and self.files:
                self.f += 1
                str_representation.append(self.get_string_representation(os.path.join(path, entry), depth, temp))
            if self.directories and os.path.isdir(os.path.join(path, entry)):
                str_representation.append(self.get_string_representation(os.path.join(path, entry), depth, temp))
                self.dicts += 1
                str_representation += self.down(f'{path}{os.path.sep}{entry}', depth=depth + 1, last_elem=temp)
        return str_representation

    def get_string_representation(self, path: str, depth: int, last_elem) -> str:
        if self.absolute_path:
            element = path
        elif self.relative_path:
            element = path.split(self.start_path + os.path.sep)[1]
        else:
            element = path if self.absolute_path else path.split(os.path.sep)[-1]
        representation = ''
        for i in range(depth):
            representation += Seperator.TO_PARENT.value if last_elem[i] else Seperator.SPACE.value
        return representation + str(Seperator.LAST.value if not last_elem[depth] else Seperator.MIDDLE.value) + element

    def entry_matches(self, entry: str, included: bool = False) -> bool:
        data = self.include if included else self.exclude
        for regex in data:
            if re.match(regex, entry):
                return True
        return False


def print_tree(path: str = '', print_string: bool = True, max_depth: int = 10, directories: bool = True,
               files: bool = True, exclude: list = [], include: list = [], show_hidden: bool = True,
               absolute_path: bool = False, relative_path: bool = False, print_sum: bool = True):
    """
    this method provides the functionality to print the working directory by setting multiple options
    :param path: directory which should be printed -> cwd if nothing is specified
    :param print_string: default prints the string -> False return the string in the end
    :param max_depth: default 10
    :param directories: directories are printed by default -> False if they should not be printed
    :param files: files are printed by default -> False if they should not be printed
    :param exclude: list of regexes -> files & folders which match will not be printed
    :param include: list of regexes -> only files & folder which match will be printed
    :param show_hidden: hidden folders & files are printed by default -> False to change
    :param absolute_path: the absolute path from the file/folder is printed
    :param relative_path: the relative path according to the argument path is printed
    :param print_sum: printing the number of directories and files in the end
    :return: tree as a string if print_string == False, otherwise nothing
    """
    if path == '':
        path = os.getcwd()
    if not show_hidden:
        exclude.append(r'^\..*')
    if not include:
        # if there is nothing specified, all files should be included except those which are excluded
        include = [r'.*']
    directory_tree = Tree(path, max_depth, directories, files, exclude, include, show_hidden, absolute_path, relative_path,
                          print_sum)
    tree = [path] + directory_tree.down(path, 0, [True] * max_depth)
    if directory_tree.print_sum:
        tree += [f'{directory_tree.dicts} directories, {directory_tree.f} files']
    if print_string:
        print(*tree, sep='\n')
    else:
        return tree


if __name__ == '__main__':
    print_tree(max_depth=3, show_hidden=False, relative_path=True)
