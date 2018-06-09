# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Find the nearest distance between Ghost and Pacman
        nearestGhost = min([manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates])
        #print nearestGhost
        if nearestGhost:
            distGhost = 1 / nearestGhost
        else:
            distGhost = 100
        # Find the nearest food for Pacman to eat
        if newFood.asList():
            nearestFood = min([manhattanDistance(newPos, food) for food in newFood.asList()])
        else:
            nearestFood = 0
        # Consider (1) distance to the food (2) number of food left (3) nearest distance to Ghost
        w1 = -1 # (1)
        w2 = -50 # (2)
        w3 = -10 # (3)
        evaluation = w1 * nearestFood + w2 * len(newFood.asList()) + w3 * distGhost

        return evaluation
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, self.depth)[1] # calling maxValue recursively
        #util.raiseNotDefined()

    def maxValue(self, state, ply):
        if state.isWin() or state.isLose() or ply == 0: # if no more ply or next state
            return self.evaluationFunction(state), None

        legalMoves = state.getLegalActions(0) # get legal actions
        scores = [self.minValue(state.generateSuccessor(self.index, move), 1, ply) for move in legalMoves]
        maxScore = max(scores) # choose max in successor min nodes
        for i in range(len(scores)): # select the best move
            if scores[i] == maxScore:
                choice = [i]
        return maxScore, legalMoves[choice[0]]

    def minValue(self, state, agent, ply):
        if state.isWin() or state.isLose() or ply == 0:
            return self.evaluationFunction(state), None

        legalMoves = state.getLegalActions(agent) # get legal actions
        if(agent == state.getNumAgents() - 1): # call maxValue for Pacman agent
            scores = [self.maxValue(state.generateSuccessor(agent, move), (ply - 1)) for move in legalMoves]
        else: # otherwise, call minValue for Ghost agent
            scores = [self.minValue(state.generateSuccessor(agent, move), agent + 1, ply) for move in legalMoves]
        minScore = min(scores) # choose min in successor max nodes
        for i in range(len(scores)): # select the best move
            if scores[i] == minScore:
                choice = [i]
        return minScore, legalMoves[choice[0]]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def AlphaBetaSearch(state): # basically follows the psudo code in slides
            a = None
            b = None
            value = None
            bestAction = None

            for action in state.getLegalActions(0): # legal actions of Pacman
                value = max(value, minValue(state.generateSuccessor(0, action), 1, 1, a, b))
                if a is None: # initialize
                    a = value
                    bestAction = action
                else: # update the max best option
                    if value > a:
                        a = max(value, a)
                        bestAction = action
            return bestAction

        def maxValue(state, agent, ply, a, b): # implement Max-Value function
            if ply > self.depth:
                return self.evaluationFunction(state)
            value = None
            for action in state.getLegalActions(agent):
                v = minValue(state.generateSuccessor(agent, action), agent + 1, ply, a, b)
                value = max(value, v)
                if b is not None and value > b:
                    return value
                a = max(a, value)

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        def minValue(state, agent, ply, a, b): # implement Min-Value function
            if agent == state.getNumAgents():
                return maxValue(state, 0, ply + 1, a, b)
            value = None
            for action in state.getLegalActions(agent):
                v = minValue(state.generateSuccessor(agent, action), agent + 1, ply, a, b)
                if value is not None:
                    value = min(value, v)
                else:
                    value = v
                if a is not None and value < a:
                    return value
                if b is not None:
                    b = min(b, value)
                else:
                    b = value

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        return AlphaBetaSearch(gameState)
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimaxSearch(gameState, 0, self.depth)[1]

    def expectimaxSearch(self, state, agent, ply):
        if state.isWin() or state.isLose() or ply == 0: # if no more ply or next state
            return self.evaluationFunction(state), None
        else:
            if agent == 0: # initialize v in maxValue for Pacman
                v = -999999999
            else: # initialize v in expValue
                v = 0
            if agent == state.getNumAgents() - 1:
                ply -= 1
            choice = None
            nextAgent = (1 + agent) % state.getNumAgents() # index of next agent
            legalMoves = state.getLegalActions(agent) # get legal actions
            for move in legalMoves:
                score = self.expectimaxSearch(state.generateSuccessor(agent, move), nextAgent, ply)
                if agent == 0: # Pacman agent
                    if v < score[0]:
                        v = score[0] # max-Value
                        choice = move
                else:
                    v += score[0] / len(legalMoves) # probabilities
                    choice = move
            return v, choice

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <Instead of evaluating actions in reflex agent function, the
      evaluation function here should evaluate states. In the function, I considered
      the minimal distance to food, number of food and capsules, and nearest Ghost.
      The evaluation is modified from question 1.>
    """
    "*** YOUR CODE HERE ***"
    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curGhostStates = currentGameState.getGhostStates()

    if curFood.asList(): # similar to reflex agent
        nearestFood = min([manhattanDistance(curPos, food) for food in curFood.asList()])
    else:
        nearestFood = 0

    nearestGhost = min([manhattanDistance(curPos, ghostState.getPosition()) for ghostState in curGhostStates])
    #print nearestGhost
    if nearestGhost:
        distGhost = 1 / nearestGhost
    else:
        distGhost = 100

    # Consider (1) distance to the food (2) number of food left (3) nearest Ghost (4) number of capsules
    w1 = -1 # (1)
    w2 = -1000 # (2)
    w3 = -10 # (3)
    w4 = -10 # (4)
    evaluation = currentGameState.getScore() + w1 * nearestFood + w2 * currentGameState.getNumFood() + w3 * distGhost + w4 * len(currentGameState.getCapsules())

    return evaluation
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
