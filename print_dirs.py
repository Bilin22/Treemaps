"""Assignment 2: Demonstration of using the os module

=== CSC148 Winter 2023 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith
[TODO copyright update...]
"""

import os
from tm_trees import ordered_listdir


def print_items(d: str = os.path.join(".", "example-directory")
                , indentation: str = '') -> None:
    """
    A sample program showing how to recurse on directories using os.

    Print the list of files and directories in directory <d>, recursively,
    prefixing each with the given <indentation>.
    """
    for filename in ordered_listdir(d):
        subitem = os.path.join(d, filename)
        if os.path.isdir(subitem):
            print(indentation + filename + os.sep)
            print_items(subitem, indentation + '  ')
        else:
            print(indentation + filename)


if __name__ == '__main__':
    # Put in a path for a directory, like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/dianeh/Documents/courses/csc148/assignments' (OSX)
    # to print the contents of that directory.
    # Tips:
    # . means the current directory
    # .. means the parent directory of the current directory
    # these can be useful for specifying relative paths and aren't
    # dependent on the full path, which is specific to you and your
    # file structure on your computer.
    # As a default, we've specified PATH to be for the example
    # directory provided in the starter code zip file.
    PATH = os.path.join(".", "example-directory")
    print(f"calling print_items on path: {PATH}, "
          f"with base name: {os.path.basename(PATH)}")
    print_items(PATH)
