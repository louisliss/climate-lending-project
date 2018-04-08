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
print(tabulate(top10orig,headers="keys",tablefmt="html"))   

#top 10 by amount

bosoriginations = bosoriginations.sort_values(by=['loan_amount'],ascending=False)
top10amount = bosoriginations.head(10)
print(tabulate(top10amount,headers="keys",tablefmt="html"))

```
Top 10 by number of Originations:

<table>
<thead>
<tr><th style="text-align: right;">   </th><th>panel_name                   </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">532</td><td>QUICKEN LOANS, INC.          </td><td style="text-align: right;">      1679597</td><td style="text-align: right;">          5955</td></tr>
<tr><td style="text-align: right;">357</td><td>LOANDEPOT.COM                </td><td style="text-align: right;">      1938749</td><td style="text-align: right;">          5837</td></tr>
<tr><td style="text-align: right;">641</td><td>UNION YES FCU                </td><td style="text-align: right;">      2302502</td><td style="text-align: right;">          5700</td></tr>
<tr><td style="text-align: right;">289</td><td>GUARANTEED RATE INC.         </td><td style="text-align: right;">      1960483</td><td style="text-align: right;">          5599</td></tr>
<tr><td style="text-align: right;"> 48</td><td>BANK OF AMER NA              </td><td style="text-align: right;">      1921483</td><td style="text-align: right;">          4222</td></tr>
<tr><td style="text-align: right;">676</td><td>WELLS FARGO BK NA            </td><td style="text-align: right;">      2093657</td><td style="text-align: right;">          4089</td></tr>
<tr><td style="text-align: right;">546</td><td>RESIDENTIAL MORTGAGE SERVICES</td><td style="text-align: right;">      1136229</td><td style="text-align: right;">          3769</td></tr>
<tr><td style="text-align: right;">568</td><td>SANTANDER BK NA              </td><td style="text-align: right;">      1239706</td><td style="text-align: right;">          3654</td></tr>
<tr><td style="text-align: right;">190</td><td>EASTERN BK                   </td><td style="text-align: right;">       899979</td><td style="text-align: right;">          3092</td></tr>
<tr><td style="text-align: right;">211</td><td>FAIRWAY INDP MORTGAGE CORP   </td><td style="text-align: right;">       988207</td><td style="text-align: right;">          2993</td></tr>
</tbody>
</table>

Top 10 by amount of debt ($000s):

<table>
<thead>
<tr><th style="text-align: right;">   </th><th>panel_name                   </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">641</td><td>UNION YES FCU                </td><td style="text-align: right;">      2302502</td><td style="text-align: right;">          5700</td></tr>
<tr><td style="text-align: right;">676</td><td>WELLS FARGO BK NA            </td><td style="text-align: right;">      2093657</td><td style="text-align: right;">          4089</td></tr>
<tr><td style="text-align: right;">289</td><td>GUARANTEED RATE INC.         </td><td style="text-align: right;">      1960483</td><td style="text-align: right;">          5599</td></tr>
<tr><td style="text-align: right;">357</td><td>LOANDEPOT.COM                </td><td style="text-align: right;">      1938749</td><td style="text-align: right;">          5837</td></tr>
<tr><td style="text-align: right;"> 48</td><td>BANK OF AMER NA              </td><td style="text-align: right;">      1921483</td><td style="text-align: right;">          4222</td></tr>
<tr><td style="text-align: right;">337</td><td>JPMORGAN CHASE BK NA         </td><td style="text-align: right;">      1880435</td><td style="text-align: right;">          2866</td></tr>
<tr><td style="text-align: right;">251</td><td>FIRST REPUBLIC BK            </td><td style="text-align: right;">      1714343</td><td style="text-align: right;">          1934</td></tr>
<tr><td style="text-align: right;">532</td><td>QUICKEN LOANS, INC.          </td><td style="text-align: right;">      1679597</td><td style="text-align: right;">          5955</td></tr>
<tr><td style="text-align: right;">568</td><td>SANTANDER BK NA              </td><td style="text-align: right;">      1239706</td><td style="text-align: right;">          3654</td></tr>
<tr><td style="text-align: right;">546</td><td>RESIDENTIAL MORTGAGE SERVICES</td><td style="text-align: right;">      1136229</td><td style="text-align: right;">          3769</td></tr>
</tbody>
</table>

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

print(tabulate(top10amount,headers="keys",tablefmt="html"))   



```

Only Bank

<table>
<thead>
<tr><th style="text-align: right;">  </th><th>panel_name         </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;"> 0</td><td>BOSTON PRIVATE B&TC</td><td style="text-align: right;">         1350</td><td style="text-align: right;">             1</td></tr>
</tbody>
</table>

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
print(tabulate(top10orig,headers="keys",tablefmt="html"))    


#top 10 by amount

originatedclimate9in100yrbanks = originatedclimate9in100yrbanks.sort_values(by=['loan_amount'],ascending=False)
top10amount = originatedclimate9in100yrbanks.head(10)
print(tabulate(top10amount,headers="keys",tablefmt="html"))   


```
Top 10 by Originations

<table>
<thead>
<tr><th style="text-align: right;">  </th><th>panel_name                    </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">56</td><td>MSA MORTGAGE LLC              </td><td style="text-align: right;">         6980</td><td style="text-align: right;">            21</td></tr>
<tr><td style="text-align: right;">47</td><td>LOANDEPOT.COM                 </td><td style="text-align: right;">         6422</td><td style="text-align: right;">            19</td></tr>
<tr><td style="text-align: right;">27</td><td>EAST BOSTON SVG BK            </td><td style="text-align: right;">        19884</td><td style="text-align: right;">            18</td></tr>
<tr><td style="text-align: right;">73</td><td>PRIMELENDING A PLAINSCAPITAL C</td><td style="text-align: right;">         5010</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">43</td><td>GUARANTEED RATE INC.          </td><td style="text-align: right;">         4895</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">78</td><td>RESIDENTIAL MORTGAGE SERVICES </td><td style="text-align: right;">         4690</td><td style="text-align: right;">            14</td></tr>
<tr><td style="text-align: right;">89</td><td>UNION YES FCU                 </td><td style="text-align: right;">         4193</td><td style="text-align: right;">            13</td></tr>
<tr><td style="text-align: right;">83</td><td>SANTANDER BK NA               </td><td style="text-align: right;">         2369</td><td style="text-align: right;">             9</td></tr>
<tr><td style="text-align: right;">39</td><td>FIRST REPUBLIC BK             </td><td style="text-align: right;">         4243</td><td style="text-align: right;">             8</td></tr>
<tr><td style="text-align: right;">33</td><td>FAIRWAY INDP MORTGAGE CORP    </td><td style="text-align: right;">         2823</td><td style="text-align: right;">             8</td></tr>
</tbody>
</table>

Top 10 by Amount

<table>
<thead>
<tr><th style="text-align: right;">  </th><th>panel_name                    </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">11</td><td>BOSTON PRIVATE B&TC           </td><td style="text-align: right;">        23221</td><td style="text-align: right;">             5</td></tr>
<tr><td style="text-align: right;">27</td><td>EAST BOSTON SVG BK            </td><td style="text-align: right;">        19884</td><td style="text-align: right;">            18</td></tr>
<tr><td style="text-align: right;">67</td><td>PEOPLESBANK                   </td><td style="text-align: right;">         7500</td><td style="text-align: right;">             1</td></tr>
<tr><td style="text-align: right;">56</td><td>MSA MORTGAGE LLC              </td><td style="text-align: right;">         6980</td><td style="text-align: right;">            21</td></tr>
<tr><td style="text-align: right;">47</td><td>LOANDEPOT.COM                 </td><td style="text-align: right;">         6422</td><td style="text-align: right;">            19</td></tr>
<tr><td style="text-align: right;">73</td><td>PRIMELENDING A PLAINSCAPITAL C</td><td style="text-align: right;">         5010</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">29</td><td>EASTERN BK                    </td><td style="text-align: right;">         4964</td><td style="text-align: right;">             4</td></tr>
<tr><td style="text-align: right;">43</td><td>GUARANTEED RATE INC.          </td><td style="text-align: right;">         4895</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">78</td><td>RESIDENTIAL MORTGAGE SERVICES </td><td style="text-align: right;">         4690</td><td style="text-align: right;">            14</td></tr>
<tr><td style="text-align: right;">39</td><td>FIRST REPUBLIC BK             </td><td style="text-align: right;">         4243</td><td style="text-align: right;">             8</td></tr>
</tbody>
</table>

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
print(tabulate(top10orig,headers="keys",tablefmt="html"))   

#top 10 by amount

originatedclimate21in10yrbanks = originatedclimate21in10yrbanks.sort_values(by=['loan_amount'],ascending=False)
top10amount = originatedclimate21in10yrbanks.head(10)
print(tabulate(top10amount,headers="keys",tablefmt="html"))   

```

Top 10 by Originations

<table>
<thead>
<tr><th style="text-align: right;">  </th><th>panel_name                    </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">56</td><td>MSA MORTGAGE LLC              </td><td style="text-align: right;">         6980</td><td style="text-align: right;">            21</td></tr>
<tr><td style="text-align: right;">47</td><td>LOANDEPOT.COM                 </td><td style="text-align: right;">         6422</td><td style="text-align: right;">            19</td></tr>
<tr><td style="text-align: right;">27</td><td>EAST BOSTON SVG BK            </td><td style="text-align: right;">        19884</td><td style="text-align: right;">            18</td></tr>
<tr><td style="text-align: right;">73</td><td>PRIMELENDING A PLAINSCAPITAL C</td><td style="text-align: right;">         5010</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">43</td><td>GUARANTEED RATE INC.          </td><td style="text-align: right;">         4895</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">78</td><td>RESIDENTIAL MORTGAGE SERVICES </td><td style="text-align: right;">         4690</td><td style="text-align: right;">            14</td></tr>
<tr><td style="text-align: right;">89</td><td>UNION YES FCU                 </td><td style="text-align: right;">         4193</td><td style="text-align: right;">            13</td></tr>
<tr><td style="text-align: right;">83</td><td>SANTANDER BK NA               </td><td style="text-align: right;">         2369</td><td style="text-align: right;">             9</td></tr>
<tr><td style="text-align: right;">33</td><td>FAIRWAY INDP MORTGAGE CORP    </td><td style="text-align: right;">         2823</td><td style="text-align: right;">             8</td></tr>
<tr><td style="text-align: right;">39</td><td>FIRST REPUBLIC BK             </td><td style="text-align: right;">         4243</td><td style="text-align: right;">             8</td></tr>
</tbody>
</table>

Top 10 by Amount

<table>
<thead>
<tr><th style="text-align: right;">  </th><th>panel_name                    </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">11</td><td>BOSTON PRIVATE B&TC           </td><td style="text-align: right;">        23221</td><td style="text-align: right;">             5</td></tr>
<tr><td style="text-align: right;">27</td><td>EAST BOSTON SVG BK            </td><td style="text-align: right;">        19884</td><td style="text-align: right;">            18</td></tr>
<tr><td style="text-align: right;">67</td><td>PEOPLESBANK                   </td><td style="text-align: right;">         7500</td><td style="text-align: right;">             1</td></tr>
<tr><td style="text-align: right;">56</td><td>MSA MORTGAGE LLC              </td><td style="text-align: right;">         6980</td><td style="text-align: right;">            21</td></tr>
<tr><td style="text-align: right;">47</td><td>LOANDEPOT.COM                 </td><td style="text-align: right;">         6422</td><td style="text-align: right;">            19</td></tr>
<tr><td style="text-align: right;">73</td><td>PRIMELENDING A PLAINSCAPITAL C</td><td style="text-align: right;">         5010</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">29</td><td>EASTERN BK                    </td><td style="text-align: right;">         4964</td><td style="text-align: right;">             4</td></tr>
<tr><td style="text-align: right;">43</td><td>GUARANTEED RATE INC.          </td><td style="text-align: right;">         4895</td><td style="text-align: right;">            15</td></tr>
<tr><td style="text-align: right;">78</td><td>RESIDENTIAL MORTGAGE SERVICES </td><td style="text-align: right;">         4690</td><td style="text-align: right;">            14</td></tr>
<tr><td style="text-align: right;">39</td><td>FIRST REPUBLIC BK             </td><td style="text-align: right;">         4243</td><td style="text-align: right;">             8</td></tr>
</tbody>
</table>

//////////////////////////////////////////////////////////////////////////////

21 Inches of SLR, 100-Year Flood

```python

originatedclimate21in100yr = originatedclimate[originatedclimate['21in100yrhirisk'] == 1]


#tons more! up to thousands now.
originatedclimate21in100yr.shape

df = originatedclimate21in100yr.groupby('panel_name').sum().reset_index()
df = df[['panel_name','loan_amount']]

df2 = pd.DataFrame(originatedclimate21in100yr['panel_name'].value_counts().reset_index())
df2 = df2.rename(columns={'index':'panel_name','panel_name':'originations'})

originatedclimate21in100yrbanks = pd.merge(df, df2, on='panel_name',how='left')

#top 10 by originations

originatedclimate21in100yrbanks = originatedclimate21in100yrbanks.sort_values(by=['originations'],ascending=False)
top10orig = originatedclimate21in100yrbanks.head(10)
print(tabulate(top10orig,headers="keys",tablefmt="html"))   

#top 10 by amount

originatedclimate21in100yrbanks = originatedclimate21in100yrbanks.sort_values(by=['loan_amount'],ascending=False)
top10amount = originatedclimate21in100yrbanks.head(10)
print(tabulate(top10amount,headers="keys",tablefmt="html"))  

```

Top 10 by Originations

<table>
<thead>
<tr><th style="text-align: right;">   </th><th>panel_name                </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;">107</td><td>GUARANTEED RATE INC.      </td><td style="text-align: right;">        66734</td><td style="text-align: right;">           179</td></tr>
<tr><td style="text-align: right;">240</td><td>UNION YES FCU             </td><td style="text-align: right;">        57602</td><td style="text-align: right;">           151</td></tr>
<tr><td style="text-align: right;">131</td><td>LOANDEPOT.COM             </td><td style="text-align: right;">        42994</td><td style="text-align: right;">           119</td></tr>
<tr><td style="text-align: right;">259</td><td>WELLS FARGO BK NA         </td><td style="text-align: right;">        66448</td><td style="text-align: right;">           118</td></tr>
<tr><td style="text-align: right;"> 96</td><td>FIRST REPUBLIC BK         </td><td style="text-align: right;">        87101</td><td style="text-align: right;">           115</td></tr>
<tr><td style="text-align: right;"> 15</td><td>BANK OF AMER NA           </td><td style="text-align: right;">        55138</td><td style="text-align: right;">            98</td></tr>
<tr><td style="text-align: right;">202</td><td>PROSPECT MORTGAGE, LLC    </td><td style="text-align: right;">        34808</td><td style="text-align: right;">            96</td></tr>
<tr><td style="text-align: right;"> 84</td><td>FAIRWAY INDP MORTGAGE CORP</td><td style="text-align: right;">        26717</td><td style="text-align: right;">            78</td></tr>
<tr><td style="text-align: right;">155</td><td>MSA MORTGAGE LLC          </td><td style="text-align: right;">        25407</td><td style="text-align: right;">            66</td></tr>
<tr><td style="text-align: right;">217</td><td>SANTANDER BK NA           </td><td style="text-align: right;">        19859</td><td style="text-align: right;">            56</td></tr>
</tbody>
</table>

Top 10 by Amount

<table>
<thead>
<tr><th style="text-align: right;">   </th><th>panel_name              </th><th style="text-align: right;">  loan_amount</th><th style="text-align: right;">  originations</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;"> 96</td><td>FIRST REPUBLIC BK       </td><td style="text-align: right;">        87101</td><td style="text-align: right;">           115</td></tr>
<tr><td style="text-align: right;">125</td><td>JPMORGAN CHASE BK NA    </td><td style="text-align: right;">        67068</td><td style="text-align: right;">            44</td></tr>
<tr><td style="text-align: right;">107</td><td>GUARANTEED RATE INC.    </td><td style="text-align: right;">        66734</td><td style="text-align: right;">           179</td></tr>
<tr><td style="text-align: right;">259</td><td>WELLS FARGO BK NA       </td><td style="text-align: right;">        66448</td><td style="text-align: right;">           118</td></tr>
<tr><td style="text-align: right;"> 29</td><td>BOSTON PRIVATE B&TC     </td><td style="text-align: right;">        63948</td><td style="text-align: right;">            46</td></tr>
<tr><td style="text-align: right;">240</td><td>UNION YES FCU           </td><td style="text-align: right;">        57602</td><td style="text-align: right;">           151</td></tr>
<tr><td style="text-align: right;"> 15</td><td>BANK OF AMER NA         </td><td style="text-align: right;">        55138</td><td style="text-align: right;">            98</td></tr>
<tr><td style="text-align: right;"> 69</td><td>EAST BOSTON SVG BK      </td><td style="text-align: right;">        53956</td><td style="text-align: right;">            48</td></tr>
<tr><td style="text-align: right;"> 68</td><td>EAST BOSTON SAVINGS BANK</td><td style="text-align: right;">        43068</td><td style="text-align: right;">            21</td></tr>
<tr><td style="text-align: right;">131</td><td>LOANDEPOT.COM           </td><td style="text-align: right;">        42994</td><td style="text-align: right;">           119</td></tr>
</tbody>
</table>
