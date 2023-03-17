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
              self.outOf, "Game", self.game, "Tournament:", self.tournament)

    def addTournament(self, tournament):
        self.tournament = tournament

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

