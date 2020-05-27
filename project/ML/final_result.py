# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd

def azureml_main(dataframe1 = None, dataframe2 = None):

    if dataframe1.empty:
        return pd.DataFrame(columns = ['close']),

    fine_rezults = dataframe2['isbn'].dropna().unique()

    predicted = dataframe1.values.tolist()
    
    rezult  = []
    
    for row in predicted:
        rezult.append([i for i in row if i in fine_rezults])
    

    return pd.DataFrame(rezult),
