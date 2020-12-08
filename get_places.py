import constants
import pandas as pd
import re

def extract_places_of_interest(tweet):
    ''' Método para identificar e classificar locais de ocorrência de eventos, seja ruas, avenidas, praças, etc. '''
    splitted_tweet = tweet.split()
    for place_type in constants.PLACE_TYPES:
        if place_type in tweet:
            place_name = []
            for name_part in splitted_tweet[splitted_tweet.index(place_type) + 1:]:
                if name_part[0].isupper() or name_part in constants.PREPOSITIONS:
                    place_name.append(name_part)
                    if name_part[-1] in [',', '.', ';']:
                        place_name.pop()
                        place_name.append(name_part[:-1])
                        break
                else:
                    break
            place_name = ' '.join(place_name)
            print(place_name)