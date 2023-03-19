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
        self.setWins = []
        self.setLoses = []
        self.points = 0.0
        self.trueSkill = 0.0
        self.braacket = 0.0


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


    def getAlts(self):
        return self.alts


    def getWinPercent(self):
        return len(self.setWins) / (len(self.setWins) + len(self.setLoses))


    def addWin(self, set):
        self.setWins.append(set)


    def addLoss(self, set):
        self.setLoses.append(set)


    def displayTotalRecord(self):
        print(self.name + ':', len(self.setWins), '-', len(self.setLoses))


    def hasAttendedAtLeast(self, number):
        if self.tournamentsAttended() >= number:
            return True
        return False

    def getTotalSets(self):
        return len(self.setWins) + len(self.setLoses)


    def getWinPercent(self):
        return len(self.setWins) / (len(self.setWins) + len(self.setLoses))


    def displaySets(self):
        print("Wins: ")
        for i in self.setWins:
            i.displayAll()
        print("Losses: ")
        for i in self.setLoses:
            i.displayAll()


    def getSetCountWithPlayer(self, opp):
        if (self.name == opp):
            return "--"
        else:
            wins = 0
            for w in self.setWins:
                if w.loser == opp:
                    wins += 1
            losses = 0
            for l in self.setLoses:
                if l.winner == opp:
                    losses += 1
            return str(wins) + " - " + str(losses)


    def getSetIntsWith(self, opp):
        losses = 0
        wins = 0
        if (self.name == opp):
            return wins, losses
        else:

            for w in self.setWins:
                if w.loser == opp:
                    wins += 1

            for l in self.setLoses:
                if l.winner == opp:
                    losses += 1
            return wins, losses

    def setTrueSkill(self, score):
        self.trueSkill = score


    def setBraacket(self, score):
        self.braacket = score


    def get7525(self):
        return (.75 * float(self.trueSkill) + .25 * float(self.braacket))


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

class HeadToHeadPlayer:
    def __init__(self, name):
        self.setWins = []
        self.setLoses = []
        self.name = name

    def getWinPercent(self):
        return len(self.setWins) / (len(self.setWins) + len(self.setLoses))

    def addWin(self, set):
        self.setWins.append(set)


    def addLose(self, set):
        self.setLoses.append(set)


    def display(self):
        print(self.name + ':', len(self.setWins), '-', len(self.setLoses))

    def getTotalSets(self):
        return len(self.setWins) + len(self.setLoses)

    def displaySets(self):
        print("Wins: ")
        for i in self.setWins:
            i.displayAll()
        print("Losses: ")
        for i in self.setLoses:
            i.displayAll()
    def __lt__(self, other):
        if self.getWinPercent() == other.getWinPercent():
            return self.getTotalSets() < other.getTotalSets()
        return self.getWinPercent() < other.getWinPercent()

    def __le__(self, other):
        if self.getWinPercent() == other.getWinPercent():
            return self.getTotalSets() <= other.getTotalSets()
        return self.getWinPercent() <= other.getWinPercent()

    def __eq__(self, other):
        if self.getWinPercent() == other.getWinPercent():
            return self.getTotalSets() == other.getTotalSets()
        return self.getWinPercent() == other.getWinPercent()

    def __ge__(self, other):
        if self.getWinPercent() == other.getWinPercent():
            return self.getTotalSets() >= other.getTotalSets()
        return self.getWinPercent() >= other.getWinPercent()

    def __gt__(self, other):
        if self.getWinPercent() == other.getWinPercent():
            return self.getTotalSets() > other.getTotalSets()

        return self.getWinPercent() > other.getWinPercent()

    def __ne__(self, other):
        if self.getWinPercent() == other.getWinPercent():
            return self.getTotalSets() != other.getTotalSets()
        return self.getWinPercent() != other.getWinPercent()