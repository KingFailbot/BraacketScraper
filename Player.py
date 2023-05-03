"""Player a class the represents the data of an individual player

Can contain information including a players placements, theSet records, names, and specific theSet records against
a player
"""


class Player:
    """Displays a players tag, # of tournaments attended, and the points a player has earned

    """

    def display(self):
        print("Player:", self.name)
        print("Tournaments attended:", self.tournamentsAttended())
        print("Points:", self.points)

    """Initializes a player
    
    Sets empty variables for a players placings (results) alternate tags, theSet wins and losses, and various ranking
    points
    
    :param name the players tag
    """

    def __init__(self, name):
        self.name = name
        self.results = []
        self.alts = []
        self.setWins = []
        self.setLoses = []
        self.points = 0.0
        self.trueSkill = 0.0
        self.braacket = 0.0

    """Adds a placement to the players placement data
    
    :param placement, the placement data to be added
    
    :param alt, the alternate tag used at the tournament
    """

    def addPlacement(self, placement, alt):
        if not self.alts.__contains__(alt):  # if the alt is not already included
            self.alts.append(alt)
        self.results.append(placement)
        self.points += placement.points  # add the points for the placement

    """Gives the number of tournaments a player has attended
    
    :returns the number of tournaments a player has attended
    """

    def tournamentsAttended(self):
        count = 0
        for _ in self.results:  # for every placement added
            count = count + 1
        return count

    """prints each placement a player has
    """

    def printResults(self):
        for i in self.results:
            i.display()

    """prints every alternate tag the player has used
    """

    def printAlts(self):
        for i in self.alts:
            print(i)

    """prints the players name, points, and number of tournaments attended
    """

    def printOneLine(self):
        print(self.name, self.points, self.tournamentsAttended())

    """ getter function for alts list
    
    :returns the list of every alternate tag used (strings)
    """

    def getAlts(self):
        return self.alts

    """ Returns the number of sets won / total sets
    
    :returns a float representing wins/total
    """

    def getWinPercent(self):
        return len(self.setWins) / (len(self.setWins) + len(self.setLoses))

    """Adds a theSet that the players won to the win list.
    
    :param theSet, the theSet to be added
    """

    def addWin(self, theSet):
        self.setWins.append(theSet)

    """Adds a theSet that the player lost to the win list.

        :param theSet, the theSet to be added
        """

    def addLoss(self, theSet):
        self.setLoses.append(theSet)

    """Displays a string in the format "WINS - LOSSES"
    """

    def displayTotalRecord(self):
        print(self.name + ':', len(self.setWins), '-', len(self.setLoses))

    """Utility function used to see if the players has attended a minimum number of tournaments
    
    :param number, the minimum number of tournaments
    
    :returns a boolean value of whether the tournaments attended is sufficient
    """

    def hasAttendedAtLeast(self, number):
        if self.tournamentsAttended() >= number:
            return True
        return False

    """Utility function that returns the total sets played
    
    :returns the count of sets played
    """

    def getTotalSets(self):
        return len(self.setWins) + len(self.setLoses)

    """Displays every theSet the player has played. Wins then losses
    """

    def displaySets(self):
        print("Wins: ")
        for i in self.setWins:
            i.displayAll()
        print("Losses: ")
        for i in self.setLoses:
            i.displayAll()

    """Gives the theSet count string between two players
    
    :param opp, the string name of the opponent
    
    :returns a string formatted like "WINS - LOSES"
    """
    def getSetCountWithPlayer(self, opp):
        if self.name == opp:  # if asked for theSet count with self, returns the --
            return "--"
        else:
            wins = 0
            for w in self.setWins:  # for every time the opponent is in theSet wins
                if w.loser == opp:
                    wins += 1
            losses = 0
            for loss in self.setLoses:
                if loss.winner == opp:
                    losses += 1
            return str(wins) + " - " + str(losses)

    """
    """
    def getSetIntsWith(self, opp):
        losses = 0
        wins = 0
        if self.name == opp:
            return wins, losses
        else:

            for w in self.setWins:
                if w.loser == opp:
                    wins += 1

            for loss in self.setLoses:
                if loss.winner == opp:
                    losses += 1
            return wins, losses

    """A function that gets every theSet that two players have played (two lists)
    
    :param opp, the opponent who was played against
    
    :returns wins the sets the player has won against the opponent
    
    :returns losses, the sets the player has lost against the opponent
    """
    def getSetsAgainst(self, opp):
        losses = []
        wins = []
        if self.name == opp:  # if the opponent is the current player, return all sets
            return wins, losses
        else:

            for w in self.setWins:
                if w.loser == opp:
                    wins.append(w)

            for loss in self.setLoses:
                if loss.winner == opp:
                    losses.append(loss)
            return wins, losses

    """Sets the TrueSkill score for a player
    
    :param score, the score to be theSet for the player's TrueSkill
    """
    def setTrueSkill(self, score):
        self.trueSkill = score

    """ Sets the braacket point score for a player
    
    :param score, the score in braacket points
    """
    def setBraacket(self, score):
        self.braacket = score

    """Returns the weighted average of players points
    
    :returns a float point value
    """
    def get7525(self):
        return .75 * float(self.trueSkill) + .25 * float(self.braacket)

    """Set of compare operations that sort players by number of points
    """
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
