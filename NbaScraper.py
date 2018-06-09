import collections
import requests
from lxml import html, etree


class ScrapeNba:

    def __init__(self):
        pass

    def get_data(self, date):

        link = "http://scores.nbcsports.com/nba/scoreboard.asp?day="+date+"&meta=true"

        response = requests.get(link)
        sourceCode = response.content
        htmlElem = html.fromstring(sourceCode)

        scrape_teams = htmlElem.xpath("//table/tr/td[@class='shsNamD']/a")
        teams = [str(s.text_content()) for s in scrape_teams]

        valid_quarters = ['1', '2', '3', '4', 'Tot', 'OT', '2OT', '3OT', '4OT', '5OT', '6OT', '7OT']

        scrape_status_quarter = htmlElem.xpath("//table/tr[@class='shsTableTtlRow']/td")
        statuses, quarters = [], ['0']
        i = 0
        while i < len(scrape_status_quarter):
            if len(scrape_status_quarter[i].text_content()) > 15:
                x = "play at " + scrape_status_quarter[i].text_content()[:10]
                statuses.append(x)
                quarters += ['1', '2', '3', '4', 'Tot']
                i += 2
            else:
                x = scrape_status_quarter[i].text_content()
                if x not in valid_quarters:
                    statuses.append(x)
                if x in valid_quarters:
                    quarters.append(x)
                i += 1

        # get corresponding scores for teams

        scrape_scores = htmlElem.xpath("//table//tr[not(@*)]//td[@class='shsTotD']")
        scores = [str(s.text_content()) for s in scrape_scores]

        for i in range(len(scores)):
            if scores[i] == "\xa0":
                scores[i] = "N/A"

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

        all_games = [[] for _ in range(len(statuses))]

        ## add status
        for i in range(len(statuses)):
            all_games[i].append(statuses[i])

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
