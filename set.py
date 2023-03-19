class Set:
    def __init__(self, winner, loser, wscore, lscore, order):
        self.winner = winner
        self.loser = loser
        self.winningScore = wscore
        self.losingScore = lscore
        self.order = order
        self.outOf = wscore * 2 - 1
        self.game = wscore + lscore

    def display(self):
        print("#", self.order, self.winner, self.loser, self.winningScore, '-', self.losingScore, "Best of:", self.outOf, "Game", self.game)

    def displayAll(self):
        """
        print("#", self.order, self.winner, self.loser, self.winningScore, '-', self.losingScore, "Best of:",
              self.outOf, "Game", self.game, "Tournament:", self.tournament)
        """
        print(self.winner, self.loser, self.winningScore, '-', self.losingScore, "Best of:",
              self.outOf, "Game", self.game, "Tournament:", self.tournament, "Date:", self.date)

    def addTournament(self, tournament):
        self.tournament = tournament


    def addDate(self, date):
        self.date = date

    def __lt__(self, other):
        return self.order < other.order

    def __le__(self, other):
        return self.order <= other.order

    def __eq__(self, other):
        return self.order == other.order

    def __ge__(self, other):
        return self.order >= other.order

    def __gt__(self, other):
        return self.order > other.order

    def __ne__(self, other):
        return self.order != other.order

class SetDecider:
    def __init__(self, mode):
        self.mode = mode

    def decide(self, set):
        if self.mode == 1:
            bool = self.isBestOfThree(set)
        elif self.mode == 2:
            bool = self.isGameThree(set)
        elif self.mode == 3:
            bool = self.isBestOfFive(set)
        elif self.mode == 4:
            bool = self.isGameFive(set)
        elif self.mode == 5:
            bool = self.isBestOfOne(set)
        elif self.mode == 6:
            bool = self.isSummer2022(set)
        elif self.mode == 7:
            bool = self.isFall2022(set)
        elif self.mode == 8:
            bool = self.isSpring2023(set)
        else:
            bool = self.isSet(set)

        return bool


    def isSet(self, set):
        return True


    def isGameFive(self, set):
        if ((set.game == 5) and (set.outOf == 5)):
            return True
        return False


    def isBestOfFive(self, set):
        if(set.outOf == 5):
            return True
        return False


    def isBestOfThree(self, set):
        if(set.outOf == 3):
            return True
        return False


    def isGameThree(self, set):
        if((set.outOf == 3) and (set.game == 3)):
            return True
        return False

    def isBestOfOne(self,set):
        if((set.outOf == 1)):
            return True
        return False


    def isSpring2023(self, set):
        temp = set.date
        if(not (temp.find("2023") > -1)):
            return False
        if(temp.find("January") > -1):
            return True
        if (temp.find("February") > -1):
            return True
        if (temp.find("March") > -1):
            return True
        if (temp.find("April") > -1):
            return True
        return False


    def isSummer2022(self, set):
        temp = set.date
        if(not (temp.find("2022") > -1)):
            return False
        if(temp.find("April") > -1):
            return True
        if (temp.find("May") > -1):
            return True
        if (temp.find("June") > -1):
            return True
        if (temp.find("July") > -1):
            return True
        if (temp.find("August") > -1):
            return True
        return False


    def isFall2022(self, set):
        temp = set.date
        if(not (temp.find("2022") > -1)):
            return False
        if(temp.find("September") > -1):
            return True
        if (temp.find("October") > -1):
            return True
        if (temp.find("November") > -1):
            return True
        if (temp.find("December") > -1):
            return True
        return False