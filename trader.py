from headline_to_symbol import headline_to_symbol
from datetime import datetime, time
from closest_lines import get_closest_line, format_lines
from plotter import plot, prepare_plots
from data_logger import log_data
from time import sleep
from EntityClass import EntityClass
import numpy as np
import pandas as pd


# readying entities
entities = headline_to_symbol()
ans = str(input("Add entity? (y/n)"))
while ans == 'y':
    symbol = str(input("Enter symbol:"))
    headline = str(input("Enter headline:"))
    entities.append(EntityClass(symbol, headline))
    ans = str(input("Add entity? (y/n)"))
prepare_plots(entities)
num_entities = len(entities)

# readying stored data
data_fil = 'PastTrades.h5'
data = pd.read_hdf(data_fil, key='date')  # data frame of past prices
format_lines(data)
print("Done- data load")

minutes = -1
clock = datetime.now()

while clock.time() < time(15, 30):
    clock = datetime.now()
    if clock.time() > time(9, 14):
        minutes += 1

        while datetime.now().second != 59:  # start at end of minute
            continue

        for entity in entities:
            entity.update_values()
            try:
                list_closest_lines = get_closest_line(entity.line)
                list_closest_lines.append(entity.line)
                plot(list_closest_lines, entity.id)

            except:
                pass

    else:
        print("waiting " + str(clock.time()))
    sleep(60)
log_data(entities)
