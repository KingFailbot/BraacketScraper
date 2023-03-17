import csv
import time

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook

from Placing import Placing

from Player import Player
from Player import HeadToHeadPlayer

from set import Set


def scrapeLast200Tournaments():
    r = requests.get('https://braacket.com/league/MNUltNew/tournament?rows=200')
    bracketURL = "https://braacket.com"
    print(r)

    links = []
    tournaments = []
    entrantCounts = []
    dates = []
    matches = []
    # print(len(entrantCounts))
    soup = BeautifulSoup(r.content, 'html.parser')

    count = 0
    truecount = 0
    for link in soup.find_all('a'):
        text = link.get('href')
        delimiter = -1
        if text is not None:
            delimiter = text.find("/tournament/")
        if delimiter != -1:
            if count % 2 != 1:
                text = bracketURL + text
                links.append(text)
                # print(text)
                truecount = truecount + 1
            count = count + 1

    # print("Links: ", truecount)
    # print(r.content)

    s = soup.find_all('div', class_='my-dashboard-values-sub')
    count = 0

    for line in s:
        text = line.getText()
        date = text.find('Date')
        if (date != -1) & (text is not None):
            text = text.replace('\n', '')
            text = text.split('Date', 1)[1]
            # print(text)
            dates.append(text)
            count = count + 1

    # print("Date Count: ", count)

    s = soup.find_all('td', class_='ellipsis')
    count = 0
    # tournament name grabber
    for line in s:
        line.get('href')
        text = line.getText()
        delimiter = text.find("\n")
        if (delimiter != -1) & (text is not None):
            text = text.replace("\n", "")
            tournaments.append(text)
            # print(text)
            count = count + 1

    # print("Tournament Count: ", count)

    s = soup.find_all('span', class_='text-bold')
    count = 0

    for line in s:
        text = line.getText()
        leftParen = text.find('(')
        if (leftParen != -1) & (text is not None):
            text = text.split('(', 1)[1]
            text = text.split(')', 1)[0]
            entrantCounts.append(text)
            # print(entrantCounts[count])

            count = count + 1

    # print("Entrant Counts: ", count)

    s = soup.find_all('div', class_='my-dashboard-values-sub')
    count = 0
    truecount = 0

    for line in s:
        text = line.getText()
        date = text.find('Matches')
        if (date != -1) & (text is not None):
            if count % 2 == 0:
                text = text.split('Matches', 1)[1]
                text = text.replace('\n', '')
                text = text.split("/", 1)[1]
                text = text.replace("\t", '')

                # print(text)
                matches.append(text)
                truecount = truecount + 1
            count = count + 1

    # print("Matches Count: ", truecount)

    print('')
    print("ArraySize for Tournaments", len(tournaments))
    print('ArraySize for Dates', len(dates))
    print("ArraySize for Entrants", len(entrantCounts))
    print("ArraySize for Links", len(links))

    areEqual = len(tournaments) == len(entrantCounts)
    areEqual = areEqual & (len(tournaments) == len(links))
    if areEqual:
        with open('Last200Tournaments.csv', 'w', newline='') as new_file:

            pairs = []
            for t, d, e, m, l in zip(tournaments, dates, entrantCounts, matches, links):
                item = {'Tournament': t, 'Date': d, 'Entrants': e, 'Matches': m, "Link": l}
                pairs.append(item)

            fieldnames = ['Tournament', 'Date', 'Entrants', 'Matches', 'Link']

            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')

            csv_writer.writeheader()
            for row in pairs:
                csv_writer.writerow(row)
    return links


def getAllTextInstances(array, soup, classType, className, display):
    for item in soup.find_all(classType, class_=className):

        if item != None:
            item = item.getText()
            item = removeWhiteSpace(item)
            if display:
                print(item)
            array.append(item)
    return array



def removeifContains(word, target):
    delim = word.find(target)
    if delim != -1:
        word = word.replace(target, '')
    return word


def getSeasonName(date):
    if date.find('2022') > -1:
        array = ['April', 'May', 'June', 'July', 'August']
        if (findAnyInString(array, date)):
            return "Summer 2022"
        else:
            return "Fall 2022"
    else:
        return "Spring 2023"


def findAnyInString(array, date):
    for i in array:
        if date.find(i) > -1:
            return True
    return False


def cleanString(word):
    word = word.replace('/', '')
    word = word.replace('\\', '')
    word = word.replace(':', '')
    word = word.replace('*', '')
    word = word.replace('?', '')
    word = word.replace('\"', '')
    word = word.replace('<', '')
    word = word.replace('>', '')
    word = word.replace('|', '')
    word = word.replace(',', '')
    return word


def replaceAltWithPlayer(word, players, alts):
    index = alts.index(word)
    """
    if(len(players) != len(alts)):
        print("ALTS AND PLAYERS NOT EQUAL")
    
    """
    if index < len(players):
        return players[index]
    else:
        return word


def cutString(word, start, end):
    contains = word.find(start)
    if contains != -1:
        word = word.split(start)[1]
    contains = word.find(end)
    if contains != -1:
        word = word.split(end)[0]
    return word


def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False


def removeWhiteSpace(word):
    word = removeifContains(word, '\n')
    word = removeifContains(word, "\t")
    word = removeifContains(word, " ")
    return word


def getHeader(url):
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('a', class_='text-bold')
    tournamentName = s.getText()
    tournamentName = cleanString(tournamentName)
    print(tournamentName)
    s = soup.find_all('div', class_='btn btn-default')
    date = s[1].getText()
    entrants = s[2].getText()
    sets = s[3].getText()
    date = removeWhiteSpace(date)
    entrants = removeWhiteSpace(entrants)
    entrants = cutString(entrants, '/', 'NA')
    sets = removeWhiteSpace(sets)
    sets = cutString(sets, '/', 'NA')

    s = soup.find('div', class_="my-dashboard-text text-left read-more-target info-read-more")
    s = s.find('a')
    link = s.get('href')

    return tournamentName, date, entrants, sets, link


def getPlayersAndAlts(url):
    players = []
    alts = []
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    for alt in soup.find_all('td', class_='ellipsis'):
        alt = alt.getText()
        alt = removeWhiteSpace(alt)
        alts.append(alt)
    for player in soup.find_all('span', class_='hidden-xs'):
        player = player.getText()
        if player.find("  ") != -1:
            players.append(removeWhiteSpace(player))

    return players, alts


def getDoubleElimN(number):
    n = 1
    while number > pow(2, n + 1):
        n = n + 1
    return n


def getDoubleElimPlacement(number):
    if number < 5:
        return number
    n = getDoubleElimN(number)
    if number > (pow(2, n) + pow(2, (n - 1))):
        return (pow(2, n) + pow(2, (n - 1))) + 1
    return pow(2, n) + 1


def scrapeATournament(url, workBook, placementFile, headToHeadWB, headToHeadFile):
    """
    Needed parameters
    tournamentName
    date
    firstPlace
    Entrants
    Sets played
    OG Bracket Link
    League Link
    """

    tournamentName, date, entrants, sets, link = getHeader(url)
    print("Date:", date)
    print("Entrants:", entrants)
    print("Sets:", sets)
    print("ogLink:", link)
    print("braacket link:", url)
    time.sleep(2)

    count = 1
    rankingURL = url + "/ranking?rows=200"
    players, alts = getPlayersAndAlts(rankingURL)
    nums = []
    for _ in players:
        nums.append(getDoubleElimPlacement(count))
        count = count + 1
    first = players[0]
    print('First:', first)

    titleFields = ['Tournament Name', 'Date', 'Winner', 'Entrants', 'Sets Played', 'Original Link:', 'League Link']
    fields = [tournamentName, date, first, entrants, sets, link, url]
    fieldnames = ['Placement', 'Tag', 'Alt']

    sheetname = tournamentName
    strlength = len(sheetname)
    if strlength > 30:
        sheetname = sheetname[:30]

    sheet = workBook.add_sheet(sheetname)
    for i in range(0, len(titleFields)):
        sheet.write(0, i, titleFields[i])
        sheet.write(1, i, fields[i])

    for i in range(0, len(fieldnames)):
        sheet.write(2, i, fieldnames[i])
    for i in range(0, len(nums)):
        sheet.write(3 + i, 0, nums[i])
        sheet.write(3 + i, 1, players[i])
        sheet.write(3 + i, 2, alts[i])

    workBook.save(placementFile)
    path = "Placements/" + getSeasonName(date) + "/" + tournamentName + ".csv"
    # filename = tournamentName + '.csv'

    with open(path, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        writer.writerow(fields)
        writer.writerow(fieldnames)
        for i in range(0, len(players)):
            writer.writerow([nums[i], players[i], alts[i]])

    time.sleep(2)
    getOneHeadToHead(url, titleFields, fields, headToHeadWB, headToHeadFile, players, alts)
    return fields


def countMinusOneRemaining(array, currIdx):
    count = 0
    for i in range(currIdx, len(array)):
        if int(array[i]) == -1:
            count = count + 1
    return count


def scrapeLast200Placements():
    links = scrapeLast200Tournaments()

    # url = "https://braacket.com/tournament/0158DF57-0695-4D2F-A111-8E67687BF8D9"

    # url = "https://braacket.com/tournament/233866E7-DAC3-420B-B08C-1C014FEB2206"
    placementWB = Workbook()
    placementFile = 'PR tournaments.xls'
    headToHeadWB = Workbook()
    headToHeadFile = 'HeadToHead.xls'

    time.sleep(2)
    #  newlinks = ["https://braacket.com/tournament/233866E7-DAC3-420B-B08C-1C014FEB2206",
    #              "https://braacket.com/tournament/0158DF57-0695-4D2F-A111-8E67687BF8D9"]
    titleFields = ['Tournament Name', 'Date', 'Winner', 'Entrants', 'Sets Played', 'Original Link:', 'League Link']
    names = []
    dates = []
    winners = []
    entrants = []
    sets = []
    oglink = []
    leaguelink = []

    titlesheet = placementWB.add_sheet("Tournaments")

    for i in range(0, len(titleFields)):
        titlesheet.write(0, i, titleFields[i])

    count = 0
    for i in reversed(links):
        time.sleep(2)
        attributes = scrapeATournament(i, placementWB, placementFile, headToHeadWB, headToHeadFile)
        names.append(attributes[0])
        dates.append(attributes[1])
        winners.append(attributes[2])
        entrants.append(attributes[3])
        sets.append(attributes[4])
        oglink.append(attributes[5])
        leaguelink.append((attributes[6]))
        for j in range(0, len(attributes)):
            titlesheet.write(count + 1, j, attributes[j])
        count = count + 1

    placementWB.save(placementFile)
    headToHeadWB.save(headToHeadFile)

    with open("tournaments.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        for i in range(0, len(names)):
            writer.writerow([names[i], dates[i], winners[i], entrants[i], sets[i], oglink[i], leaguelink[i]])


def calculateTournamentPoints(fileLocation, players, playernames):
    tournamentName = ''
    entrants = 0

    with open(fileLocation, 'r', encoding= 'utf-8') as file:
        reader = csv.reader(file)
        count = 0

        for row in reader:
            if count == 1:
                header = row[0].split("\t")
                tournamentName = header[0]
                entrants = int(header[3])
                print("Tournament:", tournamentName)
                print("Entrants: ", entrants)

            if (count > 2):
                info = row[0].split(("\t"))
                placement = int(info[0])
                tag = info[1]
                # print("Line:", count + 1)
                # print(row[0])
                if(len(info) > 2):
                    alt = info[2]
                else:
                    alt = info [1]
                # print(placement, tag, alt)
                result = Placing(tournamentName, entrants, placement)
                if playernames.__contains__(tag) == False:
                    playernames.append(tag)
                    thisPlayer = Player(tag)
                    thisPlayer.addPlacement(result, alt)
                    # thisPlayer.display()
                    # result.display()
                    players.append(thisPlayer)
                else:
                    index = playernames.index(tag)
                    thisPlayer = players[index]
                    thisPlayer.addPlacement(result, alt)
                    players[index] = thisPlayer

            count = count + 1
    return players, playernames


def printAllAlts():
    players = []
    playernames = []
    fileLocation = "Summer 2022/Inver Grove Fights #26.csv"

    filenames = []
    count = 0
    # filenames = ["Summer 2022/Inver Grove Fights #26.csv", "Summer 2022/Inver Grove Fights #29.csv"]
    with open("All tournaments.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if count > 0:
                content = 'All tournaments/' + row[0] + '.csv'
                filenames.append(content)
            count = count + 1

    for name in filenames:
        players, playernames = calculateTournamentPoints(name, players, playernames)
    players.sort(reverse=True)
    count = 0

    for p in players:
        if (p.tournamentsAttended() >= 1):
            print(p.name)
            p.printAlts()
            print()

            count = count + 1

    with open("alts.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(["Player: ", "Alts"])
        for i in players:
            i.alts.append(i.name)
            writer.writerow([(x,) for x in reversed(i.alts)])


def getHeadToHead(filename):
    url = "https://braacket.com/tournament/1F27B9A5-28A0-4C71-9191-AB690A07A1CD"


def getOneHeadToHead(url, titleFields, fields, headToHeadWB, headToHeadFile, players, alts):
    url = url + '/match'
    print(url)
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    winners = []
    losers = []
    winScore = []
    loseScore = []
    order = []
    Sets = []
    count = 0
    len1 = len(players)
    len2 = len(alts)
    if len1 > len2:
        for i in range(0, len2):
            print(players[i], alts[i])
        print(players[len1 - 1])
        print("NOT EQUAL!!!")
    elif len2 > len1:
        for i in range(0, len1):
            print(players[i], alts[i])
        print(alts[len2 - 1])
        print("NOT EQUAL!!!")
    else:
        print("Equal")


    count = 0
    for item in soup.find_all('table', class_='tournament_encounter-row'):
        entries = []
        count = count + 1

        entries = item.getText().split("\n")
        smallcount = 0;
        goodData = []
        for j in entries:
            j = removeWhiteSpace(j)
            if (j != '' and j!=' '):

                goodData.append(j)

                smallcount += 1
        if(len(goodData) > 4):
            if(not(( int(goodData[2]) == -1 )or (int(goodData[4]) == -1))):
                order.append(int(goodData[0]))
                if int(goodData[2]) > int(goodData[4]):
                    # print("Winner:", goodData[1])
                    winners.append(replaceAltWithPlayer(goodData[1], players, alts))
                    winScore.append(int(goodData[2]))
                    # print("Loser:", goodData[3])
                    losers.append(replaceAltWithPlayer(goodData[3], players, alts))
                    loseScore.append(int(goodData[4]))
                else:
                    # print("Loser:", goodData[1])
                    losers.append(replaceAltWithPlayer(goodData[1], players, alts))
                    loseScore.append(int(goodData[2]))
                    # print("Winner:", goodData[3])
                    winners.append(replaceAltWithPlayer(goodData[3], players, alts))
                    winScore.append(int(goodData[4]))
            else:
                print("DQ!!!")
    for i in range(0, len(winners)):
        set = Set(winners[i], losers[i], winScore[i], loseScore[i], order[i])
        Sets.append(set)
    Sets = sorted(Sets)

    date = fields[1]
    date = getSeasonName(date)
    tournamentName = fields[0]

    path = "HeadToHead/" + date + "/" + tournamentName + ".csv"

    row3 = ['Set Num', 'Winner', 'Loser', 'WS', 'LS', 'Best of', 'Game']
    with open(path, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        writer.writerow(fields)
        writer.writerow(row3)
        for i in Sets:
            writer.writerow([i.order, i.winner, i.loser, i.winningScore, i.losingScore, i.outOf, i.game])
    sheetname = tournamentName
    strlength = len(sheetname)
    if strlength > 30:
        sheetname = sheetname[:30]

    sheet = headToHeadWB.add_sheet(sheetname)
    for i in range(0, len(titleFields)):
        sheet.write(0, i, titleFields[i])
        sheet.write(1, i, fields[i])

    for i in range(0, len(row3)):
        sheet.write(2, i, row3[i])
    for i in range(0, len(Sets)):
        sheet.write(3 + i, 0, Sets[i].order)
        sheet.write(3 + i, 1, Sets[i].winner)
        sheet.write(3 + i, 2, Sets[i].loser)
        sheet.write(3 + i, 3, Sets[i].winningScore)
        sheet.write(3 + i, 4, Sets[i].losingScore)
        sheet.write(3 + i, 5, Sets[i].outOf)
        sheet.write(3 + i, 6, Sets[i].game)
    headToHeadWB.save(headToHeadFile)



    """
    pathname = Path("HeadToHead/" + date)
    print(pathname)
    pathname.mkdir(parents=True)
    fpath = (pathname / filename).with_suffix('.csv')
    print(fpath)
    """


def getSeasonNameTest():
    print(getSeasonName("05 April 2022"))
    print(getSeasonName("01 May 2022"))
    print(getSeasonName("30 June 2022"))
    print(getSeasonName("31 July 2022"))
    print(getSeasonName("12 August 2022"))

    print(getSeasonName("22 September 2022"))
    print(getSeasonName("05 October 2022"))
    print(getSeasonName("15 November 2022"))
    print(getSeasonName("21 December 2022"))

    print(getSeasonName("06 January 2023"))
    print(getSeasonName("25 February 2023"))
    print(getSeasonName("24 March 2023"))
    print(getSeasonName("04 April 2023"))

    date = "04 April 2023"
    if date.find("2022") > 0:
        print("true")
    else:
        print("false")


def testOneTournament():
    wb = Workbook()
    url = "https://braacket.com/tournament/824F229F-9115-4C42-B5EC-A55BA3930582"
    placementFile = 'PR tournaments.xls'
    wb2 = Workbook()
    file = 'HeadToHead.xls'
    scrapeATournament(url, wb, placementFile, wb2, file)


def getAllGameFives(playernames, players):
    dates = []
    tournaments = []
    with open("tournaments.csv", 'r', encoding= 'utf-8') as csvfile:
        reader = csv.reader((csvfile))
        count = 0

        for row in reader:
            if count > 0:
                info = row[0].split('\t')
                tournaments.append(info[0])
                dates.append(info[1])
            count += 1

    for i in range(0, len(tournaments)):
        filename = "HeadToHead\\"
        filename = filename + getSeasonName(dates[i]) + '\\' + tournaments[i] + '.csv'
        getOneGameFive(filename, playernames, players)
    temp = players
    players.sort()
    for p in players:
        p.display()
    fields = ["Player", "Wins", "Loses", "Win %"]
    with open("GameFive.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(fields)
        for p in players:
            writer.writerow([p.name, len(p.setWins), len(p.setLoses), p.getWinPercent()])
    players = temp
def getOneGameFive(filename, names, players):
    with open(filename, 'r', encoding= 'utf-8') as file:
        reader = csv.reader(file, delimiter= '\t')
        count = 0
        sets = []
        for row in reader:
            if count == 1:
                # tournamentName = row[0].split('\t')[0]
                tournamentName = row[0]
                print(tournamentName)
            if count > 2:
                if row[0] != '':
                    # info = row[0].split('\t')
                    # set = Set(info[1], info[2], int(info[3]), int(info[4]), int(info[0]))
                    set = Set(row[1], row[2], int(row[3]), int(row[4]), int(row[0]))
                    set.addTournament(tournamentName)
                    sets.append(set)
            count += 1
            # print(count)
    for set in sets:
        if (set.game == 5):
            if(not (names.__contains__(set.winner))):
                names.append(set.winner)
                players.append(HeadToHeadPlayer(set.winner))
            if(not (names.__contains__(set.loser))):
                names.append(set.loser)
                players.append(HeadToHeadPlayer(set.loser))
            index = names.index(set.winner)
            players[index].addWin(set)
            index = names.index(set.loser)
            players[index].addLose(set)
        set.display()

def getb05(playernames, players):
    dates = []
    tournaments = []
    with open("tournaments.csv", 'r', encoding= 'utf-8') as csvfile:
        reader = csv.reader((csvfile))
        count = 0

        for row in reader:
            if count > 0:
                info = row[0].split('\t')
                tournaments.append(info[0])
                dates.append(info[1])
            count += 1

    for i in range(0, len(tournaments)):
        filename = "HeadToHead\\"
        filename = filename + getSeasonName(dates[i]) + '\\' + tournaments[i] + '.csv'
        getOneb05(filename, playernames, players)

    temp = players
    players.sort()
    for p in players:
        p.display()
    fields = ["Player", "Wins", "Loses", "Win %"]
    with open("BestofFive.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(fields)
        for p in players:
            writer.writerow([p.name, len(p.setWins), len(p.setLoses), p.getWinPercent()])
    players = temp

def getOneb05(filename, names, players):
    with open(filename, 'r', encoding= 'utf-8') as file:
        reader = csv.reader(file, delimiter= '\t')
        count = 0
        sets = []
        for row in reader:
            if count == 1:
                # tournamentName = row[0].split('\t')[0]
                tournamentName = row[0]
                print(tournamentName)
            if count > 2:
                if row[0] != '':
                    # info = row[0].split('\t')
                    # set = Set(info[1], info[2], int(info[3]), int(info[4]), int(info[0]))
                    set = Set(row[1], row[2], int(row[3]), int(row[4]), int(row[0]))
                    set.addTournament(tournamentName)
                    sets.append(set)
            count += 1
            # print(count)
    for set in sets:
        if (set.outOf == 5):
            if(not (names.__contains__(set.winner))):
                names.append(set.winner)
                players.append(HeadToHeadPlayer(set.winner))
            if(not (names.__contains__(set.loser))):
                names.append(set.loser)
                players.append(HeadToHeadPlayer(set.loser))
            index = names.index(set.winner)
            players[index].addWin(set)
            index = names.index(set.loser)
            players[index].addLose(set)

# testOneTournament()
# scrapeLast200Placements()

names = []
players = []
filename = "HeadToHead/Fall 2022/Keepers of the North #12.csv"

getOneGameFive(filename, names, players)
# getAllGameFives(names, players)
# getb05(names, players)
for i in players:
    i.displaySets()


"""
Tournaments: 
LGS: 
https://braacket.com/tournament/C63AA01C-2C2F-4405-964A-86CC007D8051/match
Keepers of the North:
https://braacket.com/tournament/7E937162-5BFF-4E12-ADC9-DCD4F8062813/match
Med City #100:
https://braacket.com/tournament/0F138AAC-8338-49F5-A364-9831A5AE94BA/match


"""