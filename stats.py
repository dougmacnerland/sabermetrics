from lxml import html
import requests
import mlbgame
import ast
import os.path

mlb_endpoint = 'http://m.mlb.com/lookup/json/named.psc_leader_hit_hr_dist.bam'
br_url = 'http://www.baseball-reference.com'

js_player_class = 'player_list'

cached_pages = {}
player_urls = {}

def get_page(url):
    if url not in cached_pages:
        r = requests.get(url)
        cached_pages[url] = r.text
    return cached_pages[url]

def fetch_player_lookup_json():
    """
    the urls are in reference to baseball-reference.com
    :return player_json: json that contains the urls correspending to each player
    """

    if os.path.isfile('./player.json'):
        g = open('player.json', 'r')
        p_dict = ast.literal_eval(g.read())
        return p_dict

    br_homepage = requests.get(br_url)
    br_elements = html.fromstring(br_homepage.text)
    player_script = br_elements.xpath('//div[@id="players"]/script')[0].text

    #beginning = start of the json declaration + declaration offset
    beginning = player_script.index('sr_goto_json["player_json"]') + 30
    end = player_script.index(';', beginning)
    player_json = ast.literal_eval(player_script[beginning:end])

    #the json is structured poorly for data lookup and has empty keys
    #so convert it into a python structure
    player_dict = {}
    for team in player_json:
        player_dict[team] = {}
        for entry in player_json[team]:
            for url in entry:
                if url != '':
                    player = entry[url]
                    player_dict[team][player] = url

    f = open('player.json', 'w')
    f.write(str(player_dict))

    return player_dict

def br_table(player_team, player_name):
    urls = fetch_player_lookup_json()
    stat_url = br_url + urls[player_team][player_name]

    r = requests.get(stat_url)
    br_etree = html.fromstring(r.text)

    return br_etree.xpath('//table[@id="batting_standard"]')[0]

def parse_events(ig):
    ge = mlbgame.game_events(ig)
    for i in ge:
        for j in ge[i]:
            for k in ge[i][j]:
                print k

if __name__ == '__main__':
    print 'running stats... '