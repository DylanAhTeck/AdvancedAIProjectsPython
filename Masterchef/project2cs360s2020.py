import operator

filename = "input.txt"

file = open(filename, "r")
content = file.read().splitlines()


class Contestant:
    def __init__(self, ID, cooking, captainship_A, captainship_B, picked):
        self.ID = ID
        self.cooking = cooking
        self.captainship_A = captainship_A
        self.captainship_B = captainship_B
        self.picked = picked


class Team:
    def __init__(self, team_members, name):
        self.team_members = team_members
        self.power = 0
        self.name = name

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
            power += 120

        return power


class GameStateNode:
    def __init__(self, team_A, team_B, available_candidates, turn='A', advantage=0):
        self.team_A = team_A
        self.team_B = team_B
        self.available_candidates = available_candidates
        self.turn = turn
        self.advantage = advantage
        self.child_nodes = []

    def terminalTest(self):
        if len(self.team_A.team_members) == 5 and len(self.team_B.team_members) == 5:
            return True
        return False

    def utility(self):
        self.setAdvantage()
        return self.advantage

    def setUtility(self, utility):
        self.advantage = utility

    def setAdvantage(self):
        self.advantage = self.team_A.calculatePower() - self.team_B.calculatePower()

    def generateActions(self):

        if len(self.available_candidates) == 0:
            return

        for contestant in self.available_candidates:

            # Create a child node
            if(self.turn == 'A'):
                new_members = self.team_A.team_members.copy()
                new_members.append(contestant)
                new_team_A = Team(new_members, 'A')
                turn = 'B'

                new_available_candidates = self.available_candidates.copy()
                new_available_candidates.remove(contestant)

                child_node = GameStateNode(
                    new_team_A, self.team_B, new_available_candidates, turn)

            elif(self.turn == 'B'):
                new_members = self.team_B.team_members.copy()
                new_members.append(contestant)
                new_team_B = Team(new_members, 'B')

                turn = 'A'

                new_available_candidates = self.available_candidates.copy()
                new_available_candidates.remove(contestant)
                child_node = GameStateNode(
                    self.team_A, new_team_B, new_available_candidates, turn)

            # Add child node to root's children
            self.child_nodes.append(child_node)

        return self.child_nodes


def maxValue(state):
    if state.terminalTest():
        return state.utility()

    v = float("-inf")
    actions = state.generateActions()
    for action in actions:
        v = max(v, minValue(action))
    state.setUtility(v)
    return v


def minValue(state):
    if state.terminalTest():
        return state.utility()

    v = float("inf")
    actions = state.generateActions()
    for action in actions:
        v = min(v, maxValue(action))
    state.setUtility(v)
    return v


def minimax(state):
    v = maxValue(state)
    print("Advantage: " + str(v))
    best_action = state.child_nodes[0]
    for child_nodes in state.child_nodes:
        if child_nodes.advantage == v:
            if()


def main():

    available_candidates = []
    team_A = []
    team_B = []
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
                team_A.append(Contestant(ID, cooking, cap_A, cap_B, picked))
            elif picked == '2':
                team_B.append(Contestant(ID, cooking, cap_A, cap_B, picked))
        count += 1

    available_candidates.sort(key=operator.attrgetter('ID'))
    team_A.sort(key=operator.attrgetter('ID'))
    team_B.sort(key=operator.attrgetter('ID'))

    TeamA = Team(team_A, 'A')
    TeamB = Team(team_B, 'B')

    initial_state = GameStateNode(TeamA, TeamB, available_candidates)
    minimax(initial_state)


if __name__ == '__main__':
    main()
