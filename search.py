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
#import searchAgents

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
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    expanded = [] # initializing the expanded nodes
    frontier = util.Stack() # initializing frontier using initial states
    frontier.push([(problem.getStartState(), None, None)]) # (successor, action, stepCost)

    while not frontier.isEmpty(): # check whether still in frontier
        fringe = frontier.pop() # choose a node and pop it

        states = fringe[len(fringe) - 1] # initializing
        states = states[0] # get start state

        if problem.isGoalState(states): # check whether current state is goal
            #print [x[1] for x in fringe][1:]
            return [x[1] for x in fringe][1:] # if true, return action list

        if states not in expanded: # check whether node has been expanded
            expanded.append(states) # if not, add it to the list

            for successor in problem.getSuccessors(states): # add all node's successors to frontier
                if successor[0] not in expanded: # check whether node has been expanded
                    successorList = fringe[:] # previous frontier
                    successorList.append(successor) # if not expended, add it to the list
                    frontier.push(successorList) # push a tuple of state into frontier

    return [] # if the frontier is empty then return failure

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    expanded = [] # initializing the expanded nodes
    frontier = util.Queue() # initializing frontier using initial states
    frontier.push([(problem.getStartState(), None, None)]) # (successor, action, stepCost)

    while not frontier.isEmpty(): # check whether still in frontier
        fringe = frontier.pop() # choose a node and pop it

        states = fringe[len(fringe) - 1] # initializing
        states = states[0] # get start state
        
        if problem.isGoalState(states): # check whether current state is goal
            return [x[1] for x in fringe][1:] # if true, return action list

        if states not in expanded: # check whether node has been expanded
            expanded.append(states) # if not, add it to the list

            for successor in problem.getSuccessors(states): # add all node's successors to frontier
                if successor[0] not in expanded: # check whether node has been expanded
                    successorList = fringe[:] # previous frontier
                    successorList.append(successor) # if not expended, add it to the list
                    frontier.push(successorList) # push a tuple of state into frontier

    return [] # if the frontier is empty then return failure

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    expanded = [] # initializing the expanded nodes
    actionList = [] # action list to current nodes
    frontier = util.PriorityQueue() # initializing frontier using initial states
    frontier.push((problem.getStartState(), actionList), None) # (successor, action, stepCost)

    while not frontier.isEmpty(): # check whether still in frontier
        states, actions = frontier.pop() # choose a node and pop it

        if states not in expanded: # check whether node has been expanded
            expanded.append(states) # if not, add it to the list

            if problem.isGoalState(states): # check whether current state is goal
                return actions # if true, return action list

            for successor in problem.getSuccessors(states): # add all node's successors to frontier
                position, direction, cost = successor # successor information
                nextAction = actions + [direction] # next action list
                nextCost = problem.getCostOfActions(nextAction) # get cost of actions
                frontier.push((position, nextAction), nextCost) # push a tuple of state into frontier

    return [] # if the frontier is empty then return failure

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    expanded = [] # initializing the expanded nodes
    actionList = [] # action list to current nodes
    frontier = util.PriorityQueue() # initializing frontier using initial states
    frontier.push((problem.getStartState(), actionList), heuristic(problem.getStartState(), problem)) # (successor, action, stepCost)

    while not frontier.isEmpty(): # check whether still in frontier
        states, actions = frontier.pop() # choose a node and pop it

        if states not in expanded: # check whether node has been expanded
            expanded.append(states) # if not, add it to the list

            if problem.isGoalState(states): # check whether current state is goal
                return actions # if true, return action list

            for successor in problem.getSuccessors(states): # add all node's successors to frontier
                position, direction, cost = successor # successor information
                nextAction = actions + [direction] # next action list
                nextCost = problem.getCostOfActions(nextAction) + heuristic(position, problem) # cost with heuristic
                frontier.push((position, nextAction), nextCost) # push a tuple of state into frontier

    return [] # if the frontier is empty then return failure


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
