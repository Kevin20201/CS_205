import numpy as np
import sys
##### Referenced Geeks for Geeks on how to call deepcopy() https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
import copy
##### Referenced The Python Standard Library https://docs.python.org/3/library/queue.html
from queue import PriorityQueue
from queue import Queue

##### Referenced StackOverflow https://stackoverflow.com/questions/2482602/a-general-tree-implementation to see how to create a generic tree structure
class Tree:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

    def get_parent(self):
        return self.parent
    
    def get_state(self):
        return self.state

##### Referenced The Python Tutorial https://docs.python.org/3/tutorial/classes.html to understand how to write a probelm class
class Problem:
    def __init__(self, initial_state, goal_state, puzzle_size, heuristic, parent):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.size = puzzle_size
        self.heuristic = heuristic
        
    def node_weight(self, puzzle):
        weight = 0
        # uniform cost search
        if (self.heuristic == 1):
            # For this problem it is considered breath first search
            # Referenced Professor Eamon Keogh's slide deck 3__Heuristic Search 2 slide 4
            return 0
        # misplaced tile heuristic
        elif (self.heuristic == 2):
            for row in range(self.size):
                for column in range(self.size):
                    # Check if location of value is same as goal state (expected)
                    if puzzle[row][column] != self.goal_state[row][column]:
                        weight+=1
            return weight
        #manhattan Distance heuristic\n")
        elif (self.heuristic == 3):
            for row in range(self.size):
                for column in range(self.size):
                    value = puzzle[row][column]
                    # The row for the value lies in the multiplplicity of the size value -1 because of indexing
                    correct_row = int(value / self.size)
                    # The column is the remainder of the value from the size so we take the mod
                    correct_column = int(value % self.size)
                    # If value is the blank spot, then row is set at the bottom
                    if value == 0:
                        correct_row=self.size
                    # Adjustment for indexing on row and special cases for modulo 0 values
                    if correct_column == 0:
                        correct_column = self.size-1
                        correct_row-=1
                    # Adjustment for indexing
                    else:
                        correct_column-=1
                    # Calculate the Manhattan Distance of row and column
                    weight_row = abs(row - correct_row)
                    weight_column = abs(column - correct_column)
                    weight += (weight_row + weight_column)
            return weight
        return weight
    
##### Referenced Professor Eamon Keogh's operators variable naming convention from Slide deck 2__Blind Search_part1 slide 27
# Move blank left swaps blank with the value on its left
def move_blank_left(node, row, column):
    # Make copy so we dont overwrite
    puzzle = copy.deepcopy(node)
    blank = puzzle[row][column]
    temp = puzzle[row][column-1]
    puzzle[row][column-1] = blank
    puzzle[row][column] = temp
    return puzzle

# Move blank left swaps blank with the value on its right
def move_blank_right(node, row, column):
    # Make copy so we dont overwrite
    puzzle = copy.deepcopy(node)
    blank = puzzle[row][column]
    temp = puzzle[row][column+1]
    puzzle[row][column+1] = blank
    puzzle[row][column] = temp
    return puzzle

# Move blank left swaps blank with the value above
def move_blank_up(node, row, column):
    # Make copy so we dont overwrite
    puzzle = copy.deepcopy(node)
    blank = puzzle[row][column]
    temp = puzzle[row-1][column]
    puzzle[row-1][column] = blank
    puzzle[row][column] = temp
    return puzzle

# Move blank left swaps blank with the value below
def move_blank_down(node, row, column):
    # Make copy so we dont overwrite
    puzzle = copy.deepcopy(node)
    blank = puzzle[row][column]
    temp = puzzle[row+1][column]
    puzzle[row+1][column] = blank
    puzzle[row][column] = temp
    return puzzle  

def expand(node, problem, queue, states):
    # First find where the blank is located
    blank_position = None
    puzzle = None
    for row in range(problem.size):
        for column in range(problem.size):
            # If value is 0 (blank) then return its position
            if node[1][row][column] == 0:
                blank_position = (row, column)
                break
        if blank_position is not None:
            break
    # Check valid operators then perform the move if valid
    # Corner Cases: Top Left, Top Right, Bottom Left, Bottom Right
    if blank_position == (0,0):
        puzzle = move_blank_right(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_down(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    elif blank_position == (0,problem.size-1):
        puzzle = move_blank_left(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_down(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    elif blank_position == (problem.size-1,0):
        puzzle = move_blank_right(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            # print("sdfsdfd")
            # print(node[1])
            # print(copy.deepcopy(node[2]).get_state())
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_up(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    elif blank_position == (problem.size-1,problem.size-1):
        puzzle = move_blank_left(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_up(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    # Border Cases: Top, Left Side, Right Side, Bottom
    elif blank_position[0] == 0:
        puzzle = move_blank_left(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_right(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_down(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    elif blank_position[1] == 0:
        puzzle = move_blank_up(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_right(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_down(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    elif blank_position[1] == problem.size-1:
        puzzle = move_blank_up(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_left(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_down(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    elif blank_position[0] == problem.size-1:
        puzzle = move_blank_up(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_left(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_right(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    # For the rest all four operations are valid
    else:
        puzzle = move_blank_up(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_left(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_right(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
        puzzle = move_blank_down(node[1], blank_position[0], blank_position[1])
        if puzzle not in states:
            states.append(puzzle)
            queue.put((problem.node_weight(puzzle), puzzle, Tree(puzzle, copy.deepcopy(node[2]))))
    return

def print_node(puzzle, problem):
    print_puzzle = '['
    for row in range(problem.size):
        print_puzzle += '['
        for column in range(problem.size):
            print_puzzle += str(puzzle[row][column])
            print_puzzle += ' '
        print_puzzle = print_puzzle[:-1] + ']\n'
    print_puzzle = print_puzzle[:-1] + ']\n'
    print(print_puzzle)
    return

def print_solution(node, solution_depth):
    traverse_node = node[2]
    while traverse_node.get_parent() is not None:
        puzzle = traverse_node.get_state()
        print_puzzle = '['
        for row in range(problem.size):
            print_puzzle += '['
            for column in range(problem.size):
                print_puzzle += str(puzzle[row][column])
                print_puzzle += ' '
            print_puzzle = print_puzzle[:-1] + ']\n'
        print_puzzle = print_puzzle[:-1] + ']\n'
        print(print_puzzle)
        traverse_node = traverse_node.get_parent()
        solution_depth+=1
    return solution_depth

##### Main "Driver" Program from Professor Eamon Keogh's slides
# function general-search(problem, QUEUEING-FUNCTION)
# nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
# loop do
# if EMPTY(nodes) then return "failure"
# node = REMOVE-FRONT(nodes)
# if problem.GOAL-TEST(node.STATE) succeeds then return node
# nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
# end

# Recall that Uniform Cost Search is just A* with h(n) hardcoded to equal zero.
# Quote above was taken from Professor Eamon Keogh's Project_1_The_Eight_Puzzle_CS_205_2024.pdf handout
def a_star_search(problem, queue):
    # Keep track of repeated states
    ##### Referenced w2school https://www.w3schools.com/python/python_sets.asp on how to use sets in python
    states = [problem.initial_state]
    # Inserts initial_state in the queue as a tuple (weight, puzzle)
    queue.put((problem.node_weight(problem.initial_state), problem.initial_state, Tree(problem.initial_state, None)))
    node = None
    max_queue_size = max(queue.qsize(), 0)
    total_nodes_traversed = 0
    solution_depth = 0
    while True:
        # If queue is empty then there is no solution to the puzzle
        if queue.empty():
            print("FAILURE")
            return
        # Otherwise we continue to retrieve from the queue
        node = queue.get()
        total_nodes_traversed += 1
        print_node(node[1], problem)
        # print(node)
        if problem.goal_state == node[1]:
            print("SUCCESS")
            print("Printing the Traversed Solution...")
            solution_depth = print_solution(node, solution_depth)
            print_node(problem.initial_state, problem)
            print("\nMax Queue Size: ", max_queue_size)
            print("\nTotal Nodes Traversed: ", total_nodes_traversed)
            print("\nSolution Depth: ", solution_depth)
            return 
        # Otherwise we check valid operators and insert results into queue
        # Call the expand function to only traverse valid states
        expand(node, problem, queue, states)
        max_queue_size = max(queue.qsize(), max_queue_size)
        
if __name__ == "__main__":
    # Asks the user for puzzle_size
    print("Welcome to N puzzle solver!")
    print("What size puzzle would you like to generate? (e.g. 8, 15, 25)")
    print("Please INSERT a valid natural number and press ENTER: ")
    puzzle_size = 8
    # Asks the user for number of rows in the puzzle
    # print("Please INSERT the amount of rows needed for the puzzle: ")
    rows = pow(puzzle_size+1, 1/2)
    print(rows)
    print("Please INSERT a valid puzzle you would like to test row by row.\n" + 
          "Note: for the empty space in the puzzle, please INSERT the number 0.")
    # Asks the user to enter the puzzle they would like to test
    puzzle = []
    for row in range(int(rows)):
        print("Please INSERT values for row " + str(row+1) + " with a space in between each number:\n" + 
              "Press ENTER when you are ready.\n")
        # puzzle.insert()
    # Asks the user the algorithm they would like to use
    print("Please select the algorithm you would like the program to use by entering its correspoding number as shown: \n")
    print("1. Uniform Cost Search\n" + 
          "2. A* with the Misplaced Tile heuristic\n" +
          "3. A* with the Manhattan Distance heuristic\n")
    print("Select an algortihm and press ENTER: ")
    heuristic = 1
    ## The program now have everything it needs to begin
    print("The program has successfully loaded the puzzle and will begin to search for the goal_state...")
    # goal_state = for num in range(puzzle_size+1)
    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]
    ##### Depth 0 test case from Professor Eamon Keogh's Project_1_The_Eight_Puzzle_CS_205_2024.pdf handout
    # initial_state = [[1, 2, 3],
    #               [4, 5, 6],
    #               [7, 8, 0]]
    ##### Depth 2 test case from Professor Eamon Keogh's Project_1_The_Eight_Puzzle_CS_205_2024.pdf handout
    initial_state = [[1, 2, 3],
                     [4, 5, 6],
                     [0, 7, 8]]
    ##### Depth 4 test case from Professor Eamon Keogh's Project_1_The_Eight_Puzzle_CS_205_2024.pdf handout
    # initial_state = [[1, 2, 3],
    #                  [5, 0, 6],
    #                  [4, 7, 8]]
    ##### Depth 12 test case from Professor Eamon Keogh's Project_1_The_Eight_Puzzle_CS_205_2024.pdf handout
    # initial_state = [[1, 3, 6],
    #                  [5, 0, 7],
    #                  [4, 8, 2]]
    queue = None
    if heuristic == 1:
        queue = Queue()
    else:
        queue = PriorityQueue()

    print("Calling the function...")
    
    problem = Problem(initial_state, goal_state, int(rows), heuristic, None)
    
    a_star_search(problem, queue)