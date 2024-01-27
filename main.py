from min_char_rnn import RNN
from genius_client import GeniusClient
from training_data import TrainingData

import argparse
import logging
import os
import time


logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artist', type=str, required=True)
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--iters', type=int, default=10000)

    args = parser.parse_args()
    artist: str = args.artist
    url: str = args.url
    iters: int = args.iters
    return artist, url, iters

if __name__ == "__main__":

    artist, url, iters = get_args()
    
    if f"lyrics\\{artist.lower()}" not in [x[0] for x in os.walk('lyrics')]:
        genius = GeniusClient(url, artist)
        logger.warning(f'crawling all {artist} lyrics from Genius.')
        genius.run()
    else:
        logger.warning(f'found existing data of {artist}.')

    time.sleep(2)
    data = TrainingData(f'lyrics/{artist}')

    logger.warning('training RNN model using crawled data.')

    rnn = RNN(
        data=data, 
        iters=iters)
    rnn.run()