__author__ = 'mkleiman'
"""
File written to scrape data from riot's api
"""

import time
from math import floor

# Config
api_keys = ['4fc5d1d3-817b-4a0e-b86d-ad6436bb9391']

resource_folders = ['AP_ITEM_DATASET/5.11/NORMAL_5x5', 'AP_ITEM_DATASET/5.11/RANKED_SOLO',
                    'AP_ITEM_DATASET/5.14/NORMAL_5x5', 'AP_ITEM_DATASET/5.14/RANKED_SOLO']

output_folder = 'output'
output_name = 'game_info.csv'

RATE_LIMIT = floor(len(api_keys) * 500 / 600.0)

print RATE_LIMIT

request_counter = 0
if request_counter > RATE_LIMIT:
    time.sleep(1)