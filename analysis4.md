# Fourth Analysis of HMDA Data

Our goals(cumulative):

1. Shave down the HMDA data to just Boston tracts; existing data includes several North Shore cities and towns.
2. Create a CSV with all banks originating mortgages in Boston, with columns for Total Amount originated in the city, and then Amounts Originated for each risk level.
3. Create a CSV with the top ten lenders in each tract

## Step 1

The code below sets up a dataframe of all originated mortgages in Boston and links in whether each mortgage is in a high risk tract under various climate scenarios. We've defined high risk as >=25% flooded for now. Note that the HMDA data for the Boston Metro Division includes many tracts outside of the City of Boston--the code below also culls the mortgage info for just mortgages in Boston tracts.

```python

import pandas as pd
import numpy as np
import os

os.chdir("Data")

#bring in list of boston census tracts
boston = pd.read_csv("bostontracts.txt")
boston = boston[['NAME10']]
boston = boston.rename(columns={'NAME10':'census_tract_number'})
boston = list(boston['census_tract_number'])


#bring in list of census tracts, cut by boston tracts, assign high risk status
climate = pd.read_csv("climateriskbytract.csv", index_col=0)
climate = climate[climate['census_tract_number'].isin(boston)]

classification = lambda x: 1 if x >= 0.25 else 0

climate['9in10yrhirisk'] = climate['9in10yr'].apply(classification)
climate['9in100yrhirisk'] = climate['9in100yr'].apply(classification)
climate['21in10yrhirisk'] = climate['21in10yr'].apply(classification)
climate['21in100yrhirisk'] = climate['21in100yr'].apply(classification)

# Checking how many tracts we get using this threshold
# climate[climate['9in10yrhirisk'] == 1].shape
# climate[climate['9in100yrhirisk'] == 1].shape
# climate[climate['21in10yrhirisk'] == 1].shape
# climate[climate['21in100yrhirisk'] == 1].shape

climate = climate[['census_tract_number','9in10yrhirisk','9in100yrhirisk','21in10yrhirisk','21in100yrhirisk']]


#bring in hmda data, cut by boston tracts
hmda = pd.read_csv("hmda_data.csv", index_col=0, low_memory=False)
hmda = hmda[hmda['census_tract_number'].isin(boston)]
hmdaclimate = pd.merge(hmda, climate, how='left',on='census_tract_number')
originatedclimate = hmdaclimate[hmdaclimate['action_type'] == 1].copy()

```

## Step 2

The code below does the aggregating for each of the 541 banks lending in the city.

```python


citytotal = originatedclimate.groupby('panel_name').sum().reset_index()
citytotal = citytotal.rename(columns={'loan_amount':'total_loan_amt'})
citytotal = citytotal[['panel_name','total_loan_amt']]

#9in10yr amt
amt9in10yr = originatedclimate[originatedclimate['9in10yrhirisk']==1]
amt9in10yr = amt9in10yr.groupby('panel_name').sum().reset_index()
amt9in10yr = amt9in10yr.rename(columns={'loan_amount':'9in10yr_loan_amt'})
amt9in10yr = amt9in10yr[['panel_name','9in10yr_loan_amt']]

#9in100yr amt
amt9in100yr = originatedclimate[originatedclimate['9in100yrhirisk']==1]
amt9in100yr = amt9in100yr.groupby('panel_name').sum().reset_index()
amt9in100yr = amt9in100yr.rename(columns={'loan_amount':'9in100yr_loan_amt'})
amt9in100yr = amt9in100yr[['panel_name','9in100yr_loan_amt']]

#21in10yr amt
amt21in10yr = originatedclimate[originatedclimate['21in10yrhirisk']==1]
amt21in10yr = amt21in10yr.groupby('panel_name').sum().reset_index()
amt21in10yr = amt21in10yr.rename(columns={'loan_amount':'21in10yr_loan_amt'})
amt21in10yr = amt21in10yr[['panel_name','21in10yr_loan_amt']]

#21in100yr amt
amt21in100yr = originatedclimate[originatedclimate['21in100yrhirisk']==1]
amt21in100yr = amt21in100yr.groupby('panel_name').sum().reset_index()
amt21in100yr = amt21in100yr.rename(columns={'loan_amount':'21in100yr_loan_amt'})
amt21in100yr = amt21in100yr[['panel_name','21in100yr_loan_amt']]


#merging everything into a flat file
merge1 = pd.merge(citytotal, amt9in10yr, how='left', on='panel_name')
merge1 = merge1.fillna({'9in10yr_loan_amt':0})
merge2 = pd.merge(merge1, amt9in100yr, how='left', on='panel_name')
merge2 = merge2.fillna({'9in100yr_loan_amt':0})
merge3 = pd.merge(merge2, amt21in10yr, how='left', on='panel_name')
merge3 = merge3.fillna({'21in10yr_loan_amt':0})
merge4 = pd.merge(merge3, amt21in100yr, how='left', on='panel_name')
merge4 = merge4.fillna({'21in100yr_loan_amt':0})

#fuck yeah
bosoriginationsv2 = merge4.copy()

#export
bosoriginationsv2.to_csv('bosoriginationsv2.csv')

```

##Step 3

The code below starts with the originated climate dataframe and creates the top 10 banks for each tract

```python

originatedclimatetract = originatedclimate.groupby(['census_tract_number','panel_name'],as_index=False).sum()
originatedclimatetract = originatedclimatetract[['census_tract_number','panel_name','loan_amount']]
originatedclimatetract['rank'] = originatedclimatetract.groupby('census_tract_number')['loan_amount'].rank(ascending=False)
originatedclimatetract = originatedclimatetract.sort_values(by=['census_tract_number','rank'])
originatedclimatetract = originatedclimatetract[originatedclimatetract['rank'] < 11]

#export

originatedclimatetract.to_csv('originatedclimatetract.csv')

```
