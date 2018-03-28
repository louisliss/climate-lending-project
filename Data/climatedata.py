import pandas as pd
import numpy as np
import os

#create a dataframe with a single key column
os.chdir("Data")
hmda = pd.read_csv("hmda_data.csv", low_memory=False)
tracts = pd.DataFrame(hmda['census_tract_number'].unique())
tracts.columns = ['census_tract_number']

#read in 10 year flood with 9 inches of SLR (bhfm)
'''note: percentage column (calculated in arcgis) is the proportion of each
tract projected to be inundated in a flood'''

flood9in10yr = pd.read_csv("9in10yrflood.txt")
flood9in10yrmerge = flood9in10yr[['NAME10', 'percentage']].copy()
flood9in10yrmerge = flood9in10yrmerge.rename(columns={'percentage':'9in10yr', 'NAME10':'census_tract_number'})

#merge into key dataframe with 0s for dry tracts
merge1 = pd.merge(tracts, flood9in10yrmerge, how='outer',on='census_tract_number')
merge1 = merge1.fillna({'9in10yr':0})

#read in 100 year flood with 9 inches of SLR (bhfm), merge into the last
flood9in100yr = pd.read_csv("9in100yrflood.txt")
flood9in100yrmerge = flood9in100yr[['NAME10', 'percentage']].copy()
flood9in100yrmerge = flood9in100yrmerge.rename(columns={'percentage':'9in100yr', 'NAME10':'census_tract_number'})

merge2 = pd.merge(merge1, flood9in100yrmerge, how='outer',on='census_tract_number')
merge2 = merge2.fillna({'9in100yr':0})


#lather, rinse, repeat

flood21in10yr = pd.read_csv("21in10yrflood.txt")
flood21in10yrmerge = flood21in10yr[['NAME10', 'percentage']].copy()
flood21in10yrmerge = flood21in10yrmerge.rename(columns={'percentage':'21in10yr', 'NAME10':'census_tract_number'})

merge3 = pd.merge(merge2, flood21in10yrmerge, how='outer',on='census_tract_number')
merge3 = merge3.fillna({'21in10yr':0})

flood21in100yr = pd.read_csv("21in100yrflood.txt")
flood21in100yrmerge = flood21in100yr[['NAME10', 'percentage']].copy()
flood21in100yrmerge = flood21in100yrmerge.rename(columns={'percentage':'21in100yr', 'NAME10':'census_tract_number'})

merge4 = pd.merge(merge3, flood21in100yrmerge, how='outer',on='census_tract_number')
merge4 = merge4.fillna({'21in100yr':0})

#adding in fema 100yr data, but it needs to be fixed up

fema=pd.read_csv("FEMA100yr.txt")

fematracts = pd.DataFrame(fema['NAME10'].unique())
fematracts.columns = ['NAME10']

area = fema[['NAME10','area']]
area = area.drop_duplicates()

interarea = fema[['NAME10','interarea']]
interarea = interarea.groupby(['NAME10'],as_index=False)['interarea'].sum()

femafinal = pd.merge(area,interarea,how='left',on='NAME10')
femafinal['fema100yr'] = (fema['interarea'] / fema['area']).round(6)
femafinal = femafinal.rename(columns={'NAME10':'census_tract_number'})
femafinal = femafinal.drop(columns=['area','interarea'])

#last merge


finalfloodrisk = pd.merge(merge4,femafinal,how='outer',on='census_tract_number')
finalfloodrisk = finalfloodrisk.fillna({'fema100yr':0})

#export

finalfloodrisk.to_csv("climateriskbytract.csv")
