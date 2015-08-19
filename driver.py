__author__ = 'mkleiman'
"""
File written to scrape data from riot's api
"""

import csv
import json
import sys
from time import sleep, strftime
from os import listdir
from os.path import isfile, join
from re import search
from lol_api_request import make_api_call

#
# Config
#
RATE_LIMIT = 6
SLEEP_TIMER = 15

# Change below line
api_key_list = ['INSERT_KEY']
num_apis = len(api_key_list)

# Choose 5.14 if your Ben
resource_folders = ['AP_ITEM_DATASET/5.11/NORMAL_5x5', 'AP_ITEM_DATASET/5.11/RANKED_SOLO']

output_file = 'output/game_info.csv'
headers = ['patch_num', 'game_mode', 'match_id', 'match_duration', 'champ', 'team', 'creep_per_min_z_to_10',
           'creep_per_min_10_to_20', 'creep_per_min_20_to_30', 'creep_per_min_30_to_e', 'role', 'lane', 'did_win',
           'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'kills', 'deaths', 'assists', 'doubleKills',
           'tripleKills', 'quadraKills', 'pentaKills', 'unrealKills', 'total_heal', 'gold_earned', 'gold_spent',
           'crowd_control_dealt_time']

input_files = []

# Get all json files to iterate through
for folder in resource_folders:
    files_in_folder = [f for f in listdir(folder) if isfile(join(folder, f))]
    for json_file in files_in_folder:
        if json_file == 'NA.json':
            input_files.append(folder + '/' + json_file)

# Create output
with open(output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
    csv_writer.writeheader()
    for input_file in input_files:
        print '[' + strftime('%H:%M:%S') + '] Reading Input file: ' + input_file
        # Read input
        with open(input_file, 'r') as g:
            server = search('\/(\w{2})\.', g.name).group(1).lower()
            patch_num = search('5.{3}', g.name).group(0)
            game_mode = search('\/([A-Z]+\w*)', g.name).group(1)

            decoded_json = json.load(g)
            request_count = 0

            # make api calls
            total_calls_made = 0
            print '[' + strftime('%H:%M:%S') + '] Began sending API requests'
            for game_id in decoded_json:
                game_url = 'https://' + server + '.api.pvp.net/api/lol/' + server + '/v2.2/match/' + str(game_id)
                sleep(1)
                game = make_api_call(game_url, {'api_key': api_key_list[total_calls_made % num_apis]})
                while game == 429:
                    print '[' + strftime('%H:%M:%S') + '] Error, api call failed. Total calls made: ' + str(
                        total_calls_made)
                    sleep(1)
                    game = make_api_call(game_url, {'api_key': api_key_list[total_calls_made % num_apis]})

                request_count += 1
                total_calls_made += 1

                if request_count == RATE_LIMIT:
                    sys.stdout.write(
                        '[' + strftime('%H:%M:%S') + '] Rate limit reached, now sleeping for ' + str(SLEEP_TIMER) + ' seconds...')
                    sleep(SLEEP_TIMER)
                    request_count = 0
                    print 'Resuming...(calls made: ' + str(total_calls_made) + ')'

                # write to output file
                for player_row in game:
                    player_row.update({'patch_num': patch_num, 'game_mode': game_mode})
                    if not set(player_row.keys()).issubset(headers):
                        raise IndexError('Error: some values in row are\'nt in output headers')
                csv_writer.writerows(game)
