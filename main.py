# Imports
import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt

# Settings
use_most_recent_date = True
label_major_counties = False
date = '2020-12-12'


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
    death_per_10000=10_000 * (merged_county_info.get('deaths') / merged_county_info.get('population'))
)
merged_county_info = merged_county_info.set_index('county')

# Counties with pop > 700,000
major_counties = merged_county_info[merged_county_info.get('population') > 700_000].index.to_list()

# Counties with pop > 100,000
minor_counties = merged_county_info[(merged_county_info.get('population') < 700_000)
                                    & (merged_county_info.get('population') > 100_000)].index.to_list()


print(merged_county_info)

# Plot Median Income vs. Deaths per 1000 (Blue/Orange/Grey for colorblind-friendly plot)
merged_county_info.plot(kind='scatter', x='median_household_income', y='death_per_10000', alpha=0.8,
                        color=(100/255, 100/255, 100/255))  # Grey
plt.title('Median Income vs. Deaths per 10000 ({})'.format(date), fontname='DejaVu Sans', fontsize=18)
plt.xlabel('Median Household Income', fontname='DejaVu Sans', fontsize=18)
plt.ylabel('Deaths per 10000', fontname='DejaVu Sans', fontsize=18)

for county in merged_county_info.index:
    if county in major_counties:
        if label_major_counties:
            plt.text(
                merged_county_info.get('median_household_income').loc[county],
                merged_county_info.get('death_per_10000').loc[county],
                county, fontname='DejaVu Sans', fontsize=9
            )
        plt.scatter(
            merged_county_info.get('median_household_income').loc[county],
            merged_county_info.get('death_per_10000').loc[county],
            color=(16/255,110/255,206/255)  # Blue
        )
    elif county in minor_counties:
        plt.scatter(
            merged_county_info.get('median_household_income').loc[county],
            merged_county_info.get('death_per_10000').loc[county],
            color=(206 / 255, 125 / 255, 16 / 255)  # Orange
        )


print("Correlation between Median Household Income and Deaths per 1000.")
print("All Counties:    {}".format(round(merged_county_info
                                         .get('median_household_income')
                                         .corr(merged_county_info.get('death_per_10000')), 2)))
df_large = merged_county_info[(merged_county_info.get('population') > 700_000)]
print("Large Counties:  {}".format(round(df_large
                                         .get('median_household_income')
                                         .corr(merged_county_info.get('death_per_10000')), 2)))
z_large = np.polyfit(df_large.get('median_household_income'), df_large.get('death_per_10000'), 1)
p_large = np.poly1d(z_large)

plt.plot(df_large.get('median_household_income'), p_large(df_large.get('median_household_income')), c=(16/255,110/255,206/255))

df_med = merged_county_info[(merged_county_info.get('population') <= 700_000) &
                                                            (merged_county_info.get('population') > 100_000)]
print("Medium Counties: {}".format(round(df_med
                                         .get('median_household_income')
                                         .corr(merged_county_info.get('death_per_10000')), 2)))
z_med = np.polyfit(df_med.get('median_household_income'), df_med.get('death_per_10000'), 1)
p_med = np.poly1d(z_med)

plt.plot(df_med.get('median_household_income'), p_med(df_med.get('median_household_income')), c=(206 / 255, 125 / 255, 16 / 255))

df_small = merged_county_info[merged_county_info.get('population') <= 100_000]

print("Small Counties:  {}".format(round(df_small
                                         .get('median_household_income')
                                         .corr(merged_county_info.get('death_per_10000')), 2)))
z_small = np.polyfit(df_small.get('median_household_income'), df_small.get('death_per_10000'), 1)
p_small = np.poly1d(z_small)

plt.plot(df_small.get('median_household_income'), p_small(df_small.get('median_household_income')), c=(100/255, 100/255, 100/255))


plt.show()
