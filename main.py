
import csv
import requests
import time
from bs4 import BeautifulSoup

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
        if (text != None):
            delimiter = text.find("/tournament/")
        if (delimiter != -1):
            if (count % 2 != 1):
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
        if ((date != -1) & (text != None)):
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
        link = line.get('href')
        text = line.getText()
        delimiter = text.find("\n")
        if ((delimiter != -1) & (text != None)):
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
        if ((leftParen != -1) & (text != None)):
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
        if ((date != -1) & (text != None)):
            if (count % 2 == 0):
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
    if (areEqual):
        with open('Last200Tournaments.csv', 'w') as new_file:

            pairs = []
            for t, d, e, m, l in zip(tournaments, dates, entrantCounts, matches, links):
                item = {'Tournament': t, 'Date': d, 'Entrants': e, 'Matches': m, "Link": l}
                pairs.append(item)

            fieldnames = ['Tournament', 'Date', 'Entrants', 'Matches', 'Link']

            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')

            csv_writer.writeheader()
            for row in pairs:
                csv_writer.writerow(row)


def removeifContains(word, target):
    delim = word.find(target)
    if delim == -1 :
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
    if(contains != -1):
        word = word.split(start)[1]
    contains = word.find(end)
    if (contains != -1):
        word = word.split(end)[0]
    return word;

def removeWhiteSpace(word):
    word = removeifContains(word, '\n')
    word = removeifContains(word, "\t")
    return word

def getHeader(url):
    r = requests.get(url)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('a', class_='text-bold')
    tournamentName = s.getText()
    print(cleanString(tournamentName))
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



    return players, alts
def scrapeATournament(url):
    """
    Needed parameters
    tournamentName
    date
    firstPlace
    Entrants
    Sets played
    OG Bracket Link
    League Link



    tournamentName, date, entrants, sets, link = getHeader(url)
    print("Date:", date)
    print("Entrants:", entrants)
    print("Sets:", sets)
    print("ogLink:", link)
    print("braacket link:", url)
    time.sleep(2)


    """
    rankingURL = url + "/ranking"
    player, alts = getPlayersAndAlts(rankingURL)


# scrapeLast200Tournaments()

url = "https://braacket.com/tournament/0158DF57-0695-4D2F-A111-8E67687BF8D9"

scrapeATournament(url)
