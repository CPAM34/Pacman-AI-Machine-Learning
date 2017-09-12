# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Initialize initial variables for start state, whether the start is the goal, and empty path and list of directions
    start = problem.getStartState()
    isGoal = problem.isGoalState(start)
    path = []
    directions = []
    # BFS queue created to house 3 element tuples in form of (state, directions to state, path of states to state)
    dfsstack = util.Stack()
    dfsstack.push((start, directions, path))
    # While the stack is not empty, pop the first element in the queue
    while not dfsstack.isEmpty():
        i = dfsstack.pop()
        # For each successor of the popped state...
        for j in problem.getSuccessors(i[0]):
            path = copy.deepcopy(i[2])
            # if the state of the successor is not in the path list
            if j[0] not in path:
                # check if successor is the goal and append directions to successor and successor itself to the path
                isGoal = problem.isGoalState(j[0])
                directions = copy.deepcopy(i[1])
                path.append(i[0])
                directions.append(j[1])
                # if successor is the goal state, return directions. Otherwise, push a tuple with the successor, list of directions to it, and path of states to the successor to the stack
                if isGoal:
                    return directions
                dfsstack.push((j[0], directions, path))
    # if no elements are lest, there are no directions to be had, so return empty list of directions
    directions = []
    return directions
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Initialize initial variables for start state, whether the start is the goal, and empty path and list of directions
    start = problem.getStartState()
    isGoal = problem.isGoalState(start)
    path = []
    directions = []
    # BFS queue created to house 2 element tuples in form of (state, directions to state)
    bfsqueue = util.Queue()
    bfsqueue.push((start, directions))
    # While the queue is not empty, pop the first element in the queue
    while not bfsqueue.isEmpty():
        i = bfsqueue.pop()
        # For each successor of the popped state...
        for j in problem.getSuccessors(i[0]):
            # if the state of the successor is not in the path list
            if j[0] not in path:
                # check if successor is the goal and append directions to successor and successor itself to the path
                isGoal = problem.isGoalState(j[0])
                directions = copy.deepcopy(i[1])
                path.append(j[0])
                directions.append(j[1])
                # if successor is the goal state, return directions. Otherwise, queue a tuple up with the successor and list of directions to it
                if isGoal:
                    return directions
                bfsqueue.push((j[0], directions))
    # if no elements are lest, there are no directions to be had, so return empty list of directions
    directions = []
    return directions
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Initialize initial variables for start state, whether the start is the goal, and empty path and list of directions, as well as the cost of the directions
    start = problem.getStartState()
    isGoal = problem.isGoalState(start)
    path = []
    directions = []
    cost = 0
    # UCS uses a 2 element tuple priority queue (state, directions of state), with the cost
    ucspriorityqueue = util.PriorityQueue()
    ucspriorityqueue.push((start, directions), cost)
    # While the priority queue is not empty, pop the first element in the PQ
    while not ucspriorityqueue.isEmpty():
        i = ucspriorityqueue.pop()
        # Check if the popped state is the goal state. If so, return the list of directions to the popped state
        isGoal = problem.isGoalState(i[0])
        directions = copy.deepcopy(i[1])
        if isGoal:
            return directions
        path.append(i[0])
        # for each successor to the popped state...
        for j in problem.getSuccessors(i[0]):
            # if successor is not in the path, add the directions to it to the list of directions and find out the cost of the traversal
            if j[0] not in path:
                directions = copy.deepcopy(i[1])
                directions.append(j[1])
                cost = problem.getCostOfActions(directions)
                # push onto the PQ a tuple of the current state and directions to it, as well as the cost of enacting those directions
                ucspriorityqueue.push((j[0], directions), cost)
    # if no elements are lest, there are no directions to be had, so return empty list of directions
    directions = []
    return directions
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Initialize initial variables for start state, whether the start is the goal, and empty path representing the closed set of visited states and list of directions, as well as the heuristic cost of the directions
    start = problem.getStartState()
    isGoal = problem.isGoalState(start)
    path = []
    directions = []
    heuristic_cost = heuristic(start, problem)
    # A* uses a 2 element tuple priority queue (state, directions of state), with the cost
    astarpriorityqueue = util.PriorityQueue()
    astarpriorityqueue.push((start, directions), heuristic_cost)
    # While the priority queue is not empty, pop the first element in the PQ
    while not astarpriorityqueue.isEmpty():
        i = astarpriorityqueue.pop()
        # Check if the popped state is the goal state. If so, return the list of directions to the popped state
        isGoal = problem.isGoalState(i[0])
        directions = copy.deepcopy(i[1])
        if isGoal:
            return directions
        path.append(i[0])
        # for each successor to the popped state...
        for j in problem.getSuccessors(i[0]):
            # if successor is not in the path, add the directions to it to the list of directions and find out the total cost of the traversal, local and heuristic
            if j[0] not in path:
                directions = copy.deepcopy(i[1])
                directions.append(j[1])
                heuristic_cost = heuristic(j[0], problem)
                local_cost = problem.getCostOfActions(directions)
                # push onto the PQ a tuple of the current state and directions to it, as well as the local cost of enacting those directions and heuristic cost
                astarpriorityqueue.push((j[0], directions), heuristic_cost + local_cost)
    # if no elements are lest, there are no directions to be had, so return empty list of directions
    directions = []
    return directions
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
