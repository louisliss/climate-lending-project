import pandas as pd
import numpy as np
import os

os.chdir("Data")

climate = pd.read_csv("climateriskbytract.csv", index_col=0)

classification = lambda x: 1 if x >= 0.25 else 0

climate['9in10yrhirisk'] = climate['9in10yr'].apply(classification)
climate['9in100yrhirisk'] = climate['9in100yr'].apply(classification)
climate['21in10yrhirisk'] = climate['21in10yr'].apply(classification)
climate['21in100yrhirisk'] = climate['21in100yr'].apply(classification)

climate = climate[['census_tract_number','9in10yrhirisk','9in100yrhirisk','21in10yrhirisk','21in100yrhirisk']]

hmda = pd.read_csv("hmda_data.csv", index_col=0, low_memory=False)
hmdaclimate = pd.merge(hmda, climate, how='left',on='census_tract_number')
originatedclimate = hmdaclimate[hmdaclimate['action_type'] == 1].copy()

df = originatedclimate.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

bosoriginations = pd.merge(df, df2, on='panel_name',how='left')

def banksize (x):
    if x >= 510220:
        return 1
    elif x <= 31465:
        return 3
    else:
        return 2

bosoriginations['banksize'] = bosoriginations['loan_amount'].apply(lambda x: banksize(x))

bosoriginations[bosoriginations['banksize'] == 1].head()



bosoriginations.to_csv('bosoriginations.csv')
