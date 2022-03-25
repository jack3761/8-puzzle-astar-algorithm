
import numpy as np
import copy
import time

class Node():

    def __init__(self, grid=None, parent=None):
        self.parent = parent
        self.grid = grid      

        self.g = 0
        self.h = 0
        self.f = 0

#Manhattan distance heuristic, returns h value
def manhattan(node_grid, goal_grid):
    d = 0
    dx = 0
    dy = 0
    for i in range(9):
        #Find the coordinates of each tile on both grids
        current_coord = np.argwhere(node_grid == i)[0]
        goal_coord = np.argwhere(goal_grid == i)[0]
        
        #Find manhattan distance between tiles
        dx = abs(current_coord[0] - goal_coord[0])
        dy = abs(current_coord[1] - goal_coord[1])        
        d += dx + dy
    return d

#Misplaced tiles heuristic, returns h value
def misplaced(node_grid, goal_grid):
    d=0
    for i in range(9):
        #Compares whether each tile is in the same location on each grid
        current_coord = np.argwhere(node_grid == i)[0]
        goal_coord = np.argwhere(goal_grid == i)[0]
        if not np.array_equal(current_coord, goal_coord):
            d += 1
    return d

#Main a* algorithm, takes in start and end grid and chosen heuristic and returns the path of grids
def astar(start_grid, goal_grid, heuristic):

    open = []
    closed = []

    start_node = Node(start_grid)
    goal_node = Node(goal_grid)

    open.append(start_node)
    nodes_visited = 0
    while len(open) > 0:

        #Get current node
        current_count = 0
        current_node = open[0]
        for count, node in enumerate(open):
            #Find the node with the lowest f value
            if node.f < current_node.f:
                current_node = node
                current_count = count
        open.pop(current_count)
        closed.append(current_node)

        #Check if goal is reached
        if np.array_equal(current_node.grid, goal_node.grid):
            print("Found node")
            print("Nodes visited: " + str(nodes_visited))
            path = []
            current = current_node
            #Create the path from the start grid to the goal
            while current is not None:
                path.append(current.grid)
                current = current.parent
            return path[::-1]
            

        #Generate every possible child node for the current node
        children = []
        for translation in [(-1,0), (0,-1), (0,1), (1, 0)]:
            empty_position = np.argwhere(current_node.grid == 0)
            new_position = empty_position + translation

            #Check for invalid node
            if -1 in new_position or 3 in new_position:
                continue
                    
            new_node = Node(copy.copy(current_node.grid), current_node)

            #Shuffle tiles to create child of the current node
            new_node.grid[empty_position[0,0], empty_position[0,1]] = current_node.grid[new_position[0,0], new_position[0,1]]
            new_node.grid[new_position[0,0], new_position[0,1]] = 0

            children.append(new_node)

        for child in children:
            add = True
            for node in closed:
                if np.array_equal(child.grid, node.grid):
                    add = False
            
            #Find f value for each valid child
            child.g = current_node.g + 1
            if heuristic == 1:
                child.h = misplaced(child.grid, goal_grid)
            else:
                child.h = manhattan(child.grid, goal_grid)

            child.f = child.g + child.h

            for node in open:
                if np.array_equal(child.grid, node.grid) and child.g > node.g:
                    add = False

            #Add valid child to open list
            if add == True:
                open.append(child)
            nodes_visited += 1


#Starts the program and UI
def run():
    valid = False
    while valid == False:
        print("1. Use default grid")
        print("2. Enter grid")
        print("3. Run test cases")
        choice = input("Enter choice: ")
        if choice == "1":
            start_grid = np.array([[4,1,2], [0,8,7], [6,3,5]])
            goal_grid = np.array([[1,2,3], [4,5,6], [7,8,0]])
            valid = True
        elif choice == "2":
            print("Enter start grid one row at a time with the empty space being 0 (eg 012)")
            row1 = []
            row2 = [] 
            row3 = []
            input1 = input("Enter row 1: ")
            input2 = input("Enter row 2: ")
            input3 = input("Enter row 3: ")
            for i in range(3):
                row1.append(int(input1[i]))
                row2.append(int(input2[i]))
                row3.append(int(input3[i]))
            start_grid = np.array([row1, row2, row3])
            print("This is your start grid:")
            for i in range(3):
                print("")
                for j in range(3):
                    print(str(start_grid[i,j]) + " ", end='')
            print("Enter goal grid one row at a time with the empty space being 0 (eg 012)")
            row1 = []
            row2 = [] 
            row3 = []
            input1 = input("Enter row 1: ")
            input2 = input("Enter row 2: ")
            input3 = input("Enter row 3: ")
            for i in range(3):
                row1.append(int(input1[i]))
                row2.append(int(input2[i]))
                row3.append(int(input3[i]))
            goal_grid = np.array([row1, row2, row3])
            print("This is your goal grid:")
            for i in range(3):
                print("")
                for j in range(3):
                    print(str(goal_grid[i,j]) + " ", end='')
            valid = True
        elif choice == "3":
            print("Running test cases (WARNING: Some test cases take a very long time to run)")
            test()
        else:
            valid = False

    
    valid = False
    path = []
    while valid == False:
        print("Select heuristic")
        print("1. Misplaced tiles")
        print("2. Manhattan distance")
        choice = input("Enter choice: ")
        if choice == "1":
            start_time = time.time()
            path = astar(start_grid, goal_grid, 1)
            valid = True
        elif choice == "2":
            start_time = time.time()
            path = astar(start_grid, goal_grid, 2)
            valid = True
        else:
            valid = False

    print("Time taken: " + str(round(time.time()-start_time, 3)) + " seconds")
    print("Amount of moves: " + str(len(path) - 1))
    choice = input("Show path? (Y/N): ")
    if choice.upper() == "Y":
        for grid in path:
            print("")
            for i in range(3):
                print("")
                for j in range(3):
                    print(str(grid[i,j]) + " ", end='')


def test():
    states = []
    states.append(np.array([[2,8,3], [1,6,4], [7,0,5]])) #5 moves
    states.append(np.array([[1,0,2], [7,5,4], [8,6,3]])) #11 moves
    states.append(np.array([[8,3,5], [4,1,6], [2,7,0]])) #14 moves
    states.append(np.array([[4,1,2], [0,8,7], [6,3,5]])) #17 moves
    states.append(np.array([[7,2,4], [5,0,6], [8,3,1]])) #26 moves

    goals = []
    goals.append(np.array([[1,2,3], [8,0,4], [7,6,5]]))
    goals.append(np.array([[1,2,3], [4,5,6], [7,8,0]]))
    goals.append(np.array([[1,2,3], [8,0,4], [7,6,5]]))
    goals.append(np.array([[1,2,3], [4,5,6], [7,8,0]]))
    goals.append(np.array([[0,1,2], [3,4,5], [6,7,8]]))

    total_start = time.time()
    for count, state in enumerate(states):

        #Misplaced
        print("Test " + str(count))
        print("Misplaced: ")
        start_time = time.time()
        path = astar(state, goals[count], 1)
        print("Time taken: " + str(round(time.time()-start_time, 3)) + " seconds")
        print("Amount of moves: " + str(len(path) - 1))

        print("")
        #Manhattan
        print("Manhattan: ")
        start_time = time.time()
        path = astar(state, goals[count], 2)
        print("Time taken: " + str(round(time.time()-start_time, 3)) + " seconds")
        print("Amount of moves: " + str(len(path) - 1))
        
        print("")
        print("")

run()
