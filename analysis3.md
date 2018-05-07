# Third Analysis of HMDA Data

Our goals(cumulative):

1. Banks by $ amount and share originated, Citywide (as a CSV) -- Done in Analysis 2, saved as bosoriginations.csv
2. Risk levels by $ amount and share, Citywide (as a CSV) -- Done in Analysis 2, saved as total.csv
3. Banks, by risk level, by $ amount, share, and delta from expected share (as 4 CSVs) -- Done in Analysis, saved in data folder as originatedclimate etc etc
4. New this time: Risk levels by bank size in buckets (big=1, med=2, large=3)

## Step 1: setting up our high risk tracts, narrowing down to originated loans, joining in risk information, bucketizing banks by risk level.

The code below sets up a dataframe of all originated mortgages in Boston and links in whether each mortgage is in a high risk tract under various climate scenarios. We've defined high risk as >=50% flooded for now.

```python

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
%matplotlib inline

os.chdir("Data")

climate = pd.read_csv("climateriskbytract.csv", index_col=0)

classification = lambda x: 1 if x >= 0.25 else 0

climate['9in10yrhirisk'] = climate['9in10yr'].apply(classification)
climate['9in100yrhirisk'] = climate['9in100yr'].apply(classification)
climate['21in10yrhirisk'] = climate['21in10yr'].apply(classification)
climate['21in100yrhirisk'] = climate['21in100yr'].apply(classification)

#Checking how many tracts we get using this threshold
# climate[climate['9in10yrhirisk'] == 1].shape
# climate[climate['9in100yrhirisk'] == 1].shape
# climate[climate['21in10yrhirisk'] == 1].shape
# climate[climate['21in100yrhirisk'] == 1].shape

climate = climate[['census_tract_number','9in10yrhirisk','9in100yrhirisk','21in10yrhirisk','21in100yrhirisk']]

hmda = pd.read_csv("hmda_data.csv", index_col=0, low_memory=False)
hmdaclimate = pd.merge(hmda, climate, how='left',on='census_tract_number')
originatedclimate = hmdaclimate[hmdaclimate['action_type'] == 1].copy()

#bank bucketizing

df = originatedclimate.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

bosoriginations = pd.merge(df, df2, on='panel_name',how='left')


#3 buckets
# def banksize (x):
#     if x >= 510220:
#         return 1
#     elif x <= 31465:
#         return 3
#     else:
#         return 2

#4 buckets
# def banksize(x):
#   if x >= 1679597:
#     return 1
#   elif 1679597 > x >= 510220:
#     return 2
#   elif 510220 > x >= 189580:
#     return 3
#   else:
#     return 4

#10 buckets

def banksize(x):
  if x >= 1960483:
    return 1
  elif 1960483 > x >= 1880435:
    return 2
  elif 1960483 > x >= 1136229:
    return 3
  elif 1136229 > x >= 781213:
    return 4
  elif 781213 > x >= 510220:
    return 5
  elif 510220 > x >= 347073:
    return 6
  elif 347073 > x >= 237837:
    return 7
  elif 237837 > x >= 147552:
    return 8
  elif 147552 > x >= 65570:
    return 9
  else:
    return 10

bosoriginations['banksize'] = bosoriginations['loan_amount'].apply(lambda x: banksize(x))


# bosoriginations.to_csv('bosoriginations.csv')

#join bank size into originated loans

banksize = bosoriginations[['panel_name','banksize']]

originatedclimate = pd.merge(originatedclimate, banksize, how='left', on='panel_name')

```


## Look for Steps 2 and 3, as well as a different way of doing Step 4 in Analysis 2


## Step 4: Risk levels by bank sizes

We'll aggregate each risk level by banks, then aggregate by bank size

```python

#9 in 10 yr

originatedclimate9in10yr = originatedclimate[originatedclimate['9in10yrhirisk'] == 1]

df = originatedclimate9in10yr.groupby('banksize').sum().reset_index()
df = df[['banksize','loan_amount']]
denom = df['loan_amount'].sum()
df['percentage'] = df['loan_amount'] / denom

originatedclimate9in10yr = df.copy()

originatedclimate9in10yr


#9 in 100 yr

originatedclimate9in100yr = originatedclimate[originatedclimate['9in100yrhirisk'] == 1]

df = originatedclimate9in100yr.groupby('banksize').sum().reset_index()
df = df[['banksize','loan_amount']]
denom = df['loan_amount'].sum()
df['percentage'] = df['loan_amount'] / denom

originatedclimate9in100yr = df.copy()

originatedclimate9in100yr

#21in10yr

originatedclimate21in10yr = originatedclimate[originatedclimate['21in10yrhirisk'] == 1]

df = originatedclimate21in10yr.groupby('banksize').sum().reset_index()
df = df[['banksize','loan_amount']]
denom = df['loan_amount'].sum()
df['percentage'] = df['loan_amount'] / denom

originatedclimate21in10yr = df.copy()
originatedclimate21in10yr

#21 in 100 yr

originatedclimate21in100yr = originatedclimate[originatedclimate['21in100yrhirisk'] == 1]

df = originatedclimate21in100yr.groupby('banksize').sum().reset_index()
df = df[['banksize','loan_amount']]
denom = df['loan_amount'].sum()
df['percentage'] = df['loan_amount'] / denom


originatedclimate21in100yr = df.copy()

originatedclimate21in100yr
```
