import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt

# Configure plot settings
mplt.rcParams['figure.figsize'] = (8, 5)
plt.style.use('ggplot')  # 7, 14

corona_totals = pd.read_csv('ca_county_coronavirus_totals.csv')
county_info = pd.read_csv('ca_county_population_income.csv')

# Counties with pop > 700,000
major_counties = ['Los Angeles', 'San Diego', 'Orange', 'Riverside', 'San Bernardino', 'Santa Clara',
                  'Alameda', 'Sacramento', 'Contra Costa', 'Fresno County', 'Kern', 'San Francisco',
                  'Ventura', 'San Mateo', 'San Joaquin']

most_recent_date = corona_totals.get('date').iloc[0]

corona_by_county = (
    corona_totals[corona_totals.get('date') == most_recent_date]
        .get(['county', 'deaths'])
)

merged_county_info = corona_by_county.merge(county_info, left_on='county', right_on='county')

merged_county_info = merged_county_info.assign(
    death_per_1000=1000 * (merged_county_info.get('deaths') / merged_county_info.get('population'))
)
merged_county_info = merged_county_info.set_index('county')

print(merged_county_info)
merged_county_info.plot(kind='scatter', x='median_household_income', y='death_per_1000', alpha=0.8)
plt.title('Median Income vs. Deaths per 1000', fontname='DejaVu Sans', fontsize=18)
plt.xlabel('Median Household Income', fontname='DejaVu Sans', fontsize=18)
plt.ylabel('Deaths per 1000', fontname='DejaVu Sans', fontsize=18)

for county in merged_county_info.index:
    if county not in major_counties:
        continue

    plt.text(
        merged_county_info.get('median_household_income').loc[county],
        merged_county_info.get('death_per_1000').loc[county],
        county, fontname='DejaVu Sans', fontsize=9
    )

plt.show()
