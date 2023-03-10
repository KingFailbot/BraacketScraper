from Placing import Placing


class Player:

    def display(self):
        print("Player:", self.name)
        print("Tournaments attended:", self.tournamentsAttended())
        print("Points:", self.points)

    def __init__(self, name):
        self.name = name
        self.results = []
        self.alts = []
        self.points = 0.0

    def addPlacement(self, placement, alt):
        if (self.alts.__contains__(alt) == False):
            self.alts.append(alt)
        (self.results).append(placement)
        self.points += placement.points

    def tournamentsAttended(self):
        count = 0
        for i in self.results:
            count = count + 1
        return count

    def printResults(self):
        for i in self.results:
            i.display()

    def printAlts(self):
        for i in self.alts:
            print(i)

    def printOneLine(self):
        print(self.name, self.points, self.tournamentsAttended())

    def __lt__(self, other):
        return self.points < other.points

    def __le__(self, other):
        return self.points <= other.points

    def __eq__(self, other):
        return self.points == other.points

    def __ge__(self, other):
        return self.points >= other.points

    def __gt__(self, other):
        return self.points > other.points

    def __ne__(self, other):
        return self.points != other.points
