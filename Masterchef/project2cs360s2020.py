# Copyright Dylan Ah Teck

import operator
import sys
import copy

# Class to hold each contestant's qualities, taken from the input file


class Contestant:
    def __init__(self, ID, cooking, captainship_A, captainship_B, picked):
        self.ID = ID
        self.cooking = cooking
        self.captainship_A = captainship_A
        self.captainship_B = captainship_B
        self.picked = picked

# Class to hold each team, consisting of its team members and the power (based on the team_member qualities)


class Team:
    def __init__(self, team_members, name):
        self.team_members = team_members
        self.power = 0
        self.name = name

    # Calculates the power of the based by formula given in prompt
    def calculatePower(self):
        diversity_point = True
        power = 0
        last_ID = set()

        if len(self.team_members) == 0:
            diversity_point = False

        for candidate in self.team_members:
            if self.name == 'A':
                power = power + (float(candidate.cooking)
                                 * float(candidate.captainship_A))

            else:
                power = power + (float(candidate.cooking)
                                 * float(candidate.captainship_B))

            if candidate.ID[4] in last_ID:
                diversity_point = False
            last_ID.add(candidate.ID[4])

        if diversity_point:
            power += float('120')

        return power


# Game state which is represented by each node in minimax tree
class GameStateNode:
    def __init__(self, team_A, team_B, available_candidates, turn='A', advantage=0):
        self.team_A = team_A
        self.team_B = team_B
        self.available_candidates = available_candidates
        self.turn = turn
        self.advantage = advantage
        self.child_nodes = []

    # Returns true if passes a terminal test -- i.e is a leaf-node
    def terminalTest(self):
        if len(self.team_A.team_members) == 5 and len(self.team_B.team_members) == 5:
            return True
        return False

    # Calculate utility of team and set it
    def utility(self):
        self.setAdvantage()
        return self.advantage

    # Simply set the utility from the leaf node
    def setUtility(self, utility):
        self.advantage = utility

    # Calculate advantage of current state, given Team A and Team B
    def setAdvantage(self):
        self.advantage = self.team_A.calculatePower() - self.team_B.calculatePower()

    # Generate the next possible states
    def generateActions(self):

        if len(self.available_candidates) == 0:
            return

        for contestant in self.available_candidates:

            # Create a child node
            if(self.turn == 'A'):
                new_members = copy.deepcopy(self.team_A.team_members)
                new_members.append(contestant)
                new_team_A = Team(new_members, 'A')
                turn = 'B'

                new_available_candidates = copy.copy(
                    self.available_candidates)
                new_available_candidates.remove(contestant)

                child_node = GameStateNode(
                    new_team_A, self.team_B, new_available_candidates, turn)

            elif(self.turn == 'B'):
                new_members = copy.copy(self.team_B.team_members)
                new_members.append(contestant)
                new_team_B = Team(new_members, 'B')

                turn = 'A'

                new_available_candidates = copy.copy(
                    self.available_candidates)
                new_available_candidates.remove(contestant)
                child_node = GameStateNode(
                    self.team_A, new_team_B, new_available_candidates, turn)

            # Add child node to root's children
            self.child_nodes.append(child_node)

        return self.child_nodes

# Minimax algo's max value recursive function


def maxValue(state):
    if state.terminalTest():
        return state.utility()

    v = -sys.maxsize
    actions = state.generateActions()
    for action in actions:
        v = max(v, minValue(action))
    state.setUtility(v)
    return v

# Minimax algo's min value recursive function


def minValue(state):
    if state.terminalTest():
        return state.utility()

    v = sys.maxsize
    actions = state.generateActions()
    for action in actions:
        v = min(v, maxValue(action))
    state.setUtility(v)
    return v

# Minimax finds the best possible advantage based on the algorithm
# It then explores each of the next states to find the candidate that will lead to that advantage


def minimax(state):
    v = maxValue(state)
    best_action = state.child_nodes[0]
    for child_node in state.child_nodes:
        if child_node.advantage == v:
            if((best_action.advantage == v and int(child_node.team_A.team_members[-1].ID) < int(best_action.team_A.team_members[-1].ID)) or best_action.advantage != v):
                best_action = child_node

    return best_action.team_A.team_members[-1].ID

# Alpha-beta pruning max value


def alpha_beta_maxValue(state, alpha, beta):
    if state.terminalTest():
        return state.utility()

    v = -sys.maxsize
    actions = state.generateActions()
    for action in actions:
        v = max(v, alpha_beta_minValue(action, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    state.setUtility(v)
    return v

# Alpha-beta pruning min value


def alpha_beta_minValue(state, alpha, beta):
    if state.terminalTest():
        return state.utility()

    v = sys.maxsize
    actions = state.generateActions()
    for action in actions:
        v = min(v, alpha_beta_maxValue(action, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    state.setUtility(v)
    return v

# Alpha-beta search ignores subtrees that cannot provide a higher advantage than one already found


def alpha_beta_search(state):
    v = alpha_beta_maxValue(state, -sys.maxsize, sys.maxsize)
    best_action = state.child_nodes[0]
    for child_node in state.child_nodes:

        if child_node.advantage == v:
            if((best_action.advantage == v and int(child_node.team_A.team_members[-1].ID) < int(best_action.team_A.team_members[-1].ID)) or best_action.advantage != v):
                best_action = child_node

    return best_action.team_A.team_members[-1].ID

# Main function to parse input files, create classes from data,
# call specified algorithm and output result to file


def main():
    filename = "input.txt"

    file = open(filename, "r")
    content = file.read().splitlines()

    available_candidates = []
    team_A_contestants = []
    team_B_contestants = []
    count = 0

    for line in content:
        if count == 0:
            n = line
        elif count == 1:
            algo = line
        else:
            ID, cooking, cap_A, cap_B, picked = line.split(",")
            if picked == '0':
                available_candidates.append(Contestant(
                    ID, cooking, cap_A, cap_B, picked))
            elif picked == '1':
                team_A_contestants.append(Contestant(
                    ID, cooking, cap_A, cap_B, picked))
            elif picked == '2':
                team_B_contestants.append(Contestant(
                    ID, cooking, cap_A, cap_B, picked))
        count += 1

    available_candidates.sort(key=operator.attrgetter('ID'))
    team_A_contestants.sort(key=operator.attrgetter('ID'))
    team_B_contestants.sort(key=operator.attrgetter('ID'))

    Team_A = Team(team_A_contestants, 'A')
    Team_B = Team(team_B_contestants, 'B')

    initial_state = GameStateNode(Team_A, Team_B, available_candidates)
    if algo == 'minimax':
        ans_id = minimax(initial_state)
    elif algo == 'ab':
        ans_id = alpha_beta_search(initial_state)

    f = open("output.txt", "w+")
    f.write(ans_id)
    f.close()


if __name__ == '__main__':
    main()
