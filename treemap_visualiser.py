"""Assignment 2: Treemap Visualiser

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Bogdan Simion, Diane Horton, Sophia Huynh, Tom Ginsberg,
Jonathan Calver, Jacqueline Smith, and Misha Schwartz

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 David Liu, Bogdan Simion, Diane Horton, Sophia Huynh,
Jonathan Calver, Jacqueline Smith, and Misha Schwartz

=== Module Description ===
This module contains the main program code for the treemap visualisation.
It is responsible for initializing an instance of TMTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import json
import os
from typing import Optional
import pygame

from tm_trees import TMTree, path_to_nested_tuple
from tm_trees import ChessTree, dir_tree_from_nested_tuple, \
    moves_to_nested_dict, get_worksheet_tree
from tm_trees import OperationNotSupportedError

# Screen dimensions and coordinates
# You may adjust these values as you'd like.
# When running the visualizer, you can also manually resize the window.
WIDTH = 550  # 550 this size is so the worksheet demo displays nicely
HEIGHT = 334  # 330 + FONT_OFFSET
FONT_HEIGHT = 30  # The height of the text display.
FONT_OFFSET = 4  # offset to (roughly) center text display
FONT_ROWS = 1  # Initially, how many rows of text we leave room for in display

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'

SELECTED_HIGHLIGHT = 5  # width of rectangle around the selected rectangle
HOVER_HIGHLIGHT = 2  # width of rectangle around the hovered rectangle

# noinspection PyUnresolvedReferences
WHITE = pygame.color.THECOLORS['white']
# noinspection PyUnresolvedReferences
BLACK = pygame.color.THECOLORS['black']

ANTI_ALIAS = True

# the factor used when changing the size of a node
DELTA = 0.01

# mapping of pygame key constants to the actions they correspond to.
KEY_MAP = {pygame.K_m: 'm = move',
           pygame.K_UP: 'UP = increase size',
           pygame.K_DOWN: 'DOWN = decrease size',
           pygame.K_e: 'e = expand',
           pygame.K_a: 'a = expand all',
           pygame.K_c: 'c = collapse',
           pygame.K_x: 'x = collapse all',
           pygame.K_o: 'o = open'}


def get_screen_rect(screen: pygame.Surface,
                    font_rows: int,
                    with_text_display: bool = False) -> tuple[int, int,
                                                              int, int]:
    """
    Return the pygame rect that fills the <screen>.

    If <with_text_display> is True (default is False), then the height
    is reduced to account for the space taken to display the text at the bottom
    of the display.

    <font_rows> determines how much height is used to display the text at
    the bottom.
    """
    if with_text_display:
        return 0, 0, screen.get_width(), screen.get_height()
    return (0, 0, screen.get_width(),
            screen.get_height() - (FONT_HEIGHT + FONT_OFFSET) * font_rows)


def run_visualisation(tree: TMTree, name: str) -> None:
    """
    Display an interactive graphical display of the treemap for <tree>.

    The title of the window is set to <name>.
    """

    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    pygame.display.set_caption(name)

    # Render the initial display of the treemap.
    tree.update_rectangles(get_screen_rect(screen, FONT_ROWS))
    render_display(screen, tree, None, None)

    # Start an event loop to respond to events.
    event_loop(screen, tree, FONT_ROWS)


def render_display(screen: pygame.Surface, tree: Optional[TMTree],
                   selected_node: Optional[TMTree] = None,
                   hover_node: Optional[TMTree] = None) -> int:
    """
    Render a treemap and text information to the given <screen> for the given
    <tree>, and return the number of rows used to display the text of the
    currently selected node.

    The constants TREEMAP_HEIGHT and FONT_HEIGHT are used to divide the
    screen vertically into the treemap and the text information for the selected
    rectangle.

    The <selected_node>, if not None, is highlighted in the visualization.

    The <hover_node>, if not None, is also highlighted in the visualization.
    """
    # First, clear the screen
    pygame.draw.rect(screen, BLACK,
                     get_screen_rect(screen, FONT_ROWS, True))

    # Note: this should work after you have completed Task 2
    try:
        font_rows = _render_text(screen, _get_display_text(selected_node))
        tree.update_rectangles(get_screen_rect(screen, font_rows))

        subscreen = screen.subsurface(get_screen_rect(screen, font_rows))

        # get the rectangles and draw them to the screen
        for rect, colour in tree.get_rectangles():
            pygame.draw.rect(subscreen, colour, rect)

        # add the selected and hover rectangles if necessary
        if selected_node is not None:
            pygame.draw.rect(subscreen, WHITE, selected_node.rect,
                             SELECTED_HIGHLIGHT)
        if hover_node is not None:
            pygame.draw.rect(subscreen, WHITE, hover_node.rect,
                             HOVER_HIGHLIGHT)

    except Exception as e:
        print("Possibly an error in Task 2 code. See detailed error message.")
        raise e

    # This must be called *after* all other pygame functions have run
    # in order to update the screen.
    pygame.display.flip()
    return font_rows


def _render_text(screen: pygame.Surface, text: str) -> int:
    """
    Render <text> at the bottom of the <screen>.
    Return the number of rows needed to display the <text>.
    """

    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 2 * FONT_OFFSET)

    # fix this...
    text_width, _ = font.size(text)  # _ since we ignore the text_height
    height = int(1 + text_width / screen.get_width())
    n_char = int(1 + len(text) / height)

    font_rows = height
    for h in range(height):
        offset = (font_rows - h) * (FONT_HEIGHT + FONT_OFFSET/2)
        text_pos = (0, screen.get_height() - offset)
        text_surface = font.render(text[h * n_char:(h + 1) * n_char],
                                   ANTI_ALIAS,
                                   WHITE)
        screen.blit(text_surface, text_pos)
    return font_rows


def event_loop(screen: pygame.Surface, tree: TMTree, font_rows: int) -> None:
    """Respond to events (mouse clicks, key presses) and update the <screen>.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the <tree> itself, updating the
    display if necessary.

    <font_rows> tells us how many rows of the display to use to show the
    text for the currently selected node.

    This loop ends only when the user closes the window.
    """
    selected_node = None
    hover_node = None

    while True:
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return

        # handle resize event...
        if event.type == pygame.WINDOWRESIZED:
            print(f"window resized: {get_screen_rect(screen, font_rows)}")
            # this should work once you have completed Task 2
            tree.update_rectangles(get_screen_rect(screen, font_rows))

        # get the hover position and the corresponding node
        old_hover_node = hover_node
        hover_node = tree.get_tree_at_position(pygame.mouse.get_pos())

        if hover_node != old_hover_node:
            # Update display
            if hover_node:
                print(f"hover node changed to {hover_node.get_path_string()}")
            font_rows = render_display(screen, tree, selected_node, hover_node)

        if event.type == pygame.MOUSEBUTTONUP:
            selected_node = _handle_click(event.button, event.pos,
                                          tree, selected_node)
            # Update display
            font_rows = render_display(screen, tree, selected_node, hover_node)

        elif event.type == pygame.KEYUP and selected_node is not None:
            if event.key in KEY_MAP:
                print(f"[{KEY_MAP.get(event.key)}]")
                sn = selected_node
                selected_node = execute_task_4_expand_collapse_actions(event,
                                                                       sn)
                execute_task_4_other_actions(event, hover_node, selected_node)

                execute_task_6_open_action(event, selected_node)
            else:
                print(f"Unrecognized key pressed, recognized keys are:")
                for value in KEY_MAP.values():
                    print(value)

            # Update display
            font_rows = render_display(screen, tree, selected_node, hover_node)
        elif event.type == pygame.KEYUP and selected_node is None:
            print(f"key pressed, but no node selected!")


def execute_task_6_open_action(event: pygame.event.Event,
                               selected_node: TMTree) -> None:
    """
    Process <event> and execute the relevant method of <selected_node>.
    """
    try:
        # "open" the selected node if this operation is supported
        # for this type of tree. Note, this will only do something
        # for the ChessTree in this assignment.
        if event.key == pygame.K_o and hasattr(selected_node,
                                               'open_page'):
            print("opening...")
            selected_node.open_page()
    except Exception as e:
        print("Possibly an error in Task 6 code. See detailed error message.")
        raise e


def execute_task_4_expand_collapse_actions(event: pygame.event.Event,
                                           selected_node: TMTree) -> TMTree:
    """
    Process <event> and execute the relevant method of <selected_node>.
    """
    try:
        old_selected = selected_node
        if event.key == pygame.K_e:
            selected_node = selected_node.expand()

        elif event.key == pygame.K_a:
            selected_node = selected_node.expand_all()

        elif event.key == pygame.K_c:
            selected_node = selected_node.collapse()

        elif event.key == pygame.K_x:
            selected_node = selected_node.collapse_all()

        if old_selected is not selected_node:
            print(f"selected node is now {selected_node.get_path_string()}")

    except Exception as e:
        print("Possibly an error in Task 4 or later code."
              " See detailed error message.")
        raise e
    return selected_node


def execute_task_4_other_actions(event: pygame.event.Event,
                                 hover_node: Optional[TMTree],
                                 selected_node: TMTree) -> None:
    """
        Process <event> and execute the relevant method of <selected_node>,
        with <hover_node> as the argument if required.
    """
    try:
        if event.key == pygame.K_UP:
            selected_node.change_size(DELTA)
        elif event.key == pygame.K_DOWN:
            selected_node.change_size(-DELTA)
        elif event.key == pygame.K_m and hover_node:
            selected_node.move(hover_node)
    except OperationNotSupportedError:
        operation = f"[{KEY_MAP.get(event.key)}]"
        print(f"Node of type {type(selected_node)} says it doesn't support "
              f"operation {operation}")
    except Exception as e:
        print(
            "Possibly an error in Task 4 or later code."
            " See detailed error message.")
        raise e


def _handle_click(button: int, pos: tuple[int, int], tree: TMTree,
                  old_selected_leaf: Optional[TMTree]) -> Optional[TMTree]:
    """Return the new selected node after handling the mouse event specified
    by <button> at position <pos>.

    Based on the click, the appropriate actions are performed on <tree>.

    Note: we need to use <old_selected_leaf> to handle the case when the
    selected leaf is left-clicked again.
    """
    # this should work once you have completed Task 3
    if button == pygame.BUTTON_LEFT:
        # handle left mouse click to select a node
        selected_leaf = tree.get_tree_at_position(pos)

        if selected_leaf is None:
            return old_selected_leaf
        elif selected_leaf is old_selected_leaf:
            print(f"unselected {selected_leaf.get_path_string()}")
            return None
        else:
            print(f"selected {selected_leaf.get_path_string()}")
            return selected_leaf
    # right click or any other click does nothing
    return old_selected_leaf


def _get_display_text(leaf: Optional[TMTree]) -> str:
    """
    Return the display text of this <leaf> or an empty string if <leaf> is None.
    """
    if leaf is None:
        return ''
    return f'{leaf.get_path_string()} ({leaf.data_size})'


def run_treemap_file_system(path: str) -> None:
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a directory.

    If the provided <path> violates this precondition, this code will raise
    a ValueError.
    """
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a path to a valid directory!")

    file_tree_tuple = path_to_nested_tuple(path)
    file_tree = dir_tree_from_nested_tuple(file_tree_tuple)
    run_visualisation(file_tree, "file system visualizer")


# the names of the three chess data sets
CHESS_DATA_SETS = [f"wgm_{num_games}.json" for num_games in [10, 200, 999]]


def run_treemap_chess() -> None:
    """Run a treemap visualization for chess games.
    """
    # you can choose which data set to load or make your own!
    with open(CHESS_DATA_SETS[1]) as file:
        chess_moves = json.load(file)
    chess_dict = moves_to_nested_dict(chess_moves)
    chess_tree = ChessTree(chess_dict)
    run_visualisation(chess_tree, "chess tree visualizer")


def run_treemap_generic() -> None:
    """
    Run a treemap visualization for a generic treemap.
    """
    # Feel free to try different TMTree structures, we have just provided a
    # couple examples to get you started.
    # treemap = TMTree("A", [TMTree("B", [], 5),
    #                        TMTree("C", [TMTree("C1", [], 5),
    #                                     TMTree("C2", [], 5),
    #                                     TMTree("C3", [], 5)], 0)], 0)
    treemap = get_worksheet_tree()
    run_visualisation(treemap, "generic TMTree visualizer")


if __name__ == '__main__':
    # To check your work, you can try running the visualizer.
    # Reminder, you are encouraged to modify this while trying out your code.

    RUN_OPTIONS = ['TMTree', 'DirectoryTree', 'ChessTree']
    which = RUN_OPTIONS[2]
    # change the line above to choose which type of tree to visualize.

    if which == RUN_OPTIONS[0]:
        # To check your work for TMTree, try running this.
        print("running generic treemap visualizer!")
        run_treemap_generic()
    elif which == RUN_OPTIONS[1]:
        # To check your work for Task 5, try running this.
        # Feel free to try different paths.
        PATH = os.path.join(".", "example-directory")
        print(f"running file system treemap visualizer on path: {PATH}")
        run_treemap_file_system(PATH)
    elif which == RUN_OPTIONS[2]:
        # To check your work for Task 6, try running this.
        print("running chess treemap visualizer!")
        run_treemap_chess()
    else:
        print("invalid option chosen!")
