# valueIterationAgents.py
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
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
from itertools import izip
import time


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.nextValues = util.Counter()
        self.policy = dict()
        self.argmax = lambda array: max(izip(array, xrange(len(array))))[1]
        # Write value iteration code here
        # get all possible states
        states = self.mdp.getStates()

        #run for specified amount of iterations
        i = 0
        start_time = time.time()
        while i < iterations:
            #go over all possible states
            for s in states:
                actions = self.mdp.getPossibleActions(s)
                #go over all possible actions
                if self.mdp.isTerminal(s):
                    self.policy[s] = None
                else:
                    q_vals = []
                    for j,a in enumerate(actions):
                        #do Bellman backups
                        q_vals.append(self.getQValue(s, a))
                    #update state value
                    self.nextValues[s] = max(q_vals)
                    #update policy
                    self.policy[s] = actions[self.argmax(q_vals)]

            self.values = self.nextValues.copy()
            i += 1
        elapsed_time = time.time() - start_time
        print ('PLANNING TIME: {}'.format(elapsed_time))

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        q_val = 0
        successors = self.mdp.getTransitionStatesAndProbs(state, action)
        for succ in successors:
            nextState, prob = succ[0], succ[1]
            q_val += prob*(self.mdp.getReward(state, action, nextState) + self.discount*self.getValue(nextState))

        return q_val

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        if self.mdp.isTerminal(state):
            return None

        if state in self.policy.keys():
            return self.policy[state]
        else:  #if correct policy is not yet updated go north
            return 'north'

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
