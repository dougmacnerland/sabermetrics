import mlbgame
from lxml import html
import stats

def pitcher_response_dist(current_team, player):
    """
    takes the player name as a string and returns a distribution of hits vs pitching difficulty
    :return a matrix corresponding to the hits:
    """

    mlbteam_info = mlbgame.info.team_info()

    player_table = stats.br_table(current_team, player)
    major_years = player_table.xpath('//table/tbody/tr[@class="full"]')

    player_distribution = []

    for year in major_years:
        yr = int(year.xpath('./th')[0].text)
        br_team_name = year.xpath('./td[@data-stat="team_ID"]/a[@title]')[0].attrib['title']
        mlb_team_name = ''
        for team in mlbteam_info:
            #mlbteam_info is an alphabetical list
            if team['club_full_name'] == br_team_name:
                mlb_team_name = team['club_common_name']

        #take note, mlbgame uses the common names
        games = mlbgame.games(yr, home=mlb_team_name, away=mlb_team_name)
        #now just to search through all of the mlb games to find events in which this layer participates
        for day in games:
            for game in day:
                print game



if __name__ == "__main__":
    pitcher_response_dist("ARI", "Nick Ahmed")