# Imports
import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt

# Settings
use_most_recent_date = False
date = '2020-11-03'

# Configure plot settings
mplt.rcParams['figure.figsize'] = (8, 5)
plt.style.use('ggplot')  # 7, 14

# Load csv data files
corona_totals = pd.read_csv('ca_county_coronavirus_totals.csv')
county_info = pd.read_csv('ca_county_population_income.csv')

# access most recent date
if use_most_recent_date:
    date = corona_totals.get('date').iloc[0]

# create a dataframe of each county's updated corona info
corona_by_county = (
    corona_totals[corona_totals.get('date') == date]
        .get(['county', 'deaths'])
)

# merge corona table & county info table
merged_county_info = corona_by_county.merge(county_info, left_on='county', right_on='county')

# mutate table with deaths per 1000 pop column
merged_county_info = merged_county_info.assign(
    death_per_1000=1000 * (merged_county_info.get('deaths') / merged_county_info.get('population'))
)
merged_county_info = merged_county_info.set_index('county')

# Counties with pop > 700,000
major_counties = merged_county_info[merged_county_info.get('population') > 700_000].index.to_list()

# Counties with pop > 100,000
minor_counties = merged_county_info[(merged_county_info.get('population') < 700_000)
                                    & (merged_county_info.get('population') > 100_000)].index.to_list()


print(merged_county_info)

# Plot Median Income vs. Deaths per 1000 (Blue/Orange/Grey for colorblind-friendly plot)
merged_county_info.plot(kind='scatter', x='median_household_income', y='death_per_1000', alpha=0.8,
                        color=(100/255, 100/255, 100/255))  # Grey
plt.title('Median Income vs. Deaths per 1000', fontname='DejaVu Sans', fontsize=18)
plt.xlabel('Median Household Income', fontname='DejaVu Sans', fontsize=18)
plt.ylabel('Deaths per 1000', fontname='DejaVu Sans', fontsize=18)

for county in merged_county_info.index:
    if county in major_counties:
        plt.text(
            merged_county_info.get('median_household_income').loc[county],
            merged_county_info.get('death_per_1000').loc[county],
            county, fontname='DejaVu Sans', fontsize=9
        )
        plt.scatter(
            merged_county_info.get('median_household_income').loc[county],
            merged_county_info.get('death_per_1000').loc[county],
            color=(16/255,110/255,206/255)  # Blue
        )
    elif county in minor_counties:
        plt.scatter(
            merged_county_info.get('median_household_income').loc[county],
            merged_county_info.get('death_per_1000').loc[county],
            color=(206 / 255, 125 / 255, 16 / 255)  # Orange
        )

plt.show()
