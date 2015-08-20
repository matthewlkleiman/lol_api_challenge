"""
Riot API scraper
"""
import requests


def make_api_call(url, params_dict):
    rows = []
    try:
        r = requests.get(url, params=params_dict)
        if r.status_code == 200:
            game_json = r.json()
            for summoner in game_json['participants']:
                row = {'champ': str(summoner['championId']), 'team': str(summoner['teamId']),
                       'match_id': str(game_json['matchId']), 'match_duration': str(game_json['matchDuration'])}
                try:
                    creep_per_min_keys = ['creep_per_min_z_to_10', 'creep_per_min_10_to_20', 'creep_per_min_20_to_30',
                                          'creep_per_min_30_to_e']
                    creep_per_min_values = summoner['timeline']['creepsPerMinDeltas'].values()
                    creep_per_min_deltas = dict(zip(creep_per_min_keys, creep_per_min_values))
                except ValueError:
                    print 'Failed to read stats'
                except KeyError:
                    creep_per_min_deltas = {}
                    print 'Failed reading creep info for summoner ' + str(
                        summoner['participantId']) + ' in match: ' + str(game_json['matchId'])

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
                row.update(creep_per_min_deltas)
                rows.append(row)
                r.close()
        else:
            r.close()
            print 'Bad request code: ' + str(r.status_code)
            print url
    except requests.exceptions.ConnectionError:
        print 'Connection to ' + url + ' failed'
    return r.status_code, rows
