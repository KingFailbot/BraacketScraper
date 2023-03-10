import csv
import time

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook

from Placing import Placing

from Player import Player


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


def removeifContains(word, target):
    delim = word.find(target)
    if delim != -1:
        word = word.replace(target, '')
    return word


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


def scrapeATournament(url, workBook):
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

    workBook.save('PR tournaments.xls')
    filename = tournamentName + '.csv'

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(titleFields)
        writer.writerow(fields)
        writer.writerow(fieldnames)
        for i in range(0, len(players)):
            writer.writerow([nums[i], players[i], alts[i]])
    return fields


def scrapeLast200Placements():
    links = scrapeLast200Tournaments()

    # url = "https://braacket.com/tournament/0158DF57-0695-4D2F-A111-8E67687BF8D9"

    # url = "https://braacket.com/tournament/233866E7-DAC3-420B-B08C-1C014FEB2206"
    wb = Workbook()

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

    titlesheet = wb.add_sheet("Tounrmanets")

    for i in range(0, len(titleFields)):
        titlesheet.write(0, i, titleFields[i])

    count = 0
    for i in reversed(links):
        time.sleep(2)
        attributes = scrapeATournament(i, wb)
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

    wb.save('PR tournaments.xls')

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



players = []
playernames = []
fileLocation = "Summer 2022/Inver Grove Fights #26.csv"

filenames = []
count = 0
# filenames = ["Summer 2022/Inver Grove Fights #26.csv", "Summer 2022/Inver Grove Fights #29.csv"]
with open("Spring 2023.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if count > 0:
            content = 'Spring 2023/' + row[0] + '.csv'
            filenames.append(content)
        count = count + 1


for name in filenames:
    players, playernames = calculateTournamentPoints(name, players, playernames)
players.sort(reverse=True)
count = 0


for p in players:
    if(p.tournamentsAttended() >= 4):
        p.printOneLine()
        count = count + 1

