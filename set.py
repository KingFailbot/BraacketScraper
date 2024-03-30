""" A class that represents the data of a theSet

"""


class Set:
    """The constructor with required information for a theSet

    Includes a winner, loser, the winning and losing scores, and the order of theSet within tournament

    param winner, the winner of the theSet (string)

    param loser, the loser of the theSet (string)

    param wscore, the score the winner won with

    param losingScore, the score the loser lost with

    param order, the index of this theSet within the tournament
    """

    def __init__(self, winner, loser, wscore, losingScore, order):
        self.tournament = None
        self.date = None
        self.winner = winner
        self.loser = loser
        self.winningScore = wscore
        self.losingScore = losingScore
        self.order = order
        self.outOf = wscore * 2 - 1
        self.game = wscore + losingScore

    """Displays all required parameters
    """

    def display(self):
        print("#", self.order, self.winner, self.loser, self.winningScore, '-', self.losingScore, "Best of:",
              self.outOf, "Game", self.game)

    """Displays required parameters, and tournament name/date
    """

    def displayAll(self):
        print(self.winner, self.loser, self.winningScore, '-', self.losingScore, "Best of:",
              self.outOf, "Game", self.game, "Tournament:", self.tournament, "Date:", self.date)

    """ adds a tournament
    
    :param tournament, the string name of this sets tournament
    """

    def addTournament(self, tournament):
        self.tournament = tournament

    """ adds the date to the tournament
    
    :param date, the string date of this theSet
    """

    def addDate(self, date):
        self.date = date

    """ Custom comparator functions that sort sets by their index number
    """

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


"""Tests if the set went to game 5

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isGameFive(theSet):
    if (theSet.game == 5) and (theSet.outOf == 5):
        return True
    return False


""" Tests if the set was best of 5

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isBestOfFive(theSet):
    if theSet.outOf == 5:
        return True
    return False


""" Tests if the set was best of three

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isBestOfThree(theSet):
    if theSet.outOf == 3:
        return True
    return False


""" tests if the set went to game 3 and was best of three

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isGameThree(theSet):
    if (theSet.outOf == 3) and (theSet.game == 3):
        return True
    return False


""" tests if the set was best of one (hopefully not)

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isBestOfOne(theSet):
    if theSet.outOf == 1:
        return True
    return False


""" tests if the set was in the spring 2023 season

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isSpring2023(theSet):
    temp = theSet.date
    if not (temp.find("2023") > -1):
        return False
    if temp.find("January") > -1:
        return True
    if temp.find("February") > -1:
        return True
    if temp.find("March") > -1:
        return True
    if temp.find("April") > -1:
        return True
    return False

def isSummer2023(theSet):
    temp = theSet.date
    if not (temp.find("2023") > -1):
        return False
    if temp.find("May") > -1:
        return True
    if temp.find("June") > -1:
        return True
    if temp.find("July") > -1:
        return True
    if temp.find("August") > -1:
        return True
    return False

""" tests if the set was in the summer Season 2022

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isSummer2022(theSet):
    temp = theSet.date
    if not (temp.find("2022") > -1):
        return False
    if temp.find("April") > -1:
        return True
    if temp.find("May") > -1:
        return True
    if temp.find("June") > -1:
        return True
    if temp.find("July") > -1:
        return True
    if temp.find("August") > -1:
        return True
    return False


""" tests if the set was in the fall 2022 season

:param theSet, the set that will be tested for the condition

:returns if the set meats the condition
"""


def isFall2022(theSet):
    temp = theSet.date
    if not (temp.find("2022") > -1):
        return False
    if temp.find("September") > -1:
        return True
    if temp.find("October") > -1:
        return True
    if temp.find("November") > -1:
        return True
    if temp.find("December") > -1:
        return True
    return False

def isFall2023(theSet):
    temp = theSet.date
    if not (temp.find("2023") > -1):
        return False
    if temp.find("September") > -1:
        return True
    if temp.find("October") > -1:
        return True
    if temp.find("November") > -1:
        return True
    if temp.find("December") > -1:
        return True
    return False

"""a class that decides if a theSet follows a desired condition

"""


class SetDecider:

    """ determines what the set decider is looking for

    param mode, the condition that sets will be tested against

    CONDITIONS
    1: The set is best of 3
    2: The set went game 3
    3: The set was best of 5
    4: The set went game 5
    5: The set was best of one
    6: The set was in summer 2022
    7: The set was in fall 2022
    8: The set was in spring 2023
    9: The set was in Summer 2023
    Else: returns true
    """
    def __init__(self, mode):
        self.mode = mode

    """ determines if the set follows the condition inputted in constructor
    
    :returns a boolean value for if the set was true
    """
    def decide(self, theSet):
        if self.mode == 1:
            isCondition = isBestOfThree(theSet)
        elif self.mode == 2:
            isCondition = isGameThree(theSet)
        elif self.mode == 3:
            isCondition = isBestOfFive(theSet)
        elif self.mode == 4:
            isCondition = isGameFive(theSet)
        elif self.mode == 5:
            isCondition = isBestOfOne(theSet)
        elif self.mode == 6:
            isCondition = isSummer2022(theSet)
        elif self.mode == 7:
            isCondition = isFall2022(theSet)
        elif self.mode == 8:
            isCondition = isSpring2023(theSet)
        elif self.mode == 9:
            isCondition = isSummer2023(theSet)
        elif self.mode == 10:
            isCondition = isFall2023(theSet)
        else:
            return True

        return isCondition
