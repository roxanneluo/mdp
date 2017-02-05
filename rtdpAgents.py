# rtdpAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu). The RTDP question was added by
# Gagan Bansal (bansalg@cs.washington.edu) and Dan Weld (weld@cs.washington.edu).


import random
import mdp, util

from learningAgents import ValueEstimationAgent

class RTDPAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A RTDPAgent takes a Markov decision process
        (see mdp.py) on initialization and runs rtdp 
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, max_iters=100):
        """
          Your value rtdp agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
              mdp.getStartState()

          Other useful functions:
              weighted_choice(choices)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = {}  # note, we use a normal python dictionary for RTDPAgent.

        # Write rtdp code here
        start_state = mdp.getStartState()
        for i in range(iterations):
            print(i)
            self.RTDPTrial(start_state)

    def RTDPTrial(self, state):
        while not self.mdp.isTerminal(state):
            #print(state)
            action = self.computeActionFromValues(state)
            # actually, I want to reuse the qvalues computed above 
            self.updateValue(state, action)
            if action is None:
                print('reach a state with no viable action')
                return
            state = self.pickNextState(state, action)
    
    def pickNextState(self, state, action):
        """
          Return the next stochastically simulated state.
        """
        "*** YOUR CODE HERE ***"
        next_states_probs = self.mdp.getTransitionStatesAndProbs(state, action)
        return weighted_choice(next_states_probs)
        util.raiseNotDefined()

    def updateValue(self, state, action):
        """
          Update the value of given state.
        """
        "*** YOUR CODE HERE ***"
        if action is None:
            if state not in self.values:
                self.values[state] = self.getValue(state)
            return
        value = self.computeQValueFromValues(state, action)
        self.values[state] = value 


    def getHeuristicValue(self, state):
        """
          Return the heuristic value of state.
        """
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        if mdp.isTerminal(state):
            return 0

        goal_state = mdp.getGoalState()
        goal_reward = mdp.getGoalReward()
        dist = util.manhattanDistance(state, goal_state)
        return self.discount**(dist - 1) * goal_reward


    def getValue(self, state):
        """
          Return the current stored value of the state.
          If the state has not been seen yet then return it heuristic value.

          Note the difference between this and the similar method in valueIterationAgents
        """
        value = None
        if state not in self.values:
            value = self.getHeuristicValue(state)
            self.values[state] = value
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        assert(action is not None)
        qv = 0
        mdp = self.mdp
        for next_state, prob in mdp.getTransitionStatesAndProbs(state, action):
            qv += prob*(mdp.getReward(state, action, next_state) + \
                    self.discount * self.getValue(next_state))
        return qv

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        action_list = self.mdp.getPossibleActions(state)
        if len(action_list) == 0 or self.mdp.isTerminal(state):
            return None 

        best_action, best_qv = None, -float("inf")
        for action in action_list:
            qv = self.computeQValueFromValues(state, action)
            if qv > best_qv:
                best_qv, best_action = qv, action
        return best_action 

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


def weighted_choice(choices):
    """
    Return a random element from list of the form: [(choice, weight), ....]
    Credits: http://stackoverflow.com/questions/3679694
    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
       if upto + w >= r:
          return c
       upto += w
    assert False, "Shouldn't get here"
