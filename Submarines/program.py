import sys
import random
import copy
import numpy as np


class MDP:
    def __init__(self, grid, gamma):
        self.U = ""
        self.discount = gamma
        self.grid = grid
        self.states = [[State(x, y) for x in range(grid)] for y in range(grid)]

    def max_neighbouring_utility(self, state, Udash):
        up_state = self.up_state(state)
        down_state = self.down_state(state)
        left_state = self.left_state(state)
        right_state = self.right_state(state)

        return max(
            self.calculate_neighbour_utility(
                up_state, down_state, left_state, right_state, Udash
            ),
            self.calculate_neighbour_utility(
                down_state, up_state, left_state, right_state, Udash
            ),
            self.calculate_neighbour_utility(
                left_state, right_state, down_state, up_state, Udash
            ),
            self.calculate_neighbour_utility(
                right_state, left_state, down_state, up_state, Udash
            ),
        )

    def calculate_neighbour_utility(self, intended, other1, other2, other3, Udash):
        ans = (
            0.7 * Udash[intended.col][intended.row]
            + 0.1 * Udash[other1.col][other1.row]
            + 0.1 * Udash[other2.col][other2.row]
            + 0.1 * Udash[other3.col][other3.row]
        )
        return ans

    def up_state(self, state):
        if state.col == 0:
            return state
        else:
            return self.states[state.col - 1][state.row]

    def down_state(self, state):
        if state.col >= self.grid - 1:
            return state
        else:
            return self.states[state.col + 1][state.row]

    def left_state(self, state):
        if state.row == 0:
            return state
        else:
            return self.states[state.col][state.row - 1]

    def right_state(self, state):
        if state.row >= self.grid - 1:
            return state
        else:
            return self.states[state.col][state.row + 1]

    def initialize_rewards(self, obstacles, destination):
        for obstacle in obstacles:
            split = obstacle.split(",")
            self.states[int(split[1])][int(split[0])].reward += -100

        split = destination.split(",")
        self.states[int(split[1])][int(split[0])].reward += 100


class State:
    def __init__(self, row, col):
        self.U = ""
        self.row = row
        self.col = col
        self.reward = -1


def value_iteration(mdp, epsilon, destination_row, destination_col):
    U = [[0.0 for x in range(mdp.grid)] for y in range(mdp.grid)]
    Udash = [[0.0 for x in range(mdp.grid)] for y in range(mdp.grid)]
    Udash[int(destination_col)][int(destination_row)] = 99

    while True:
        U = copy.deepcopy(Udash)
        delta = 0
        for row in range(mdp.grid):
            for col in range(mdp.grid):
                if not (row == int(destination_row) and col == int(destination_col)):
                    state = mdp.states[col][row]
                    Udash[state.col][state.row] = state.reward + (
                        mdp.discount * mdp.max_neighbouring_utility(state, Udash)
                    )
                    if (
                        abs(Udash[state.col][state.row] - U[state.col][state.row])
                        > delta
                    ):
                        delta = abs(
                            Udash[state.col][state.row] - U[state.col][state.row]
                        )

        if delta < epsilon:
            break

    return U


def select_optimal(mdp, U, destination, obstacles):
    output = [[" " for x in range(mdp.grid)] for y in range(mdp.grid)]
    for obstacle in obstacles:
        split = obstacle.split(",")
        output[int(split[1])][int(split[0])] = "o"

    split = destination.split(",")
    output[int(split[1])][int(split[0])] = "."

    for row in range(mdp.grid):
        for col in range(mdp.grid):
            if output[row][col] == " ":
                calculate_direction(U, output, row, col)

    return output


def calculate_direction(U, output, row, col):
    top = U[row - 1][col] if row != 0 else -sys.maxsize - 1
    left = U[row][col - 1] if col != 0 else -sys.maxsize - 1
    down = U[row + 1][col] if row != len(U) - 1 else -sys.maxsize - 1
    right = U[row][col + 1] if col != len(U) - 1 else -sys.maxsize - 1

    MAX = max(top, left, down, right)

    if top == MAX:
        output[row][col] = "^"
    elif down == MAX:
        output[row][col] = "v"
    elif right == MAX:
        output[row][col] = ">"
    else:
        output[row][col] = "<"


def main():
    filename = "input.txt"

    file = open(filename, "r")
    content = file.read().splitlines()

    obstacles = []
    count = 0
    gamma = 0.9
    epsilon = 0.01

    for line in content:
        if count == 0:
            grid_size = int(line)
        elif count == 1:
            num_obstacles = int(line)
        elif count == num_obstacles + 2:
            destination = line
        else:
            obstacles.append(line)
        count += 1

    destination_split = destination.split(",")
    mdp = MDP(grid_size, gamma)
    mdp.initialize_rewards(obstacles, destination)

    U = value_iteration(mdp, epsilon, destination_split[0], destination_split[1])
    output = select_optimal(mdp, U, destination, obstacles)

    f = open("output.txt", "w")
    for row in output:
        for symbol in row:
            f.write("%s" % symbol)
        f.write("\n")
    f.close()


if __name__ == "__main__":
    main()
