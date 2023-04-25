# Treemaps

## Introduction
> A treemap Links to an external site. is a visualisation technique to show a tree’s structure according to the weights (or sizes) of its data values. It uses rectangles to show subtrees, scaled to reflect the proportional sizes of each piece of data. 

Treemaps are used in many contexts. Among the more popular uses are news headlines, various kinds of financial information, and computer disk usage.

## Treemap Algorithms
- Initialize the tree structure: develop a `TMTree` class to define the basic functionality required by the provided treemap visualizer.
- The Treemap program operates on the data tree and a 2-D window to fill with the visualization, and generates a list of rectangles to display, based on the tree structure and `data_size` attribute for each node.
- For all rectangles in this program, we’ll use the pygame representation of a rectangle, which is a tuple of four integers `(x, y, width, height)`, where `(x, y)` represents the upper-left corner of the rectangle. Note that in pygame, the origin is in the upper-left corner and the y-axis points down. So, the lower-right corner of a rectangle has coordinates (x + width, y + height). Each unit on both axes is a pixel on the screen.

## Treemap Visualizations
- The treemap visualizer can resize, move rectangles, and manipulate the displayed-tree.
- generic treemap: ![generic treemap](https://github.com/Bilin22/Treemaps/blob/main/generic%20treemap.png)
- file system treemap: ![file system treemap](https://github.com/Bilin22/Treemaps/blob/main/file%20system%20treemap.png)
- chess treemap: ![chess treemap](https://github.com/Bilin22/Treemaps/blob/main/chess%20treemap.png)

## Acknowledgements
The starter code of this project is provided by:

University of Toronto

CSC148: Introduction to Computer Science - Winter 2023

Professor: Diane Horton

