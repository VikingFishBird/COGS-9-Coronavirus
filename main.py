import numpy as np
import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt

corona_totals = pd.read_csv('la_county_coronavirus_totals.csv')

most_recent_date = corona_totals.get('date').iloc[0]

corona_by_county = (
    corona_totals[corona_totals.get('date') == most_recent_date]
        .set_index('county')
        .get(['date', 'confirmed_cases', 'deaths'])
)

corona_by_county = corona_by_county.assign(
    mortality=corona_by_county.get('deaths') / corona_by_county.get('confirmed_cases')
)

print(corona_by_county.index)
for i in corona_by_county.index:
    print(i)
