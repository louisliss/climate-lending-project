# Second Analysis of HMDA Data

Last time, we set up a framework to look at the top lenders in the riskiest census tracts. This time, we will do two to three more things:

-We will generate an "expected share" metric to compare each lender's percentage of originations in risky tracts to their citywide share of originations to see if lenders are "specializing" in flood-prone areas.
-We will cut the data by multifamily and 1-4 family homes
-We will bring in demographics on high-risk tracts (lower priority)

## Step 1: (From last time) setting up our high risk tracts, narrowing down to originated loans, joining in risk information.

We will read in our high risk

```python

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
%matplotlib inline

os.chdir("Data")

climate = pd.read_csv("climateriskbytract.csv", index_col=0)

classification = lambda x: 1 if x >= 0.50 else 0

climate['9in10yrhirisk'] = climate['9in10yr'].apply(classification)
climate['9in100yrhirisk'] = climate['9in100yr'].apply(classification)
climate['21in10yrhirisk'] = climate['21in10yr'].apply(classification)
climate['21in100yrhirisk'] = climate['21in100yr'].apply(classification)

#Checking how many tracts we get using this 75% threshold
climate[climate['9in10yrhirisk'] == 1].shape
climate[climate['9in100yrhirisk'] == 1].shape
climate[climate['21in10yrhirisk'] == 1].shape
climate[climate['21in100yrhirisk'] == 1].shape

climate = climate[['census_tract_number','9in10yrhirisk','9in100yrhirisk','21in10yrhirisk','21in100yrhirisk']]

hmda = pd.read_csv("hmda_data.csv", index_col=0, low_memory=False)
hmdaclimate = pd.merge(hmda, climate, how='left',on='census_tract_number')
originatedclimate = hmdaclimate[hmdaclimate['action_type'] == 1].copy()

```

##Step 2 (optional): Splitting apart multifamily from 1-4 family; creating a denials dataset

Let's take some slices that we could run in case they're of interest down the road. We can look at originated multifamily vs 1-4 family properties, as well as denials

```python

#property types
originatedmf = originatedclimate[originatedclimate['property_type'] == 3].copy()
originated14 = originatedclimate[originatedclimate['property_type'] == 1].copy()
#about 1200 multifamily mortgages, 148000 1-4 family mortgages

#denials

denials = hmdaclimate[hmdaclimate['action_type'] == 2].copy()
#only 4800 denials: "Application denied by financial institution"

```
##Step 3: Creating "expected share" metric

```python

#first, we need a total count of originations

denom = len(originatedclimate)

#now, we'll count originations by bank for all of boston

df = originatedclimate.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

bosoriginations = pd.merge(df, df2, on='panel_name',how='left')

#let's do that expected share now.

bosoriginations['expected_share'] = bosoriginations['originations'] / denom

#putting it into a format we can merge in later

expectedshare = bosoriginations[['panel_name','expected_share']]

```

##Step 4: Comparing expected vs actual shares in high risk tracts

Here's the first crack of this exercise--are there

21 Inches of SLR, 10-Year Flood

//////////////////////////////////////////////////////////////////////////////

```python

originatedclimate21in10yr = originatedclimate[originatedclimate['21in10yrhirisk'] == 1]

df = originatedclimate21in10yr.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate21in10yr['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

df3 = pd.merge(df, df2, on='panel_name',how='left')

actualdenom = df3['originations'].sum()
df3['actualshare'] = df3['originations'] / actualdenom

originatedclimate21in10yrbanks = pd.merge(df3, expectedshare, on='panel_name', how='left')

originatedclimate21in10yrbanks.head()

originatedclimate21in10yrbanks['delta'] = originatedclimate21in10yrbanks['actualshare'] - originatedclimate21in10yrbanks['expected_share']

plt.scatter(y=originatedclimate21in10yrbanks['actualshare'],x=originatedclimate21in10yrbanks['expected_share'])
plt.xlabel('Expected Share')
plt.ylabel('Actual Share')
plt.plot([-.01,.08],[-.01,.08])

```
