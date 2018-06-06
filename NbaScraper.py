import collections
import requests
from lxml import html, etree


class ScrapeNba:

    def __init__(self):
        pass

    def get_data(self, date):

        #link = "http://scores.nbcsports.com/nba/scoreboard.asp?day="+date+"&meta=true"
        link = "http://scores.nbcsports.com/nba/scoreboard.asp?day=20180315&meta=true"

        response = requests.get(link)
        sourceCode = response.content
        htmlElem = html.fromstring(sourceCode)

        scrape_teams = htmlElem.xpath("//table/tr/td[@class='shsNamD']/a")
        teams = [str(s.text_content()) for s in scrape_teams]

        scrape_status = htmlElem.xpath("//table/tr[@class='shsTableTtlRow']//td[@class='shsTeamCol shsNamD']")
        status = [str(s.text_content()) for s in scrape_status]

        scrape_quarters = htmlElem.xpath("//table/tr[@class='shsTableTtlRow']//td[@class='shsTotD']")
        quarters = ['0'] + [str(s.text_content()) for s in scrape_quarters]

        # get corresponding scores for teams

        scrape_scores = htmlElem.xpath("//table//tr[not(@*)]//td[@class='shsTotD']")
        scores = [str(s.text_content()) for s in scrape_scores]

        for i in range(len(scores)):
            if scores[i] == "\xa0":
                scores[i] = "Game has not started yet"

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

        team_scores = []
        for i in range(len(teams)):
            team_score = teams[i] + " : " + str(tot_scores[i])
            team_scores.append(team_score)

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

        return game_d
