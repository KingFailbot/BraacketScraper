import csv
import time

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook

from Placing import Placing

from Player import Player

from set import Set
from set import SetDecider

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


def addAllPlacements(file, cond, players, playernames):
    with open(file, 'r', encoding= 'utf-8') as file:
        reader = csv.reader(file, delimiter= '\t')
        count = 0
        tournaments = []
        dates = []
        for row in reader:
            if count > 0:
                if(cond.__contains__(getSeasonName(row[1]))):
                    tournaments.append(row[0])
                    dates.append(row[1])
            count += 1
    count = 0
    for bracket in tournaments:
        link = "Placements\\" + getSeasonName(dates[count]) + "\\" + bracket + ".csv"
        calculateTournamentPoints(link, players, playernames)
        count += 1


def printAllAlts():

    # fileLocation = "Summer 2022/Inver Grove Fights #26.csv"

    filenames = []
    count = 0
    # filenames = ["Summer 2022/Inver Grove Fights #26.csv", "Summer 2022/Inver Grove Fights #29.csv"]
    """
    with open("tournaments.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if count > 0:
                content = 'All tournaments/' + row[0] + '.csv'
                filenames.append(content)
            count = count + 1

    for name in filenames:
        players, playernames = calculateTournamentPoints(name, players, playernames)
    """
    players = []
    playernames = []
    seasons = ["Spring 2023", "Fall 2022", "Summer 2022"]
    # seasons = ["Spring 2023"]
    addAllPlacements("tournaments.csv", seasons, players, playernames)

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
            row = [a for a in i.alts]
            row = [i.name] + row
            writer.writerow(row)
            # writer.writerow([(x,) for x in reversed(i.alts)])


def getHeadToHead(filename):
    url = "https://braacket.com/tournament/1F27B9A5-28A0-4C71-9191-AB690A07A1CD"


def getOneHeadToHead(url, titleFields, fields, headToHeadWB, headToHeadFile, players, alts):
    url = url + '/match'
    print(url)
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    Sets = []
    URLs = []
    for link in soup.find_all('a'):
        text = link.get('href')
        delimiter = -1
        if text is not None:
            delimiter = text.find("/stage/")
        if delimiter != -1:
            text = "https://braacket.com" + text
            text = removeifContains(text, '?')
            print(text)
            URLs.append(text)
    if len(URLs) == 1:
        severalURLs = False
    else:
        severalURLs = True
    if not severalURLs:
        scrapeOneH2HPage(url, Sets, players, alts, soup, severalURLs)
        row3 = ['Set Num', 'Winner', 'Loser', 'WS', 'LS', 'Best of', 'Game']
    else:
        print("MULTIPLE PHASES:")
        row3 = ['Set Num', 'Winner', 'Loser', 'WS', 'LS', 'Best of', 'Game', '**MULTIPLE BRACKET PHASES**']
        for phase in URLs:
            scrapeOneH2HPage(phase, Sets, players, alts, soup, severalURLs)
    Sets = sorted(Sets)

    date = fields[1]
    date = getSeasonName(date)
    tournamentName = fields[0]

    path = "HeadToHead/" + date + "/" + tournamentName + ".csv"


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


def scrapeOneH2HPage(url, sets, players, alts, soup, multiple):
    if(multiple):
        time.sleep(2)
        r = requests.get(url)
        print(r)
        soup = BeautifulSoup(r.content, 'html.parser')
    winners = []
    losers = []
    winScore = []
    loseScore = []
    order = []
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
        count = count + 1

        entries = item.getText().split("\n")
        smallcount = 0;
        goodData = []
        for j in entries:
            j = removeWhiteSpace(j)
            if (j != '' and j != ' '):
                goodData.append(j)

                smallcount += 1
        if (len(goodData) > 4):
            if (not ((int(goodData[2]) == -1) or (int(goodData[4]) == -1))):
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
    for i in range(0, len(winners)):
        set = Set(winners[i], losers[i], winScore[i], loseScore[i], order[i])
        sets.append(set)


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


def testScrapeOneTournament():
    wb = Workbook()
    url = "https://braacket.com/tournament/228979B6-A101-486A-AADE-73047E5F0025"
    placementFile = 'PR tournaments.xls'
    wb2 = Workbook()
    file = 'HeadToHead.xls'
    scrapeATournament(url, wb, placementFile, wb2, file)


def getAllSetsWith(cond):
    dates = []
    tournaments = []
    sets = []
    with open("tournaments.csv", 'r', encoding='utf-8') as csvfile:
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
        getOneTournamentSetsWith(cond, sets, filename)
    return sets


def getOneTournamentSetsWith(cond, sets, filename):
    with open(filename, 'r', encoding= 'utf-8') as file:
        reader = csv.reader(file, delimiter= '\t')
        count = 0
        for row in reader:
            if count == 1:
                # tournamentName = row[0].split('\t')[0]
                tournamentName = row[0]
                date = row[1]

            if count > 2:
                if row[0] != '':
                    # info = row[0].split('\t')
                    # set = Set(info[1], info[2], int(info[3]), int(info[4]), int(info[0]))
                    set = Set(row[1], row[2], int(row[3]), int(row[4]), int(row[0]))
                    set.addTournament(tournamentName)
                    set.addDate(date)
                    if cond.decide(set):
                        sets.append(set)
            count = count + 1


def setDeciderTester():
    print("Testing...")
    sets = []
    set = Set("Loaf", "Lucky", 3, 2, 1)
    sets.append(set)
    set2 = Set("Violet", "Meatflap", 2, 1, 1)
    sets.append(set2)
    set3 = Set("Ventura", "Big Will", 2, 0, 1)
    sets.append(set3)
    set4 = Set("Truth", "Barb", 3, 0, 1)
    sets.append(set4)
    decider = SetDecider(1)
    if decider.decide(set3):
        print("TRUE")
    else:
        print("FALSE")
    for i in range(0, 5):
        decider.mode = i
        print("Round", i)
        for set in sets:
            if decider.decide(set):
                print("Set:", set.winner, "Iter:", i)


def winrateSort(player):
    return player.getWinPercent()


def attendanceSort(player):
    return player.tournamentsAttended()


def setsPlayedSort(player):
    return player.getTotalSets()


def getSetDistribution(sets):
    sweep = 0
    threeone = 0
    threetwo = 0

    for set in sets:
        if (set.losingScore == 0):
            sweep += 1
        elif (set.outOf == set.game):
            threetwo += 1
        else:
            threeone += 1
    return sweep, threeone, threetwo


def sort7225(player):
    return player.get7525()

def sort7525mypoints(player):
    return .75 * float(player.trueSkill) + .25 * float(player.points)


def sort9010(player):
    return .90 * float(player.trueSkill) + .10 * float(player.braacket)


def linkSetsToPlayers(players, names, sets):
    for SET in sets:
        if (not (names.__contains__(SET.winner))):
            names.append(SET.winner)
            tempPlayer = Player(SET.winner)
            players.append(tempPlayer)
        if (not (names.__contains__(SET.loser))):
            names.append(SET.loser)
            tempPlayer = Player(SET.loser)
            players.append(tempPlayer)
        index = names.index(SET.winner)
        players[index].addWin(SET)
        index = names.index(SET.loser)
        players[index].addLoss(SET)


def scrapeRanking(trueskill, pathname):
    url = trueskill + "?rows=200"
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    players = []
    scores = []
    count = 0
    e = soup.find_all('td', class_='ellipsis')
    size = len(e)
    for row in e:
        if (count > 7 and count != size - 1):
            row = removeWhiteSpace(row.getText())
            if count == 94:
                print(row)
            length = len(row)
            if row[length - 1] == ' ':
                row = row[:-1]

            print (count - 7, row)
            players.append(row)
        count += 1
    e = soup.find_all('td', class_='min text-right')
    for row in e:
        #print(row.getText())
        scores.append(row.getText())
    titleFields = ["Rank", "Tag", "Points"]

    with open(pathname, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        for i in range(0, len(players)):
            writer.writerow([i + 1, players[i], scores[i]])


def displayTournamentsAttendedInSpring2023():
    decider = SetDecider(7)

    sets = getAllSetsWith(decider)

    players = []
    names = []

    linkSetsToPlayers(players, names, sets)

    index = names.index("Failbot")
    person = players[index]
    person.displayTotalRecord()

    print(person.getSetCountWithPlayer("Vivian"))

    index2 = names.index("Vivian")
    person = players[index2]
    person.displayTotalRecord()

    print(person.getSetCountWithPlayer("Failbot"))
    print("Players:", len(players))

    # seasons = ["Spring 2023", "Fall 2022", "Summer 2022"]
    seasons = ["Spring 2023"]
    addAllPlacements("tournaments.csv", seasons, players, names)
    print("Players:", len(players), "Names", len(names))
    count = 0
    activepeople = []
    for p in players:
        if p.hasAttendedAtLeast(4):
            count += 1
            activepeople.append(p)

    print("Players with 4 tournaments:", count)

    activepeople.sort(key=attendanceSort)
    # activepeople.sort(key=setsPlayedSort)
    for p in activepeople:
        print(p.name, p.tournamentsAttended(), p.tournamentsAttended())


def scrapeTwoRankings():
    url1 = "https://braacket.com/league/MNUltNew/ranking/2775306D-E6AD-4A38-BEE2-63E6C7B20DBA"
    dir1 = "Rankings\\Spring 2023\\Trueskill.csv"
    scrapeRanking(url1, dir1)
    url2 = "https://braacket.com/league/MNUltNew/ranking/F67F7951-B28B-4E86-A12D-E878543BC5D7"
    dir2 = "Rankings\\Spring 2023\\Braacket.csv"

    time.sleep(2)
    scrapeRanking(url2, dir2)


def getQualifiedPlayers(trueskill, braacket, players, names):
    people1 = []
    score1 = []
    people2 = []
    score2 = []
    with open(trueskill, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        count = 0

        for row in reader:
            if count > 0:
                people1.append(row[1])
                score1.append(row[2])
            count += 1



    with open(braacket, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        count = 0

        for row in reader:
            if count > 0:
                people2.append(row[1])
                score2.append(row[2])
            count += 1


    print("Trueskill Length:", len(people1))
    print("Braacket Length:", len(people2))


    badInput = []
    for i in range (0, len(people1)):
        temp = people1[i]
        bool = people2.__contains__(temp)

        if (not bool):
            badInput.append(i)

    for i in reversed(badInput):
        del people1[i]
        del people2[i]

    badInput = []
    for i in range (0, len(people2)):
        if (not people1.__contains__(people2[i])):
            badInput.append(i)

    for i in reversed(badInput):
        del people2[i]
        del score2[i]


    print("Trueskill Length:", len(people1), "Score:", len(score1))
    print("Braacket Length:", len(people2), "Score:", len(score2))

    for i in range(0,len(people1)):
        tag = people1[i]
        if (not names.__contains__(tag)):
            names.append(tag)
            temp = Player(tag)
            players.append(temp)
        index = names.index(tag)
        players[index].setTrueSkill(score1[i])

    for i in range(0,len(people2)):
        tag = people2[i]
        if (not names.__contains__(tag)):
            names.append(tag)
            temp = Player(tag)
            players.append(temp)
        index = names.index(tag)
        players[index].setBraacket(score2[i])


def getAndCalculateStats():
    scrapeTwoRankings()
    players = []
    names = []
    getQualifiedPlayers("Rankings\\Spring 2023\\Trueskill.csv", "Rankings\\Spring 2023\\Braacket.csv", players, names)
    print("Names:", len(names), "Players:", len(players))
    players.sort(key=sort7225, reverse=True)
    with open("StatPR.csv", 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(["Rank", "Player", "Points", "Trueskill, Braacket"])
        count = 1
        for i in players:
            writer.writerow([count, i.name, sort7225(i), i.trueSkill, i.braacket])
            count += 1



def makeHead2Head(players, filename):

    arr = [str(i + 1) for i in range(0, len(players))]
    arr = ["#", ""] + arr
    for i in arr:
        print(i)

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(arr)
        arr = [p.name for p in players]
        arr = ['', ''] + arr + ["vs. Top 10", "vs. Top 20", "vs Field"]
        writer.writerow(arr)
        for i in range(0, len(players)):
            wins = 0
            loss = 0
            count = 0
            tenwin = 0
            tenloss = 0
            twentyloss = 0
            twentywin = 0
            for p in players:
                tempWins, tempLoses = players[i].getSetIntsWith(p.name)
                wins += tempWins
                loss += tempLoses
                count += 1
                if count == 10:
                    tenwin = wins
                    tenloss = loss
                if count == 20:
                    twentywin = wins
                    twentyloss = loss

            setTotal = str(len(players[i].setWins)) + " - " + str(len(players[i].setLoses))
            tenTotal = str(tenwin) + " - " + str(tenloss)
            twentyTotal = str(twentywin) + " - " + str(twentyloss)
            arr = [players[i].getSetCountWithPlayer(p.name) for p in players]
            arr = [str(i + 1), players[i].name] + arr
            arr = arr + [tenTotal, twentyTotal, setTotal]
            writer.writerow(arr)


def test9010():
    names = []
    players = []
    getQualifiedPlayers("Rankings\\Spring 2023\\Trueskill.csv", "Rankings\\Spring 2023\\Braacket.csv", players, names)
    index = names.index("GodIMissHer")
    del names[index]
    del players[index]
    currPr = []
    for i in players:
        currPr.append(i)
    currPr.sort(key=sort7225, reverse=True)

    players.sort(key=sort9010, reverse=True)
    count = 0

    print("#, Tag, Score, Tag, 75/25 Score")
    for i in range(0, len(players)):
        if (not players[i].name == "GodIMissHer"):
            print(count + 1, players[i].name, .90 * sort9010(players[i]), currPr[i].name, currPr[i].get7525())
            count += 1

    with open("TestWeight.csv", 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(["Rank", "Tag", "90/10 Split", "", "Tag", "75/25 Split (Current)"])
        for i in range(0, len(players)):
            writer.writerow([i + 1, players[i].name, sort9010(players[i]), "", currPr[i].name, sort7225(currPr[i])])


def makeSpring2023H2H():
    names = []
    players = []
    getQualifiedPlayers("Rankings\\Spring 2023\\Trueskill.csv", "Rankings\\Spring 2023\\Braacket.csv", players, names)

    decider = SetDecider(8)

    sets = getAllSetsWith(decider)

    linkSetsToPlayers(players, names, sets)

    players.sort(key=sort7225, reverse=True)

    for i in range(0, 20):
        print(i + 1, players[i].name, sort7225(players[i]))

    top20 = []
    for i in range(0, 21):
        top20.append(players[i])
    filename = "Top20HeadToHead.csv"
    makeHead2Head(top20, filename)


def showTrue7525():
    players = []
    playernames = []
    # seasons = ["Spring 2023", "Fall 2022", "Summer 2022"]
    seasons = ["Spring 2023"]
    getQualifiedPlayers("Rankings\\Spring 2023\\Trueskill.csv", "Rankings\\Spring 2023\\Braacket.csv", players,
                        playernames)
    addAllPlacements("tournaments.csv", seasons, players, playernames)

    players.sort(key=sort7525mypoints, reverse=True)
    active = []
    for p in players:
        if p.hasAttendedAtLeast(4):
            active.append(p)

    for i in range(0, len(active)):
        print(i + 1, active[i].name, sort7525mypoints(active[i]))


def showWinRate():
    decider = SetDecider(0)

    sets = getAllSetsWith(decider)

    players = []
    names = []

    linkSetsToPlayers(players, names, sets)

    index = names.index("Failbot")
    person = players[index]
    person.displayTotalRecord()

    print(person.getSetCountWithPlayer("Violet"))

    wins, losses = person.getSetsAgainst("Violet")

    for w in wins:
        w.displayAll()
    for l in losses:
        l.displayAll()

    index2 = names.index("Truth")
    person = players[index2]
    person.displayTotalRecord()

    print(person.getSetCountWithPlayer("Failbot"))
    print("Players:", len(players))

    seasons = ["Spring 2023", "Fall 2022", "Summer 2022"]
    addAllPlacements("tournaments.csv", seasons, players, names)

    count = 0
    activepeople = []
    for p in players:
        if p.hasAttendedAtLeast(4):
            count += 1
            activepeople.append(p)
    activepeople.sort(key=winrateSort, reverse=True)

    for i in range(0, len(activepeople)):
        print(str(i) + ':', activepeople[i].name, winrateSort(activepeople[i]) * 100)


def makeFullSpring2023H2H():
    names = []
    players = []
    getQualifiedPlayers("Rankings\\Spring 2023\\Trueskill.csv", "Rankings\\Spring 2023\\Braacket.csv", players, names)

    index = names.index("GodIMissHer")
    del names[index]
    del players[index]
    qualified = len(players)

    decider = SetDecider(8)

    sets = getAllSetsWith(decider)

    linkSetsToPlayers(players, names, sets)

    players.sort(key=sort7225, reverse=True)

    for i in range(0, 20):
        print(i + 1, players[i].name, sort7225(players[i]))

    topN = []
    for i in range(0, qualified):
        topN.append(players[i])

    filename = "FullHeadToHeadOutput.csv"
    makeHead2Head(topN, filename)


def makeSpringH2Hs():
    getAndCalculateStats()
    makeSpring2023H2H()
    makeFullSpring2023H2H()


def updateAndMakeSpring2023():
    scrapeLast200Placements()
    makeSpringH2Hs()






