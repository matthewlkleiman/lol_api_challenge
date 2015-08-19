"""
Riot API scraper
"""
import requests
import csv

# Currently all data is in here, but this isn't meant to be run as a __main__
api_key = {'api_key': 'INSERT_API_KEY'}
headers = ['champ', 'team', 'cs_diff_per_min_z_to_10', 'cs_diff_per_min_10_to_20', 'cs_diff_per_min_20_to_30',
           'cs_diff_per_min_30_to_e', 'role', 'lane', 'did_win', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5',
           'kills', 'deaths', 'assists', 'doubleKills', 'tripleKills', 'quadraKills', 'pentaKills', 'unrealKills',
           'total_heal', 'gold_earned', 'gold_spent', 'crowd_control_dealt_time']


def make_api_call(url, params_dict):
    rows = []
    r = requests.get(url, params=params_dict)
    if r.status_code == 200:
        game_json = r.json()
        for summoner in game_json['participants']:
            row = {'champ': str(summoner['championId']), 'team': str(summoner['teamId'])}
            try:
                cs_diff_per_min_keys = ['cs_diff_per_min_z_to_10', 'cs_diff_per_min_10_to_20',
                                        'cs_diff_per_min_20_to_30', 'cs_diff_per_min_30_to_e']
                cs_diff_per_min_values = summoner['timeline']['csDiffPerMinDeltas'].values()
                cs_diff_per_min_deltas = dict(zip(cs_diff_per_min_keys, cs_diff_per_min_values))
            except ValueError:
                print 'Failed to read stats'

            try:
                row['role'] = str(summoner['timeline']['role'])
                row['lane'] = str(summoner['timeline']['lane'])
            except ValueError:
                print 'Timeline not available'

            stats = summoner['stats']
            row['did_win'] = bool(stats['winner'])
            for i in xrange(6):
                try:
                    item_num = 'item' + str(i)
                    row[item_num] = stats[item_num]
                except IndexError:
                    print 'Item(s) not available'

            multi_kills = {'doubleKills': stats['doubleKills'], 'tripleKills': stats['tripleKills'],
                          'quadraKills': stats['quadraKills'], 'pentaKills': stats['pentaKills'],
                          'unrealKills': stats['unrealKills']}
            kda = {'kills': stats['kills'], 'deaths': stats['deaths'], 'assists': stats['assists']}
            row['total_heal'] = stats['totalHeal']
            gold = {'gold_earned': stats['goldEarned'], 'gold_spent': stats['goldSpent']}
            row['crowd_control_dealt_time'] = stats['totalTimeCrowdControlDealt']
            row.update(multi_kills)
            row.update(kda)
            row.update(gold)
            row.update(cs_diff_per_min_deltas)
            rows.append(row)
        return rows

# Run method
game_url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/1852548676'
game = make_api_call(game_url, api_key)

# Write output
with open('output/test.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
    csv_writer.writeheader()
    for player_row in game:
        if not set(player_row.keys()).issubset(headers):
            raise IndexError('Error: some values in row are\'nt in output headers')

    csv_writer.writerows(game)
