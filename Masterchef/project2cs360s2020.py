

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


contestants = []
count = 0

for line in content:
    if count == 0:
        n = line
    elif count == 1:
        algo = line
    else:
        ID, cooking, cap_A, cap_B, picked = line.split(",")
        contestants.append(Contestant(ID, cooking, cap_A, cap_B, picked))
    count += 1
