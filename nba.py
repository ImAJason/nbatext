import collections
import re
import requests
from lxml import html, etree
from NbaAbbrevs import abbrevs

#view-source:http://scores.nbcsports.com/nba/scoreboard.asp?day=20180401&meta=true
link = "http://scores.nbcsports.com/nba/scoreboard.asp?day=20180606&meta=true"

response = requests.get(link)
sourceCode = response.content
htmlElem = html.fromstring(sourceCode)

"""scrape_teams = htmlElem.xpath("//table/tr/td[@class='shsNamD']/a")
teams = [s.text_content() for s in scrape_teams]

scrape_status = htmlElem.xpath("//table/tr[@class='shsTableTtlRow']//td[@class='shsTeamCol shsNamD']")
status = [s.text_content() for s in scrape_status]

scrape_quarters = htmlElem.xpath("//table/tr[@class='shsTableTtlRow']//td[@class='shsTotD']")
quarters = ['0'] + [s.text_content() for s in scrape_quarters]"""

# get corresponding scores for teams

scrape_scores = htmlElem.xpath("//table//tr[not(@*)]//td[@class='shsTotD']")
scores = [s.text_content() for s in scrape_scores]

for i in range(len(scores)):
    if scores[i] == "\xa0":
        scores[i] = "Game has not started yet"

print(scores)
"""
#quarters = ['0', '1', '2', '3', '4', 'OT', 'Tot', '1', '2', '3', '4', 'Tot', '1', '2', '3', '4', 'OT', 'Tot']
#scores = ['30', '26', '22', '29', '7', '114', '29', '27', '28', '23', '17', '124', '29', '27', '28', '23', '100',
#          '29', '27', '28', '23', '150', '30', '26', '22', '29', '7', '114', '29', '27', '28', '23', '17', '124']

total_indices = [i for i, x in enumerate(quarters) if x == "Tot" or x == 'tot']
tot_scores = []

current, prev = -1, 0
for tot_index in total_indices:
    diff = tot_index - prev
    current += diff
    tot_scores.append(scores[current])
    current += diff
    tot_scores.append(scores[current])
    prev = tot_index

#tot_scores = [scores[i] for i in total_indices]

team_scores = []
for i in range(len(teams)):
    team_score = teams[i] + " : " + str(tot_scores[i])
    team_scores.append(team_score)


#team_scores = ['Philadelphia : 119', 'Charlotte : 102', 'Washington : 94', 'Chicago : 113', 'Indiana : 111', 'LA Clippers : 104']

#all_games = [['Final', 'Philadelphia : 119', 'Charlotte : 102']]

all_games = [[] for _ in range(len(status))]

## add status
for i in range(len(status)):
    all_games[i].append(status[i])

## add teamscores

i, cnt = 0, 0
for ind_scores in team_scores:
    all_games[i].append(ind_scores)
    cnt += 1
    if cnt == 2:
        cnt = 0
        i += 1

## put all of it together into game_d

game_d = collections.defaultdict(list)

i, cnt = 0, 0
for team in teams:
    game_d[team] = all_games[i]
    cnt += 1
    if cnt == 2:
        cnt = 0
        i += 1

#game_d = {'Philadelphia': ["Final", "Philadelphia : 119", "Charlotte : 102"]}



in_msg = "phi"
in_msg = " ".join(in_msg.split()).replace(" ", "").lower()

d = {'Houston': ['hou', 'rockets', 'houstonrockets'], 'Philadelphia': ['philadelphia', 'phi', '76ers', 'philadelphia76ers']}

for i in d.keys():
    if in_msg in d[i]:
        print(game_d[i])"""


#status = ['Final', 'Final', '2nd Quarter']
#quarters = ['1', '2', '3', '4', 'tot', '1', '2', '3', '4', 'OT', 'tot']
#scores = [28, 32, 31, 28, 119, 29, 22, 27, 24, 102, 27, 32, 16, 19, 94, 36, 32, 19, 26, 113, 22, 28, 26, 35, 111, 30, 21, 27, 26, 104]
#teams = ['Philadelphia', 'Charlotte', 'Washington', 'Chicago', 'Indiana', 'LA Clippers']

#text = scriptElem.text_content()

#ingamescores = [['30', '26', '17', '\xa0', '73', '29', '27', '18', '\xa0', '74']
