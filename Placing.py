"""Utility function, returns the largest power of 2 smaller than the number.

param number the number that a power of 2 is being in relation to

returns n the largest exponent such that 2^n < number
"""


def getDoubleEliminationN(number):
    n = 1
    while number > pow(2, n + 1):
        n = n + 1
    return n


"""Utility Function that returns the placement from a number (if 18th in list, placement is 17th)

:param number, the ordered index of the placement

:returns the first argument is the placement

:returns the second argument is the number of people who got that place
"""


def getDoubleEliminationPlacement(number):
    if number < 5:
        return number
    n = getDoubleEliminationN(number)
    if number > (pow(2, n) + pow(2, (n - 1))):
        return (pow(2, n) + pow(2, (n - 1))) + 1, pow(2, n - 1)  # if the placement is greater than the power of 2 plus
    # the next smallest power of two, then the placement is the above expression
    return pow(2, n) + 1, pow(2, n - 1)  # in both cases, return the second arg, the number of people who share your
    # place


"""Returns the number of people who placed equal or better than the placement

:param number, the ordered index of the placement

:returns the number of people who tied with a certain placement
"""


def getEqualOrBetterPlacements(number):
    if number < 5:
        return number
    n, n1 = getDoubleEliminationPlacement(number)
    return n + n1 - 1


"""A class containing one player's placement info for one tournament

"""


class Placing:
    tournament = ""
    date = ""
    place = 101
    entrants = 1
    points = 0

    """Prints all relevant info for a placement
    """
    def display(self):
        print(self.tournament, self.date, self.entrants, self.place, self.points)

    """The constructor for the class
    
    Calculates the point value of the placement when called
    
    :param tournament, the tournament the placement happened at
    
    :param date, the string containing the date of the tournament
    
    :param entrant, the number of entrants at the tournament
    
    :param place, the placement of the player at the tournament
    """
    def __init__(self, tournament, date, entrant, place):
        self.tournament = tournament
        self.date = date
        self.entrants = entrant
        self.place = place
        self.points = ((10 * entrant) / (getEqualOrBetterPlacements(place)))
