# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd
import numpy as np

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):

    if dataframe1 is not None: 
        dataframe1.drop(['imagine'],axis=1,inplace=True)
        dataframe1.drop(['categorie'],axis=1,inplace=True)
        dataframe1.drop(['descriere'],axis=1,inplace=True)
        dataframe1['an'] = dataframe1['an'].replace(0,np.nan)
        dataframe1['an'].fillna(dataframe1['an'].mean(), inplace=True)
        dataframe1['an'] = dataframe1['an'].astype(np.int32)    
        
    return dataframe1,
