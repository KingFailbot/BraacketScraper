import csv
import time

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook

from Placing import Placing

from Player import Player

from set import Set
from set import SetDecider

from SeasonFinder import SeasonFinder

"""A function that returns the given filename in the output directory.

:param filename, the file name desired within inputs
:returns A filename withing the output directory 
"""


def addOutputDirToStart(filename):
    outputDirectory = "Output"
    return outputDirectory + "\\" + filename


"""A function that scrapes the last 200 links from braacket.com.

A spreadsheet containing basic information is created from the last 200 tournaments on braacket.com. 

:returns an array containing all of the links of the first 200 tournaments.
"""


def scrapeLast200TournamentLinks():
    r = requests.get(
        'https://braacket.com/league/MNUltNew/tournament?rows=200')  # the page containing the last 200 tournaments
    # is requested.
    bracketURL = "https://braacket.com"
    print(r)

    # empty arrays for relevant variables are created (links, tournaments, entrants, dates, and match number.)
    links = []
    tournaments = []
    entrantCounts = []
    dates = []
    matches = []
    # print(len(entrantCounts))
    soup = BeautifulSoup(r.content, 'html.parser')

    count = 0
    trueCount = 0
    for link in soup.find_all('a'):  # find all the links in the page
        text = link.get('href')
        delimiter = -1
        if text is not None:  # if there is a link
            delimiter = text.find("/tournament/")
        if delimiter != -1:  # if the link is for a tournament
            if count % 2 != 1:  # every other link is a repeat, so ignore half
                text = bracketURL + text  # have to add the original URL since braacket does not give absolute url
                links.append(text)
                # print(text)
                trueCount = trueCount + 1
            count = count + 1

    s = soup.find_all('div', class_='my-dashboard-values-sub')

    for line in s:  # find all the dates for tournaments
        text = line.getText()
        date = text.find('Date')
        if (date != -1) & (text is not None):
            text = text.replace('\n', '')
            text = text.split('Date', 1)[1]  # splitting by the text date gives us information before and after,
            # only concerned with after
            dates.append(text)

    s = soup.find_all('td', class_='ellipsis')

    # tournament name grabber
    for line in s:
        line.get('href')
        text = line.getText()
        delimiter = text.find("\n")
        if (delimiter != -1) & (text is not None):
            text = text.replace("\n", "")
            tournaments.append(text)

    s = soup.find_all('span', class_='text-bold')

    for line in s:  # entrant counts for tournaments
        text = line.getText()
        leftParen = text.find('(')
        if (leftParen != -1) & (text is not None):
            text = text.split('(', 1)[1]
            text = text.split(')', 1)[0]  # only concerned with information between parenthesis
            entrantCounts.append(text)

    s = soup.find_all('div', class_='my-dashboard-values-sub')

    count = 0
    for line in s:
        text = line.getText()
        date = text.find('Matches')
        if (date != -1) & (text is not None):
            if count % 2 == 0:  # only concerned with ever other entry
                text = text.split('Matches', 1)[1]  # some parsing to get the number of sets played
                text = text.replace('\n', '')
                text = text.split("/", 1)[1]
                text = text.replace("\t", '')

                # print(text)
                matches.append(text)
            count += 1

    # print("Matches Count: ", trueCount)

    print(" \n ArraySize for Tournaments", len(tournaments))
    print('ArraySize for Dates', len(dates))
    print("ArraySize for Entrants", len(entrantCounts))
    print("ArraySize for Links", len(links))

    areEqual = len(tournaments) == len(entrantCounts)
    areEqual = areEqual & (len(tournaments) == len(links))
    if areEqual:  # if all the fields have the same number of entries
        with open(addOutputDirToStart('Last200Tournaments.csv'), 'w', newline='') as new_file:

            pairs = []
            # zip items for easier use later
            for t, d, e, m, l in zip(tournaments, dates, entrantCounts, matches, links):
                item = {'Tournament': t, 'Date': d, 'Entrants': e, 'Matches': m, "Link": l}
                pairs.append(item)

            fieldnames = ['Tournament', 'Date', 'Entrants', 'Matches', 'Link']

            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')

            csv_writer.writeheader()
            for row in pairs:  # write every zipped pair
                csv_writer.writerow(row)
    return links  # returns the array of tournament links


"""Utility function that removes instances of the target in the original word

:returns the reduced string
"""


def removeIfContains(word, target):
    delimiter = word.find(target)
    if delimiter != -1:
        word = word.replace(target, '')
    return word


"""Utility function that returns the season name.

Uses the SeasonFinder to return the season name (i.e. "Summer 2022")

:param date, a date of a tournament

:returns a string of the season name
"""


def getSeasonName(date):
    finder = SeasonFinder([1])
    return finder.getSeasonName(date)


"""Utility function that removes illegal characters for a file name

:param word a string that could have bad characters

:returns a clean version of word without any bad characters
"""


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


"""Utility function that takes a name, and replaces it with the "official tag" where possible

:param word the alternate tag to be replaced
:param players the list of players from the tournament
:param alts the list of alts from the tournament

:returns the players "official tag" if alts and players are the same size
"""


def replaceAltWithPlayer(word, players, alts):
    index = alts.index(word)

    if index < len(players):  # true if alts and players are the same size
        return players[index]  # returns the player in the position of the given alt
    else:
        return word


"""Utility function that takes a word, and returns a string within the given bounds

:param word, the word to be shortened
:param start, the start of the desired substring
:param end, the end of the desired substring

:returns the substring within start and end
"""


def cutString(word, start, end):
    contains = word.find(start)
    if contains != -1:  # cut the string if start is present
        word = word.split(start)[1]
    contains = word.find(end)
    if contains != -1:  # cut the string if end is present
        word = word.split(end)[0]
    return word


"""Utility function that removes white space from a string 

Removes end-line, tab, and "NBSP" from a string 

:param word the word to be remove white space from

:returns the word without whitespace
"""


def removeWhiteSpace(word):
    word = removeIfContains(word, '\n')
    word = removeIfContains(word, "\t")
    word = removeIfContains(word, " ")
    return word


"""Scraping function that gets information from the landing page of a tournament.

:param url, the url of the tournament landing page

:returns the page header information, including the name, date, entrants, and the original link
"""


def getHeader(url):
    # get the tournament page data
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('a', class_='text-bold')  # the tournament name is the only thing under this category
    tournamentName = s.getText()
    tournamentName = cleanString(tournamentName)
    print(tournamentName)

    s = soup.find_all('div', class_='btn btn-default')  # splits the information contained in the header
    date = s[1].getText()
    entrants = s[2].getText()
    sets = s[3].getText()

    date = removeWhiteSpace(date)

    entrants = removeWhiteSpace(entrants)  # the entrant count of the tournament
    entrants = cutString(entrants, '/', 'NA')

    sets = removeWhiteSpace(sets)  # the number of sets played
    sets = cutString(sets, '/', 'NA')

    s = soup.find('div', class_="my-dashboard-text text-left read-more-target info-read-more")
    s = s.find('a')
    link = s.get('href')  # the start.gg/challonge link for the tournament

    return tournamentName, date, entrants, sets, link


"""scraping function that gets every player and alternate tag seen on placement page.

:param url the url for the placements page

:returns parallel lists of player tags, and alts used
"""


def getPlayersAndAlts(url):
    players = []
    alts = []
    r = requests.get(url)  # get the URL
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')

    for alt in soup.find_all('td', class_='ellipsis'):  # get all player alts
        alt = alt.getText()
        alt = removeWhiteSpace(alt)
        alts.append(alt)

    for player in soup.find_all('span', class_='hidden-xs'):
        player = player.getText()
        if player.find("  ") != -1:  # these characters precede every player tag
            players.append(removeWhiteSpace(player))  # remove these characters

    return players, alts


"""Utility function, returns the largest power of 2 smaller than the number.

:param number the number that a power of 2 is being in relation to

:returns n the largest exponent such that 2^n < number
"""


def getDoubleEliminationN(number):
    n = 1
    while number > pow(2, n + 1):
        n = n + 1
    return n


"""Utility function that takes a number and turns it into a valid double elimination placement.

i.e. 47 --> 33, 49 --> 48. If a placement list is ordered it can take the position in list an convert to placement

:param number the number to be converted

:returns the valid double elimination placement
"""


def getDoubleEliminationPlacement(number):
    if number < 5:
        return number
    n = getDoubleEliminationN(number)
    if number > (pow(2, n) + pow(2, (n - 1))):
        return (pow(2, n) + pow(2, (n - 1))) + 1
    return pow(2, n) + 1


"""Scraping function, takes a tournament URL.

Writes a csv file and a workbook sheet for both the placement and headToHead data

:param url the landing URL to be scraped from

:param workBook, the placement workBook to be written to

:param placementFile the file location of the workBook

:param headToHeadWB, the headToHeadWB to be written to

:param headToHeadFile the file location for headToHead

:returns the fields like name, date, entrants, sets, links, and winner; this is used in 
 a spreadsheet with all tournaments information
"""


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

    # gets and prints relevant information about bracket
    tournamentName, date, entrants, sets, link = getHeader(url)
    print("Date:", date)
    print("Entrants:", entrants)
    print("Sets:", sets)
    print("ogLink:", link)
    print("braacket link:", url)
    time.sleep(2)

    # gets the placement page
    rankingURL = url + "/ranking?rows=200"
    players, alts = getPlayersAndAlts(rankingURL)  # alts are created in parallel with players (since they are
    # parallel lists on braacket)

    count = 1
    nums = []
    for _ in players:
        nums.append(getDoubleEliminationPlacement(count))  # adds as many placement data points as players
        count = count + 1
    first = players[0]  # gets first place, since that goes in spreadsheet
    print('First:', first)

    # One line of header fields labels, then a line with those fields
    titleFields = ['Tournament Name', 'Date', 'Winner', 'Entrants', 'Sets Played', 'Original Link:', 'League Link']
    fields = [tournamentName, date, first, entrants, sets, link, url]
    fieldnames = ['Placement', 'Tag', 'Alt']

    # gets a sheet name less than 30 characters for xls file
    sheetName = tournamentName
    stringLength = len(sheetName)
    if stringLength > 30:
        sheetName = sheetName[:30]

    # writes header information to xls file
    sheet = workBook.add_sheet(sheetName)
    for i in range(0, len(titleFields)):
        sheet.write(0, i, titleFields[i])
        sheet.write(1, i, fields[i])

    # writes the content of placements to xls file
    for i in range(0, len(fieldnames)):
        sheet.write(2, i, fieldnames[i])
    for i in range(0, len(nums)):
        sheet.write(3 + i, 0, nums[i])
        sheet.write(3 + i, 1, players[i])
        sheet.write(3 + i, 2, alts[i])

    # saves the workBook
    workBook.save(placementFile)

    # writes the placement data to a csv file
    path = "Placements/" + getSeasonName(date) + "/" + tournamentName + ".csv"
    with open(path, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        writer.writerow(fields)
        writer.writerow(fieldnames)
        for i in range(0, len(players)):
            writer.writerow([nums[i], players[i], alts[i]])

    time.sleep(2)  # wait for 2 seconds
    getOneHeadToHead(url, titleFields, fields, headToHeadWB, headToHeadFile, players, alts)
    # gets and outputs the headToHead information for the tournament
    return fields  # returns the fields, these are used above


"""Scraping function that iterates through the last 200 tournaments.

Creates .xls and .csv files representing all tournaments for both head to head and placement data
"""


def scrapeLast200PlacesAndSetRecords():
    links = scrapeLast200TournamentLinks()  # gets all the links to be scraped

    placementWB = Workbook()  # create worksheets and file locations for .xls files
    placementFile = addOutputDirToStart('PR tournaments.xls')
    headToHeadWB = Workbook()
    headToHeadFile = addOutputDirToStart('HeadToHead.xls')

    time.sleep(2)

    # setting up empty arrays to be filled with data from every tournament
    titleFields = ['Tournament Name', 'Date', 'Winner', 'Entrants', 'Sets Played', 'Original Link:', 'League Link']
    names = []
    dates = []
    winners = []
    entrants = []
    sets = []
    originalLink = []
    leagueLink = []

    titleSheet = placementWB.add_sheet("Tournaments")

    for i in range(0, len(titleFields)):  # writes title fields for .xls file
        titleSheet.write(0, i, titleFields[i])

    count = 0
    for i in reversed(links):
        time.sleep(2)
        attributes = scrapeATournament(i, placementWB, placementFile, headToHeadWB, headToHeadFile)
        # scrapes through every link in the array

        # adds respective data for each attribute
        names.append(attributes[0])
        dates.append(attributes[1])
        winners.append(attributes[2])
        entrants.append(attributes[3])
        sets.append(attributes[4])
        originalLink.append(attributes[5])
        leagueLink.append((attributes[6]))
        for j in range(0, len(attributes)):
            titleSheet.write(count + 1, j, attributes[j])
        count = count + 1

    # saves data in .xls files
    placementWB.save(placementFile)
    headToHeadWB.save(headToHeadFile)

    # writes a spreadsheet with all of the above data
    with open(addOutputDirToStart("tournaments.csv"), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        for i in range(0, len(names)):
            writer.writerow([names[i], dates[i], winners[i], entrants[i], sets[i], originalLink[i], leagueLink[i]])


"""Takes a tournament and adds all placements to respective players.

Uses parallel players and playerNames arrays

:param fileLocation the location of the placement data

:param players the list of player objects

:param playerNames the list of player name strings

:returns the players and playerNames with potentially new players added
"""


def calculateTournamentPoints(fileLocation, players, playerNames):
    # sets up empty variables for later
    tournamentName = ''
    entrants = 0
    date = ''

    with open(fileLocation, 'r', encoding='utf-8') as file:  # opens the data file
        reader = csv.reader(file)
        count = 0

        for row in reader:
            if count == 1:  # on the second line, get information from header
                header = row[0].split("\t")
                tournamentName = header[0]
                date = header[1]
                entrants = int(header[3])

            if count > 2:
                info = row[0].split("\t")
                placement = int(info[0])
                tag = info[1]
                # print("Line:", count + 1)
                # print(row[0])
                if len(info) > 2:  # safety check, should always be true
                    alt = info[2]
                else:  # if no valid information for alt, use the player's tag
                    alt = info[1]

                result = Placing(tournamentName, date, entrants, placement)  # add a placing with needed information
                # to player
                if not playerNames.__contains__(tag):  # if the player isn't in arrays (first time being encountered)
                    playerNames.append(tag)
                    thisPlayer = Player(tag)
                    thisPlayer.addPlacement(result, alt)

                    players.append(thisPlayer)  # adds player with placement to players array
                else:
                    index = playerNames.index(tag)  # find tag information in parallel array
                    thisPlayer = players[index]
                    thisPlayer.addPlacement(result, alt)  # add placement to player
                    players[index] = thisPlayer

            count = count + 1
    return players, playerNames  # returns the players arrays


"""Loops through all tournaments that meet a condition and adds placement data.

Takes a parallel players and playerNames array

:param file, the file that contains all locations of tournaments

:param cond, a SeasonFinder object with desired parameters

:param players, a list of players

:param playerNames, a list of player's tags (strings)
"""


def addAllPlacements(file, cond, players, playerNames):
    with open(file, 'r', encoding='utf-8') as file:  # open the spreadsheet with all tournament data
        reader = csv.reader(file, delimiter='\t')
        count = 0
        tournaments = []
        dates = []
        for row in reader:
            if count > 0:
                print(row[1])
                print(cond.inWhichSeason(row[1]))
                # print(cond.isInSeason(row[1]))
                if cond.isInSeason(row[1]):  # if the tournament follows condition, add it to list to be read
                    tournaments.append(row[0])
                    dates.append(row[1])
            count += 1
    count = 0

    for bracket in tournaments:  # for every valid tournament add its placement data
        link = "Placements\\" + getSeasonName(dates[count]) + "\\" + bracket + ".csv"  # gives correct file location
        calculateTournamentPoints(link, players, playerNames)  # adds placement data for tournament
        count += 1


"""Creates a spreadsheet with every known alternate tag

"""


def writeAllAlts():
    players = []
    playerNames = []
    seasons = SeasonFinder([1, 2, 3, 4, 5])
    # add all placement data, the alternate tags are a bonus
    addAllPlacements(addOutputDirToStart("tournaments.csv"), seasons, players, playerNames)

    # sort players so more relevant players appear higher
    players.sort(reverse=True)
    count = 0

    for p in players:  # prints all known alternate tags
        if p.tournamentsAttended() >= 1:  # if the player has attended a tournament (safety feature)
            print(p.name)
            p.printAlts()
            print()

            count = count + 1

    with open(addOutputDirToStart("alts.csv"), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(["Player: ", "Alts"])
        for i in players:
            row = [a for a in i.alts]  # for every alt the player has
            row = [i.name] + row  # adds the players name first
            writer.writerow(row)


"""scraping function for a specific headToHead page

:param url, the url of the tournament splash page

:param titleFields, the fields to be written at the top of the spreadsheet

:param fields, the fields from the tournament to write

:param headToHeadWB, the xls file to write sets to

:param headToHeadFile, the xls file location

:param players, the list of players for the tournament

:param alts, the parallel list of alternate tags for the tournament 
"""


def getOneHeadToHead(url, titleFields, fields, headToHeadWB, headToHeadFile, players, alts):
    url = url + '/match'
    print(url)
    r = requests.get(url)  # request the URL/page info
    print(r)

    soup = BeautifulSoup(r.content, 'html.parser')
    Sets = []
    URLs = []

    # some filtering to get all links for stages of the tournament
    for link in soup.find_all('a'):
        text = link.get('href')
        delimiter = -1
        if text is not None:
            delimiter = text.find("/stage/")
        if delimiter != -1:
            text = "https://braacket.com" + text
            text = removeIfContains(text, '?')
            print(text)
            URLs.append(text)

    if len(URLs) == 1:  # if there is more than one URL, it is a multiphase tournament
        severalURLs = False
    else:
        severalURLs = True

    if not severalURLs:  # if there is only one phase, standard logic applies
        scrapeOneH2HPage(url, Sets, players, alts, soup, severalURLs)
        row3 = ['Set Num', 'Winner', 'Loser', 'WS', 'LS', 'Best of', 'Game']
    else:  # if there are seperate URLs, then note that in the spreadsheet
        print("MULTIPLE PHASES:")
        row3 = ['Set Num', 'Winner', 'Loser', 'WS', 'LS', 'Best of', 'Game', '**MULTIPLE BRACKET PHASES**']
        for phase in URLs:  # scrape every phase
            scrapeOneH2HPage(phase, Sets, players, alts, soup, severalURLs)
    Sets = sorted(Sets)

    date = fields[1]
    season = getSeasonName(date)  # get the season name for the directory
    tournamentName = fields[0]

    path = "HeadToHead/" + season + "/" + tournamentName + ".csv"

    with open(path, 'w', newline='', encoding="utf-8") as csvfile:  # write every set for this tournament
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        writer.writerow(fields)
        writer.writerow(row3)
        for i in Sets:
            writer.writerow([i.order, i.winner, i.loser, i.winningScore, i.losingScore, i.outOf, i.game])

    # get an under 30 character sheet name
    sheetName = tournamentName
    stringLength = len(sheetName)
    if stringLength > 30:
        sheetName = sheetName[:30]

    sheet = headToHeadWB.add_sheet(sheetName)
    for i in range(0, len(titleFields)):
        sheet.write(0, i, titleFields[i])
        sheet.write(1, i, fields[i])
    # write the 3rd header line
    for i in range(0, len(row3)):
        sheet.write(2, i, row3[i])

    # write every set on a line
    for i in range(0, len(Sets)):
        sheet.write(3 + i, 0, Sets[i].order)
        sheet.write(3 + i, 1, Sets[i].winner)
        sheet.write(3 + i, 2, Sets[i].loser)
        sheet.write(3 + i, 3, Sets[i].winningScore)
        sheet.write(3 + i, 4, Sets[i].losingScore)
        sheet.write(3 + i, 5, Sets[i].outOf)
        sheet.write(3 + i, 6, Sets[i].game)
    headToHeadWB.save(headToHeadFile)


"""scrapes one headToHead Phase

if there is more than one head to head phase, it waits to call a scrape. Takes a parallel list of players and alts

:param url the url of the phase, only used if multiple phase

:param sets, the list of sets so far (empty unless a multiphase tournament)

:param players the list of players

:param alts, the list of alts

:param soup, the web scraping object to be used, used unless the tournament is multiphase

:param multiple, boolean value for if there are multiple phases
"""


def scrapeOneH2HPage(url, sets, players, alts, soup, multiple):
    if multiple:  # if there are multiple phases, create a new soup object
        time.sleep(2)
        r = requests.get(url)
        print(r)
        soup = BeautifulSoup(r.content, 'html.parser')
    # thisSet up empty lists to be filled with data
    winners = []
    losers = []
    winScore = []
    loseScore = []
    order = []

    # used to check if there are the same number of players and alts
    len1 = len(players)
    len2 = len(alts)

    if len1 > len2:  # bad things happen if this is the case, this means there is a mistake on the braacket page
        for i in range(0, len2):
            print(players[i], alts[i])
        print(players[len1 - 1])
        print("NOT EQUAL!!!")

    elif len2 > len1:  # bad things happen if this is the case, this means there is a mistake on the braacket page
        for i in range(0, len1):
            print(players[i], alts[i])
        print(alts[len2 - 1])
        print("NOT EQUAL!!!")
    else:  # this is good
        print("Equal")

    count = 0
    for item in soup.find_all('table', class_='tournament_encounter-row'):  # every thisSet on the webpage
        count = count + 1

        entries = item.getText().split("\n")
        # smallCount = 0
        goodData = []
        for j in entries:
            j = removeWhiteSpace(j)
            if j != '' and j != ' ':  # if j isn't empty
                goodData.append(j)

                # smallCount += 1
        if len(goodData) > 4:  # if there are enough elements to fill a full set
            if not ((int(goodData[2]) == -1) or (int(goodData[4]) == -1)):  # check for DQs, those sets do not count
                # and are denoted by a -1 score
                order.append(int(goodData[0]))  # add the sets number to order (this number is useful for ordering)
                if int(goodData[2]) > int(goodData[4]):  # if the first player won
                    # print("Winner:", goodData[1])
                    winners.append(replaceAltWithPlayer(goodData[1], players, alts))
                    winScore.append(int(goodData[2]))
                    # print("Loser:", goodData[3])
                    losers.append(replaceAltWithPlayer(goodData[3], players, alts))
                    loseScore.append(int(goodData[4]))
                else:  # the second player one
                    # print("Loser:", goodData[1])
                    losers.append(replaceAltWithPlayer(goodData[1], players, alts))
                    loseScore.append(int(goodData[2]))
                    # print("Winner:", goodData[3])
                    winners.append(replaceAltWithPlayer(goodData[3], players, alts))
                    winScore.append(int(goodData[4]))
    for i in range(0, len(winners)):  # for set winner, create a set and append it to the sets array
        thisSet = Set(winners[i], losers[i], winScore[i], loseScore[i], order[i])
        sets.append(thisSet)


"""A test function

Shows if the output of the getSeasonName function makes sense
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


"""Tests if one tournament can be scraped correctly

"""


def testScrapeOneTournament():
    wb = Workbook()
    url = "https://braacket.com/tournament/228979B6-A101-486A-AADE-73047E5F0025"
    placementFile = 'PR tournaments.xls'
    wb2 = Workbook()
    file = 'HeadToHead.xls'
    scrapeATournament(url, wb, placementFile, wb2, file)


"""Data collection function

gives a list of sets that follow a SetDecider condition

:param cond a SetDecider with a condition

:returns a list of all valid sets
"""


def getAllSetsWith(cond):
    # set up lists to be filled
    dates = []
    tournaments = []
    sets = []
    with open(addOutputDirToStart("tournaments.csv"), 'r', encoding='utf-8') as csvfile:  # open spreadsheet with all
        # tournaments
        reader = csv.reader(csvfile)
        count = 0

        for row in reader:  # gets dates and tournament names for all tournaments
            if count > 0:
                info = row[0].split('\t')
                tournaments.append(info[0])
                dates.append(info[1])
            count += 1

    for i in range(0, len(tournaments)):  # for every tournament get sets that follow the condition
        filename = "HeadToHead\\"
        filename = filename + getSeasonName(dates[i]) + '\\' + tournaments[i] + '.csv'
        getOneTournamentSetsWith(cond, sets, filename)
    return sets


"""goes through one tournament and finds valid sets

:param cond is a SetDecider that has the desired settings

:param sets, the list of sets

:param filename, the filename where the tournament is located
"""


def getOneTournamentSetsWith(cond, sets, filename):
    with open(filename, 'r', encoding='utf-8') as file:  # open the tournament sets file
        reader = csv.reader(file, delimiter='\t')
        count = 0
        for row in reader:
            if count == 1:  # get the date and tournament name from the header
                # tournamentName = row[0].split('\t')[0]
                tournamentName = row[0]
                date = row[1]

            if count > 2:  # for lines past the header
                if row[0] != '':
                    thisSet = Set(row[1], row[2], int(row[3]), int(row[4]), int(row[0]))  # add the data to the set
                    thisSet.addTournament(tournamentName)  # add the tournament to the set
                    thisSet.addDate(date)
                    if cond.decide(thisSet):  # if the set is in the criteria, then add it to the list
                        sets.append(thisSet)
            count = count + 1


"""A test function for the setDecider class.

"""


def setDeciderTester():
    print("Testing...")
    sets = []
    thisSet = Set("Loaf", "Lucky", 3, 2, 1)
    sets.append(thisSet)
    set2 = Set("Violet", "Meatflap", 2, 1, 1)
    sets.append(set2)
    set3 = Set("Ventura", "Big Will", 2, 0, 1)
    sets.append(set3)
    set4 = Set("Truth", "Big Will", 3, 0, 1)
    sets.append(set4)
    decider = SetDecider(1)

    if decider.decide(set3):
        print("TRUE")
    else:
        print("FALSE")
    for i in range(0, 5):
        decider.mode = i
        print("Round", i)
        for thisSet in sets:
            if decider.decide(thisSet):
                print("Set:", thisSet.winner, "Iter:", i)


"""Utility sorting key function that sorts players by their winRate.

"""


def winRateSort(player):
    return player.getWinPercent()


"""Utility sorting key function that sorts players by the number of tournaments they've attended

"""


def attendanceSort(player):
    return player.tournamentsAttended()


"""Utility sorting key function that sorts by attendance in the Spring 2023 season

"""


def spring2023AttendanceSort(player):
    finder = SeasonFinder([3])
    count = 0
    for place in player.results:
        if finder.isInSeason(place.date):
            count += 1
    return count


"""Utility sorting key function that sorts by attendance in the Fall 2022 season

"""


def fall2022AttendanceSort(player):
    finder = SeasonFinder([2])
    count = 0
    for place in player.results:
        if finder.isInSeason(place.date):
            count += 1
    return count


"""Utility sorting key function that sorts by attendance in the Summer 2022 season

"""


def summer2022AttendanceSort(player):
    finder = SeasonFinder([1])
    count = 0
    for place in player.results:
        if finder.isInSeason(place.date):
            count += 1
    return count


"""Utility sorting key function that sorts players by sets played

"""


def setsPlayedSort(player):
    return player.getTotalSets()


"""Utility function that gets the distribution of game counts of a list of sets

:param sets a list of sets

:return sweep, the number of sets where only one player won matches

:return threeOne, the number of sets that were 3-1

:return lastGame, the number of sets that went to the last possble game
"""


def getSetDistribution(sets):
    sweep = 0
    threeOne = 0
    lastGame = 0

    for thisSet in sets:
        if thisSet.losingScore == 0:  # if the losing score is zero
            sweep += 1
        elif thisSet.outOf == thisSet.game:  # if the game count and possible game count are equal
            lastGame += 1
        else:
            threeOne += 1
    return sweep, threeOne, lastGame


"""Utility sorting key function that sorts by a 75/25 average of Trueskill and Attendance

"""


def sort7225(player):
    return player.get7525()


"""Utility sorting key function that sorts by 75/25 average with new method for Attendance

"""


def sortCurrent7525(player):
    return .75 * float(player.trueSkill) + .25 * float(player.points)


"""Utility sorting key function that sorts by a 90/10 average

"""


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

            print(count - 7, row)
            players.append(row)
        count += 1
    e = soup.find_all('td', class_='min text-right')
    for row in e:
        # print(row.getText())
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
    addAllPlacements(addOutputDirToStart("tournaments.csv"), seasons, players, names)
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
    for i in range(0, len(people1)):
        temp = people1[i]
        bool = people2.__contains__(temp)

        if (not bool):
            badInput.append(i)

    for i in reversed(badInput):
        del people1[i]
        del people2[i]

    badInput = []
    for i in range(0, len(people2)):
        if (not people1.__contains__(people2[i])):
            badInput.append(i)

    for i in reversed(badInput):
        del people2[i]
        del score2[i]

    print("Trueskill Length:", len(people1), "Score:", len(score1))
    print("Braacket Length:", len(people2), "Score:", len(score2))

    for i in range(0, len(people1)):
        tag = people1[i]
        if (not names.__contains__(tag)):
            names.append(tag)
            temp = Player(tag)
            players.append(temp)
        index = names.index(tag)
        players[index].setTrueSkill(score1[i])

    for i in range(0, len(people2)):
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

    index = names.index("GodIMissHer")
    del names[index]
    del players[index]

    players.sort(key=sort7225, reverse=True)

    with open(addOutputDirToStart("StatPR.csv"), 'w', newline='', encoding="utf-8") as csvfile:
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

    with open(addOutputDirToStart(filename), 'w', newline='', encoding="utf-8") as csvfile:
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
    addAllPlacements(addOutputDirToStart("tournaments.csv"), seasons, players, playernames)

    players.sort(key=sortCurrent7525, reverse=True)
    active = []
    for p in players:
        if p.hasAttendedAtLeast(4):
            active.append(p)

    for i in range(0, len(active)):
        print(i + 1, active[i].name, sortCurrent7525(active[i]))


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
    addAllPlacements(addOutputDirToStart("tournaments.csv"), seasons, players, names)

    count = 0
    activepeople = []
    for p in players:
        if p.hasAttendedAtLeast(4):
            count += 1
            activepeople.append(p)
    activepeople.sort(key=winRateSort, reverse=True)

    for i in range(0, len(activepeople)):
        print(str(i) + ':', activepeople[i].name, winRateSort(activepeople[i]) * 100)


def makeFullSpring2023H2H():
    names = []
    players = []
    getQualifiedPlayers("Rankings\\Spring 2023\\Trueskill.csv", "Rankings\\Spring 2023\\Braacket.csv", players, names)

    """
    index = names.index("GodIMissHer")
    del names[index]
    del players[index]
    """
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
    scrapeLast200PlacesAndSetRecords()
    makeSpringH2Hs()


def testSeasonFinder():
    finder = SeasonFinder([1])
    dates = ["01 April 2022", "01 May 2022", "01 June 2022", "01 July 2022", "01 August 2022", "01 September 2022",
             "01 October 2022", "01 November 2022", "01 December 2022", "01 January 2023", "01 February 2023",
             "01 March 2023", "01 April 2023", "01 May 2023", "01 June 2023", "01 July 2023", "01 August 2023",
             "01 September 2023", "01 October 2023", "01 November 2023", "01 December 2023"]
    for date in dates:
        if finder.isInSeason(date):
            print(date + " is TRUE")
    print("\n\n\n")

    finder = SeasonFinder([2])
    for date in dates:
        if finder.isInSeason(date):
            print(date + " is TRUE")
    print("\n\n\n")

    finder = SeasonFinder([1, 2])
    for date in dates:
        if finder.isInSeason(date):
            print(date + " is TRUE")
    print("\n\n\n")

    finder = SeasonFinder([3])
    for date in dates:
        if finder.isInSeason(date):
            print(date + " is TRUE")
    print("\n\n\n")

    finder = SeasonFinder([1, 3])
    for date in dates:
        if finder.isInSeason(date):
            print(date + " is TRUE")
    print("\n\n\n")

    finder = SeasonFinder([4])
    for date in dates:
        if finder.isInSeason(date):
            print(date + " is TRUE")
    print("\n\n\n")

    finder = SeasonFinder([5])
    for date in dates:
        if finder.isInSeason(date):
            print(date + " is TRUE")
    print("\n\n\n")


def outputAttendance():
    players = []
    playernames = []

    seasons = ["Spring 2023", "Fall 2022", "Summer 2022"]
    # seasons = ["Spring 2023"]
    addAllPlacements(addOutputDirToStart("tournaments.csv"), seasons, players, playernames)

    activePlayers = []
    for p in players:
        if p.hasAttendedAtLeast(5):
            activePlayers.append(p)

    filename = "attendance.csv"
    activePlayers.sort(key=spring2023AttendanceSort, reverse=True)
    with open(addOutputDirToStart(filename), 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(["Player", "Spring 2023", "Fall 2022", "Summer 2022", "Total"])
        for p in activePlayers:
            writer.writerow(
                [p.name, spring2023AttendanceSort(p), fall2022AttendanceSort(p), summer2022AttendanceSort(p),
                 attendanceSort(p)])


def makeTrueSpring23StatPr():
    players = []
    names = []

    decider = SetDecider(8)

    sets = getAllSetsWith(decider)
    finder = SeasonFinder([3])

    linkSetsToPlayers(players, names, sets)
    print(len(players), len(names))
    addAllPlacements(addOutputDirToStart('tournaments.csv'), finder, players, names)

    getQualifiedPlayers("Rankings\\Spring 2023\\Trueskill.csv", "Rankings\\Spring 2023\\Braacket.csv", players, names)

    newPlayers = []
    for p in players:
        if p.hasAttendedAtLeast(4):
            newPlayers.append(p)

    newPlayers.sort(key=sortCurrent7525, reverse=True)

    with open(addOutputDirToStart("StatPRModified.csv"), 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(["Rank", "Player", "Points", "Trueskill", "Manual Placement", "Braacket"])
        count = 1
        for i in newPlayers:
            writer.writerow([count, i.name, sortCurrent7525(i), i.trueSkill, i.points, i.braacket])
            count += 1


scrapeLast200PlacesAndSetRecords()