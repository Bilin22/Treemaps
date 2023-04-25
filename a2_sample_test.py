"""Assignment 2 - Starter Tests

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

Authors: David Liu, Bogdan Simion, Diane Horton, Sophia Huynh, Tom Ginsberg,
Jonathan Calver, Jacqueline Smith, and Misha Schwartz

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 David Liu, Bogdan Simion, Diane Horton, Sophia Huynh,
Jonathan Calver, Jacqueline Smith, and Misha Schwartz

=== Module Description ===
This module contains sample tests for Assignment 2.
The tests use the provided example-directory.
This test suite is _very_ small. You should plan to add to it to
thoroughly test your code.

IMPORTANT NOTES:
    - Depending on your operating system or other system settings, you
      may end up with incorrect results when running the provided doctests
      and pytests that rely on the sizes of files stored on your computer.
      Make sure to run the self-tests on MarkUs, once they are
      posted, to confirm your code runs correctly there.
"""
import os
import pytest
from hypothesis import given
from hypothesis.strategies import integers
from typing import Tuple
from tm_trees import DIRECTORYTREE_EXAMPLE_RESULT, FileTree, TMTree, \
    DirectoryTree, dir_tree_from_nested_tuple, path_to_nested_tuple, \
    ChessTree, get_worksheet_tree, moves_to_nested_dict, \
    OperationNotSupportedError

# This should be the path to the "workshop" directory in the sample data
# included in the zip file for this assignment.
EXAMPLE_PATH = os.path.join('example-directory', 'workshop')


##############################################################################
# Helpers
##############################################################################
def is_valid_colour(colour: Tuple[int, int, int]) -> bool:
    """
    Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


###########################################
# TMTree provided basic testing
###########################################
class TestTMTree:

    def test_init_doctest(self) -> None:
        t1 = TMTree('B', [], 5)
        assert t1.rect is None
        assert t1.data_size == 5
        t2 = TMTree('A', [t1], 1)
        assert t2.rect is None
        assert t2.data_size == 6

    def test_is_displayed_tree_leaf_doctest(self) -> None:
        t1 = TMTree('B', [], 5)
        assert t1.is_displayed_tree_leaf()
        t2 = TMTree('A', [t1], 1)
        assert t1.is_displayed_tree_leaf()
        assert not t2.is_displayed_tree_leaf()

    def test_update_rectangles_doctest(self) -> None:
        t1 = TMTree('B', [], 5)
        t2 = TMTree('A', [t1], 1)
        t2.update_rectangles((0, 0, 100, 200))
        assert t2.rect == (0, 0, 100, 200)
        assert t1.rect == (0, 0, 100, 200)
        s1 = TMTree('C1', [], 5)
        s2 = TMTree('C2', [], 15)
        t3 = TMTree('C', [s1, s2], 1)
        t3.update_rectangles((0, 0, 100, 200))
        assert s1.rect == (0, 0, 100, 50)
        assert s2.rect == (0, 50, 100, 150)
        assert t3.rect == (0, 0, 100, 200)

    def test_get_rectangles_doctest(self) -> None:
        t1 = TMTree('B', [], 5)
        t2 = TMTree('A', [t1], 1)
        t2.update_rectangles((0, 0, 100, 200))
        assert t2.get_rectangles()[0][0] == (0, 0, 100, 200)
        s1 = TMTree('C1', [], 5)
        s2 = TMTree('C2', [], 15)
        t3 = TMTree('C', [s1, s2], 1)
        t3.update_rectangles((0, 0, 100, 200))
        rectangles = t3.get_rectangles()
        assert rectangles[0][0] == (0, 0, 100, 50)
        assert rectangles[1][0] == (0, 50, 100, 150)

    def test_get_tree_at_position_doctest(self) -> None:
        t1 = TMTree('B', [], 5)
        t2 = TMTree('A', [t1], 1)
        t2.update_rectangles((0, 0, 100, 200))
        assert t1.get_tree_at_position((10, 10)) is t1
        assert t2.get_tree_at_position((10, 10)) is t1
        assert t2.get_tree_at_position((500, 500)) is None
        s1 = TMTree('C1', [], 5)
        s2 = TMTree('C2', [], 15)
        t3 = TMTree('C', [s1, s2], 1)
        t3.update_rectangles((0, 0, 100, 200))
        assert t3.get_tree_at_position((0, 0)) is s1
        assert t3.get_tree_at_position((100, 100)) is s2

    def test_expand_doctest(self) -> None:
        s1 = TMTree('C1', [], 5)
        s2 = TMTree('C2', [], 15)
        t3 = TMTree('C', [s1, s2], 1)
        t3._expanded = False
        assert s1.is_displayed_tree_leaf() is False
        assert t3.expand() is s1
        assert s1.is_displayed_tree_leaf() is True

    def test_expand_all_doctest(self) -> None:
        d1 = TMTree('C1', [], 5)
        d2 = TMTree('C2', [d1], 1)
        d3 = TMTree('C', [d2], 1)
        d3._expanded = False
        d2._expanded = False
        assert d1.is_displayed_tree_leaf() is False
        assert d2.is_displayed_tree_leaf() is False
        assert d3.expand_all() is d1
        assert d1.is_displayed_tree_leaf() is True
        assert d2.is_displayed_tree_leaf() is False

    def test_collapse_doctest(self) -> None:
        d1 = TMTree('C1', [], 5)
        d2 = TMTree('C2', [d1], 1)
        assert d1.is_displayed_tree_leaf() is True
        assert d2.is_displayed_tree_leaf() is False
        assert d1.collapse() is d2
        assert d1.is_displayed_tree_leaf() is False
        assert d2.is_displayed_tree_leaf() is True

    def test_collapse_all_doctest(self) -> None:
        d1 = TMTree('C1', [], 5)
        d2 = TMTree('C2', [d1], 1)
        d3 = TMTree('C', [d2], 1)
        assert d1.is_displayed_tree_leaf() is True
        assert d1.collapse_all() is d3
        assert d1.is_displayed_tree_leaf() is False
        assert d2.is_displayed_tree_leaf() is False
        assert d3.is_displayed_tree_leaf() is True

    def test_move_doctest(self) -> None:
        s1 = TMTree('C1', [], 5)
        s2 = TMTree('C2', [], 15)
        t3 = TMTree('C', [s1, s2], 1)
        t3.update_rectangles((0, 0, 100, 200))
        assert s1.is_displayed_tree_leaf() is True
        assert s2.is_displayed_tree_leaf() is True
        s2.move(s1)
        assert s2.rect == (0, 0, 100, 200)
        assert s1.data_size == 20
        assert t3.data_size == 21
        assert t3.get_tree_at_position((0, 0)) is s2
        assert s1.is_displayed_tree_leaf() is False
        assert s2.is_displayed_tree_leaf() is True

    def test_change_size_doctest(self) -> None:
        s1 = TMTree('C1', [], 5)
        s2 = TMTree('C2', [], 15)
        t3 = TMTree('C', [s1, s2], 1)
        t3.update_rectangles((0, 0, 100, 200))
        s2.change_size(-2 / 3)
        assert s2.data_size == 5
        assert t3.data_size == 11
        assert s2.rect == (0, 100, 100, 100)

    def test_get_path_string_doctest(self) -> None:
        d1 = TMTree('C1', [], 5)
        d2 = TMTree('C2', [d1], 1)
        d3 = TMTree('C', [d2], 1)
        assert d3.get_path_string() == 'C(7) None'
        assert d1.get_path_string() == 'C | C2 | C1(5) None'

    def test_worksheet_rectangles(self) -> None:
        worksheet_tree = get_worksheet_tree()
        assert worksheet_tree.data_size == 60
        assert worksheet_tree.rect == (0, 0, 55, 30)
        rectangles = worksheet_tree.get_rectangles()
        shape_only = [rectangle[0] for rectangle in rectangles]  # skip colours
        expected_rectangles = [(0, 0, 20, 24),
                               (20, 0, 10, 24),
                               (0, 24, 30, 6),
                               (30, 0, 15, 12),
                               (30, 12, 15, 12),
                               (30, 24, 15, 6),
                               (45, 0, 10, 30)]
        assert shape_only == expected_rectangles


###########################################
# _FileTree and DirectoryTree provided basic testing
###########################################
class TestFileSystem:

    def test_directorytree_class_doctest(self) -> None:
        my_dir = dir_tree_from_nested_tuple((
            (".", [
                ("documents", [("report.pdf", 13), ("data.xlsx", 10)]),
                ("images", [("vacation", [("beach.png", 5)])]),
                ("my_song.mp3", 14),
                ("empty_dir", [])
            ])
        ))
        assert my_dir.data_size == 47
        assert len(my_dir._subtrees) == 4
        documents = my_dir._subtrees[0]
        assert isinstance(documents, DirectoryTree)
        assert isinstance(documents, TMTree)
        images = my_dir._subtrees[1]
        empty_dir = my_dir._subtrees[3]
        report_file = documents._subtrees[0]
        data_file = documents._subtrees[1]
        assert isinstance(data_file, FileTree)
        assert isinstance(data_file, TMTree)
        assert documents.data_size == 24
        assert images.data_size == 7

        assert str(my_dir) == DIRECTORYTREE_EXAMPLE_RESULT

        expected_str = "./documents (directory)".replace("/", os.path.sep)
        assert str(documents.get_path_string()) == expected_str

        expected_str = "./documents/data.xlsx (file)".replace("/", os.path.sep)
        assert str(data_file.get_path_string()) == expected_str

        my_dir.update_rectangles((0, 0, 200, 400))

        with pytest.raises(OperationNotSupportedError):
            data_file.move(report_file)

        expected_str = "./documents/data.xlsx (file)".replace("/", os.path.sep)
        assert str(data_file.get_path_string()) == expected_str

        data_file.move(empty_dir)
        expected_str = "./empty_dir/data.xlsx (file)".replace("/", os.path.sep)
        assert str(data_file.get_path_string()) == expected_str

    def test_path_to_nested_tuple_doctest(self) -> None:
        path = os.path.join("example-directory", "workshop", "prep")
        rslt = path_to_nested_tuple(path)
        assert rslt[0] == 'prep'
        assert rslt[1] == [('images', [('Cats.pdf', 17)]), ('reading.md', 7)]

    def test_example_data(self) -> None:
        """
        Test that the root of the tree at the 'workshop' directory is correct.
        """
        nested_tuple = path_to_nested_tuple(EXAMPLE_PATH)
        tree = dir_tree_from_nested_tuple(nested_tuple)
        assert tree._name == 'workshop'
        assert tree._parent_tree is None
        assert tree.data_size == 162
        assert is_valid_colour(tree._colour)
        assert len(tree._subtrees) == 3
        for subtree in tree._subtrees:
            # Note the use of is rather than ==.
            # This checks ids rather than values.
            assert subtree._parent_tree is tree

    @given(integers(min_value=100, max_value=1000),
           integers(min_value=100, max_value=1000),
           integers(min_value=100, max_value=1000),
           integers(min_value=100, max_value=1000))
    def test_single_directory_rectangles(self, x, y, width, height) -> None:
        """
        Test that the correct rectangle is produced for a single directory, for
        a range of possible rect parameter values passed to update_rectangles.
        """
        tree = dir_tree_from_nested_tuple(('empty_dir', []))
        tree.update_rectangles((x, y, width, height))
        rects = tree.get_rectangles()

        # This should be just a single rectangle and colour returned.
        assert len(rects) == 1
        rect, colour = rects[0]
        assert rect == (x, y, width, height)
        assert is_valid_colour(colour)

    def test_example_data_rectangles(self) -> None:
        """
        Test that the correct rectangles are produced for
        the EXAMPLE_PATH directory.
        """
        nested_tuple = path_to_nested_tuple(EXAMPLE_PATH)
        tree = dir_tree_from_nested_tuple(nested_tuple)

        tree.update_rectangles((0, 0, 200, 100))
        rects = tree.get_rectangles()

        # IMPORTANT: This test should pass when you have completed Task 2.
        assert len(rects) == 6

        # Here, we illustrate the correct order of the returned rectangles.
        actual_rects = [r[0] for r in rects]
        expected_rects = [(0, 0, 94, 4), (0, 4, 94, 28), (0, 32, 94, 68),
                          (94, 0, 73, 100), (167, 0, 33, 72), (167, 72, 33, 28)]

        assert len(actual_rects) == len(expected_rects)
        for i in range(len(actual_rects)):
            assert actual_rects[i] == expected_rects[i]


###########################################
# ChessTree provided basic testing
###########################################

class TestChessTree:

    def test_moves_to_nested_dict_doctest(self) -> None:
        assert moves_to_nested_dict([[]]) == {}
        assert moves_to_nested_dict([]) == {}
        assert moves_to_nested_dict([['a'], []]) == {('a', 1): {}}
        d = moves_to_nested_dict([["a", "b", "c"],
                                  ["a", "b"], ["d", "e"], ["d", "e"]])
        assert d == {('a', 0): {('b', 1): {('c', 1): {}}},
                     ('d', 0): {('e', 2): {}}}
        d = moves_to_nested_dict([["a", "b", "c"], ["a", "b"],
                                  ["d", "e", "a"], ["d", "e"]])
        assert d == {('a', 0): {('b', 1): {('c', 1): {}}},
                     ('d', 0): {('e', 1): {('a', 1): {}}}}

    def test_init_doctest(self) -> None:
        ct = ChessTree({('e2e4', 0): {('e7e5', 1): {}}})
        assert ct.is_displayed_tree_leaf() is False
        assert ct.data_size == 1
        assert ct.rect is None
        assert str(ct) == "- | (1) None\n" \
                          "    e2e4 | (1) None\n" \
                          "        e7e5(1) None"


if __name__ == '__main__':
    pytest.main(['a2_sample_test.py'])
