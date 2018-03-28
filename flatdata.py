import pandas as pd
import numpy as np
import os

os.chdir("Data")

climate = pd.read_csv("climateriskbytract.csv", index_col=0)
hmda = pd.read_csv("hmda_data.csv", index_col=0, low_memory=False)

hmda
