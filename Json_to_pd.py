"""
Now here we convert the data read earlier through by web scrapping to pandas data frame
"""

import pandas as pd
import os
# getting path to current file
seperator = os.sep
path = __file__.split(seperator)[:-1]
path = seperator.join(path) + seperator + 'allsides.json'

# making dataframe
with open(path,'r') as f:
    df = pd.read_json(f)
    print(df.head())
