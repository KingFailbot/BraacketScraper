class SeasonFinder:
    def __init__(self, target):
        self.target = target


    def isInSeason(self, date):
        if self.target.__contains__(self.inWhichSeason(date)):
            return True
        return False



    def inWhichSeason(self, date):
        if date.find('2022') > -1:
            array = ['April', 'May', 'June', 'July', 'August']
            if (self.findAnyInString(array, date)):
                return 1
            else:
                return 2
        elif date.find('2023') > -1:
            array = ['January', 'February', 'March', 'April']
            if (self.findAnyInString(array, date)):
                return 3
            array = [ 'May', 'June', 'July', 'August']
            if self.findAnyInString(array, date):
                return 4
            else:
                return 5
        else:
            return -1


    def findAnyInString(self, array, date):
        for i in array:
            if date.find(i) > -1:
                return True
        return False


    def getSeasonName(self, date):
        if self.inWhichSeason(date) == 1:
            return "Summer 2022"
        if self.inWhichSeason(date) == 2:
            return "Fall 2022"
        if self.inWhichSeason(date) == 3:
            return "Spring 2023"
        if self.inWhichSeason(date) == 4:
            return "Summer 2023"
        if self.inWhichSeason(date) == 5:
            return "Fall 2023"
        return "NA"


