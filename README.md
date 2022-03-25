# 8-puzzle solved with A* algorithm
A* algorithm to solve any given 8-puzzle problem with a chosen heuristic

## Installation

This program only requires the installation of numpy which can be installed by doing:

pip install numpy

## Getting started

Run the python script and there are three options, which are to use a default grid, enter a grid or run test cases.

Selecting the default grid will give you the option to choose a heuristic out of misplaced tiles or manhattan distance. It should be noted that using misplaced tiles can take a significant amount of time longer than manhattan distance. The program will then run and show the amount of time taken and moves made. There is then the option to display the path taken by the algorithm.

To enter a grid, you will then be required to enter the grid one line at a time. As this program is made to demonstrate the algorithm, entering an invalid grid will result in an error.

There is also the option to run the test cases, which will run 5 test grids with both heuristics, each with increasing difficulty. It should be noted here that the harder grids can take a very long time to run with the manhattan distance even with a powerful CPU.
