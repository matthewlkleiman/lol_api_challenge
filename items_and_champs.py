from driver import game

__author__ = 'mkleiman'
import requests
import csv

api_key = {'api_key': 'YOUR_API_KEY'}

champs = [
    91
    , 69
    , 43
    , 107
    , 67
    , 31
    , 13
    , 412
    , 28
    , 222
    , 57
    , 245
    , 18
    , 117
    , 17
    , 236
    , 112
    , 59
    , 99
    , 150
    , 101
    , 40
    , 75
    , 22
    , 1
    , 58
    , 44
    , 429
    , 268
    , 36
    , 42
    , 62
    , 11
    , 27
    , 238
    , 10
    , 74
    , 16
    , 122
    , 131
    , 2
    , 33
    , 103
    , 29
    , 102
    , 25
    , 111
    , 133
    , 106
    , 80
    , 15
    , 421
    , 48
    , 154
    , 105
    , 89
    , 12
    , 92
    , 20
    , 21
    , 157
    , 84
    , 267
    , 64
    , 110
    , 55
    , 121
    , 104
    , 113
    , 53
    , 86
    , 76
    , 266
    , 39
    , 77
    , 41
    , 19
    , 63
    , 35
    , 432
    , 9
    , 45
    , 127
    , 56
    , 120
    , 79
    , 61
    , 37
    , 23
    , 54
    , 81
    , 60
    , 90
    , 83
    , 72
    , 7
    , 114
    , 68
    , 115
    , 201
    , 82
    , 8
    , 14
    , 254
    , 96
    , 24
    , 38
    , 161
    , 5
    , 26
    , 119
    , 32
    , 134
    , 4
    , 30
    , 34
    , 98
    , 3
    , 143
    , 50
    , 6
    , 85
    , 78
    , 223
    , 126
    , 51
]

with open('champ_table.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=['champ_id', 'name'])
    csv_writer.writeheader()
    for champ_id in champs:
        url = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(champ_id)
        try:
            r = requests.get(url, params=api_key)
        except requests.exceptions.ConnectionError:
            print 'request failed, champ_id:  ' + str(champ_id) + ' status code: ' + str(r.status_code)
        game_json = r.json()

        csv_writer.writerow({'champ_id': champ_id, 'name': str(game_json['name'])})
