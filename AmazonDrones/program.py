try:
    import queue
except ImportError:
    import Queue as queue

import copy
import time


score = 0

for i in range(0, 49):
    overtime = False
    timeout = time.time() + 60 * 5
    # CHANGE TO filename = "input.txt" AFTER
    filename = "grading_case/input" + str(i) + ".txt"

    file = open(filename, "r")
    content = file.read().splitlines()

    count = 0
    packages = []

    for line in content:
        line.rstrip("/n")
        if count == 0:
            n = int(line)
        elif count == 1:
            d = int(line)
        elif count == 2:
            p = int(line)
        elif count == 3:
            algo = line
        else:
            packages.append(line)
        count += 1

    """print("count", count)
    print("n", n)
    print("d", d)
    print("p", p)
    print("algo", algo)
    print("packages", packages)"""

    file.close()

    # Map takes coordinate as key, number of packages as value
    package_map = {}

    for package in packages:
        if not package in package_map:
            package_map[package] = 1
        else:
            package_map[package] += 1

    """print(package_map)"""

    # DEFINITION OF CLASSES HERE

    # State consists of set of coordinates
    class State:
        def __init__(self, parent_state=None):
            if parent_state is None:
                self.package_location_set = set()
            else:
                self.package_location_set = copy.deepcopy(
                    parent_state.package_location_set
                )

        def add(self, new_location):
            self.package_location_set.add(new_location)

        def __eq__(self, other):
            return self.package_location_set == other.package_location_set

        def __hash__(self):
            return hash(str(self))

    class Node:
        def __init__(self, parent_node=None):
            "constructor to initiate this object"

            if parent_node is not None:
                # number of packages
                self.packages = parent_node.packages
                self.state = State()
                self.state.package_location_set = copy.deepcopy(
                    parent_node.state.package_location_set
                )
                self.valid = copy.deepcopy(parent_node.valid)

                # For astar
                self.g = parent_node.g
                self.h = 0

            else:
                self.packages = 0
                self.state = State()
                self.valid = [[True for i in range(n)] for j in range(n)]

                # For astar
                self.g = 0
                self.h = 0

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.packages > other.packages

        # Optimize later by adding package locations to front of list
        def find_neighbours(self):
            if len(self.state.package_location_set) >= d:
                return []

            neighbouring_states = []
            package_locations = []
            nonpackage_locations = []
            for i in range(n):
                for j in range(n):
                    if self.valid[i][j]:
                        coordinate = str(i) + "," + str(j)
                        if coordinate in package_map:
                            package_locations.append(coordinate)
                        else:
                            nonpackage_locations.append(coordinate)
                        # neighbouring_states.append(str(i) + "," + str(j))

            neighbouring_states = nonpackage_locations + package_locations
            return neighbouring_states

        def setvalid(self, new_location):
            # for location in self.state.package_location_set:
            location = new_location
            string = location.split(",")
            i = int(string[0])
            j = int(string[1])
            for I in range(n):
                for J in range(n):
                    if i == I or j == J or (abs(I - i) - abs(J - j) == 0):
                        self.valid[I][J] = False

        def add(self, new_location):
            self.state.add(new_location)

        def addg(self, new_location):
            string = new_location.split(",")
            i = int(string[0])
            j = int(string[1])
            for I in range(n):
                for J in range(n):
                    if (
                        (i == I or j == J or (abs(I - i) - abs(J - j) == 0))
                        and self.valid[I][J] is True
                        and (str(I) + "," + str(J)) in package_map
                    ):
                        # print(str(new_location) + " " + str(I) + "," + str(J))
                        self.g += package_map[(str(I) + "," + str(J))]

    goal_node = Node()

    def DFS():

        # Equivalent to empty grid with no drones placed
        start_node = Node()

        # Create LIFO Queue, insert start_node, and create explored set
        LIFO = queue.LifoQueue()
        LIFO.put(start_node)

        # Create two sets to maintain frontier and explored states
        frontier_state_set = set()
        explored_state_set = set()

        # Set goal_node global variable
        global goal_node

        while True:

            if time.time() > timeout:
                global overtime
                overtime = True
                break

            # If frontier empty, return False for failure
            if LIFO.empty():
                return False

            # Pop the last node in LIFO queue
            node = LIFO.get()

            # Add the node state to explored
            explored_state_set.add(node.state)

            # find_neighbours returns list of all possible new package locations
            # child_state is the location of each possible new package
            for new_package_location in node.find_neighbours():

                # Create new potential child_state which is same as parent state
                # plus the new package location
                child_state = State(node.state)
                child_state.add(new_package_location)

                # Check if child_state is not in explored or frontier
                if (
                    child_state not in explored_state_set
                    and child_state not in frontier_state_set
                ):

                    # Create new node from state
                    child_node = Node(node)
                    child_node.state.add(new_package_location)

                    # print(child_node.state.package_location_set)
                    if new_package_location in package_map:
                        child_node.packages += package_map[new_package_location]

                    child_node.setvalid(new_package_location)

                    # Set as goal node if achieved number of drones and MORE packages
                    if len(child_node.state.package_location_set) == d:
                        if child_node.packages > goal_node.packages:
                            goal_node = child_node

                        # Add to explored d
                        explored_state_set.add(child_node.state)

                    # Else add to frontier set

                    LIFO.put(child_node)
                    frontier_state_set.add(child_node.state)

    # g(n) is number of blocked packages
    # h(n) is - (number of packages picked up in state)

    def Astar():

        # Equivalent to empty grid with no drones placed
        start_node = Node()

        # Create priority queue and insert start_node
        pqueue = queue.PriorityQueue()
        pqueue.put((0, start_node))

        # Integer of total number of packages
        total_package = p

        # Set goal_node global variable
        global goal_node

        # To check if state is already in queue
        frontier_set = set()

        while True:

            if pqueue.empty():
                return False

            # Get the highest priority (smallest number) node from pq
            node = pqueue.get()[1]

            # If d drones is placed this is the goal state
            if len(node.state.package_location_set) == d:
                goal_node = node
                return True

            # find_neighbours returns list of all possible new package locations
            # child_state is the location of each possible new package
            for new_package_location in node.find_neighbours():

                # Create child node from new state
                child_node = Node(node)
                child_node.state.add(new_package_location)

                if new_package_location in package_map:
                    child_node.packages += package_map[new_package_location]

                # Sets the increased g cost (blocked packages) due to new package locaiton
                child_node.addg(new_package_location)

                # Sets the validity grid affected by placement of new drone
                child_node.setvalid(new_package_location)

                # The h(n) is simply the negative of the number of packages picked up
                child_node.h = -child_node.packages * 10

                if child_node.state not in frontier_set:
                    priority = int(child_node.h) + int(child_node.g)
                    pqueue.put((priority, child_node))
                    frontier_set.add(child_node.state)

    if algo == "dfs":
        DFS()
    elif algo == "astar":
        Astar()

    f = "grading_case/output" + str(i) + ".txt"
    file = open(f, "r")
    content = file.read()

    if str(goal_node.packages) == content:
        score += 1

    if overtime:
        goal_node.packages = -1

    print(str(goal_node.packages) + " " + content)

    # print(goal_node.state.package_location_set)

print(score)

