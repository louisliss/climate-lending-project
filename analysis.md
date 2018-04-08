# Analysis of HMDA Data

## Goals of this analysis:

-Turn percentage flood metric for each tract into binary "high" risk flag for each scenario
-Filter down to "originated" loans
-Look at overall distribution of loan originations among lenders by numbers and amount
-Look at distribution of originations in "high risk" tracts among lenders by number and amount
-Evaluate this "high risk" distribution in the 4 available climate risk scenarios

## Step 1: Identifying "high risk" tracts

For the purposes of this analysis, high risk tracts are more than 50% covered by the flood plain.

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

```

Looks like we only get a handful of tracts using the 50% threshold. We might consider working on this metric in the future, but it should work for now. Let's put it into our HMDA data and winnow down to only loans that were originated.

# Step 2: Narrow down to originated loans, join in high risk info

```python

hmda = pd.read_csv("hmda_data.csv", index_col=0, low_memory=False)
hmdaclimate = pd.merge(hmda, climate, how='left',on='census_tract_number')
originatedclimate = hmdaclimate[hmdaclimate['action_type'] == 1].copy()

#Our dataset of originated loans is now ~150k rows long
originatedclimate.shape

#optional: csv for posterity
# originatedclimate.to_csv('originatedclimate.csv')

```

# Step 3: Look at top Boston mortgage originators in general

Let's look at the population of originated loans and identify the top 10 lenders in Boston

```python

df = originatedclimate.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

bosoriginations = pd.merge(df, df2, on='panel_name',how='left')

#top 10 by originations

bosoriginations = bosoriginations.sort_values(by=['originations'],ascending=False)
top10orig = bosoriginations.head(10)
print(top10orig)

#top 10 by amount

bosoriginations = bosoriginations.sort_values(by=['loan_amount'],ascending=False)
top10amount = bosoriginations.head(10)
print(top10amount)

```
Top 10 by number of Originations:

panel_name  loan_amount  originations
532            QUICKEN LOANS, INC.      1679597          5955
357                  LOANDEPOT.COM      1938749          5837
641                  UNION YES FCU      2302502          5700
289           GUARANTEED RATE INC.      1960483          5599
48                 BANK OF AMER NA      1921483          4222
676              WELLS FARGO BK NA      2093657          4089
546  RESIDENTIAL MORTGAGE SERVICES      1136229          3769
568                SANTANDER BK NA      1239706          3654
190                     EASTERN BK       899979          3092
211     FAIRWAY INDP MORTGAGE CORP       988207          2993

Top 10 by amount of debt ($000s):

panel_name  loan_amount  originations
641                  UNION YES FCU      2302502          5700
676              WELLS FARGO BK NA      2093657          4089
289           GUARANTEED RATE INC.      1960483          5599
357                  LOANDEPOT.COM      1938749          5837
48                 BANK OF AMER NA      1921483          4222
337           JPMORGAN CHASE BK NA      1880435          2866
251              FIRST REPUBLIC BK      1714343          1934
532            QUICKEN LOANS, INC.      1679597          5955
568                SANTANDER BK NA      1239706          3654
546  RESIDENTIAL MORTGAGE SERVICES      1136229          3769

# Step 4: Look at top Mortgage originators in hi risk tracts

We'll look at each scenario separately.

//////////////////////////////////////////////////////////////////////////////

9 Inches of SLR, 10-year Flood:

```python

originatedclimate9in10yr = originatedclimate[originatedclimate['9in10yrhirisk'] == 1]

#uh oh, people--there's literally only one HMDA-disclosed loan in the 10-year floodplain with 9 inches of SLR
originatedclimate9in10yr.shape

df = originatedclimate9in10yr.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate9in10yr['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

originatedclimate9in10yrbanks = pd.merge(df, df2, on='panel_name',how='left')

#top 10 by originations

originatedclimate9in10yrbanks = originatedclimate9in10yrbanks.sort_values(by=['originations'],ascending=False)
top10orig = originatedclimate9in10yrbanks.head(10)
print(top10orig)

#top 10 by amount

originatedclimate9in10yrbanks = originatedclimate9in10yrbanks.sort_values(by=['loan_amount'],ascending=False)
top10amount = originatedclimate9in10yrbanks.head(10)
print(top10amount)

print(tabulate(top10amount,headers="keys",tablefmt="grid"))  



```

Only Bank

+----+---------------------+---------------+----------------+
|    | panel_name          |   loan_amount |   originations |
+====+=====================+===============+================+
|  0 | BOSTON PRIVATE B&TC |          1350 |              1 |
+----+---------------------+---------------+----------------+

//////////////////////////////////////////////////////////////////////////////

9 Inches of SLR, 100-year Flood:

```python

originatedclimate9in100yr = originatedclimate[originatedclimate['9in100yrhirisk'] == 1]


#we're up a to a couple hundred mortgages
originatedclimate9in100yr.shape

df = originatedclimate9in100yr.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate9in100yr['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

originatedclimate9in100yrbanks = pd.merge(df, df2, on='panel_name',how='left')

#top 10 by originations

originatedclimate9in100yrbanks = originatedclimate9in100yrbanks.sort_values(by=['originations'],ascending=False)
top10orig = originatedclimate9in100yrbanks.head(10)
print(top10orig)

#top 10 by amount

originatedclimate9in100yrbanks = originatedclimate9in100yrbanks.sort_values(by=['loan_amount'],ascending=False)
top10amount = originatedclimate9in100yrbanks.head(10)
print(top10amount)

```
Top 10 by Originations

panel_name  loan_amount  originations
56                MSA MORTGAGE LLC         6980            21
47                   LOANDEPOT.COM         6422            19
27              EAST BOSTON SVG BK        19884            18
73  PRIMELENDING A PLAINSCAPITAL C         5010            15
43            GUARANTEED RATE INC.         4895            15
78   RESIDENTIAL MORTGAGE SERVICES         4690            14
89                   UNION YES FCU         4193            13
83                 SANTANDER BK NA         2369             9
33      FAIRWAY INDP MORTGAGE CORP         2823             8
39               FIRST REPUBLIC BK         4243             8

Top 10 by Amount

panel_name  loan_amount  originations
11             BOSTON PRIVATE B&TC        23221             5
27              EAST BOSTON SVG BK        19884            18
67                     PEOPLESBANK         7500             1
56                MSA MORTGAGE LLC         6980            21
47                   LOANDEPOT.COM         6422            19
73  PRIMELENDING A PLAINSCAPITAL C         5010            15
29                      EASTERN BK         4964             4
43            GUARANTEED RATE INC.         4895            15
78   RESIDENTIAL MORTGAGE SERVICES         4690            14
39               FIRST REPUBLIC BK         4243             8

//////////////////////////////////////////////////////////////////////////////

21 Inches of SLR, 10-Year Flood

```python

originatedclimate21in10yr = originatedclimate[originatedclimate['21in10yrhirisk'] == 1]


#same as before
originatedclimate21in10yr.shape

df = originatedclimate21in10yr.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate21in10yr['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

originatedclimate21in10yrbanks = pd.merge(df, df2, on='panel_name',how='left')

#top 10 by originations

originatedclimate21in10yrbanks = originatedclimate21in10yrbanks.sort_values(by=['originations'],ascending=False)
top10orig = originatedclimate21in10yrbanks.head(10)
print(top10orig)

#top 10 by amount

originatedclimate21in10yrbanks = originatedclimate21in10yrbanks.sort_values(by=['loan_amount'],ascending=False)
top10amount = originatedclimate21in10yrbanks.head(10)
print(top10amount)
