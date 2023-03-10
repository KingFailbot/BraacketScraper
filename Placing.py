class Placing:
    tournament = ""
    place = 101
    entrants = 1
    points = 0

    def display(self):
        print(self.tournament,self.entrants, self.place, self.points)


    def getEqualorBetterPlacements(self, number):
        if number < 5:
            return number
        n, n1 = self.getDoubleElimPlacement(number)
        return (n+ n1-1)


    def getDoubleElimN(self, number):
        n = 1
        while number > pow(2, n + 1):
            n = n + 1
        return n


    def getDoubleElimPlacement(self, number):
        if number < 5:
            return number
        n = self.getDoubleElimN(number)
        if number > (pow(2, n) + pow(2, (n - 1))):
            return (pow(2, n) + pow(2, (n - 1))) + 1, pow(2, n-1)
        return pow(2, n) + 1, pow(2, n-1)

    def __init__(self, tournament, entrant, place):
        self.tournament = tournament
        self.entrants = entrant
        self.place = place
        self.points = ((10 * entrant) / (self.getEqualorBetterPlacements(place)))

