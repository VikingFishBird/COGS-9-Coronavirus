import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt

# Settings
use_most_recent_date = False
label_major_counties = False
date = '2020-11-03'


# Configure plot settings
mplt.rcParams['figure.figsize'] = (8, 5)
plt.style.use('ggplot')  # 7, 14

# Load csv data files
corona_totals = pd.read_csv('ca_county_coronavirus_totals.csv')
county_info = pd.read_csv('ca_county_population_income.csv')

corona_totals.fillna(0.0)

sd_corona = corona_totals[corona_totals.get('county') == 'San Diego'].get(['date', 'confirmed_cases', 'deaths', 'new_confirmed_cases', 'new_deaths'])
sd_corona = sd_corona.sort_values(by='date')

for i in range(sd_corona.shape[0]):
    plt.scatter(x=i+1, y=sd_corona.get('new_confirmed_cases').iloc[i], color=(206/255, 125/255, 16/255))

plt.show()

for i in range(sd_corona.shape[0]):
    plt.scatter(x=i+1, y=sd_corona.get('new_deaths').iloc[i], color=(100/255, 100/255, 100/255))

plt.show()