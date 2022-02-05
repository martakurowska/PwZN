import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("adults-smoking-2007-2018.csv")


dt = data.groupby('Entity').agg(continent=("Continent", np.sum), max_percentage=("Prevalence of current tobacco use (% of adults)", np.max), min_percentage=("Prevalence of current tobacco use (% of adults)", np.min))

dt['continent'].replace(0, np.nan, inplace=True)
dt['abs_change'] = dt['max_percentage']-dt['min_percentage']

dt2 = data.groupby('Entity').agg(lambda x: list(x))
dt['Prevalence of current tobacco use (% of adults)'] = dt2['Prevalence of current tobacco use (% of adults)']
dt['Year'] = dt2['Year']

# print(dt)

print(dt['abs_change'].max())  # 17.1 Nepal
print(dt.loc[dt['abs_change'] == dt['abs_change'].max()])

print(dt['abs_change'].min())  # 0.09 Oman
print(dt.loc[dt['abs_change'] == dt['abs_change'].min()])

print(data['Prevalence of current tobacco use (% of adults)'].max()) # Nauru
print(dt.loc[dt['max_percentage'] == dt['max_percentage'].max()])

print(data['Prevalence of current tobacco use (% of adults)'].min()) # Ghana
print(dt.loc[dt['max_percentage'] == dt['max_percentage'].min()])

fig, ax = plt.subplots()

country = ['Nepal', 'Oman', 'Nauru', 'Ghana', 'Poland', 'European Union', 'United States']

for c in country:
    ax.plot(dt.loc[c, :]['Year'], dt.loc[c, :]['Prevalence of current tobacco use (% of adults)'], "-o", label=c)

ax.set_xlabel('Year')
ax.set_ylabel('Share of adults who smoke [%]')
plt.title('Share of adults who smoke, 2007 to 2018')
ax.set_ylim(0,70)
ax.set_xlim(2006.1,2019)
ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0.2)
fig.tight_layout()
plt.grid()
plt.show()
