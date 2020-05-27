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
        dataframe1.drop(['nume','parola','isAdmin'],axis=1,inplace=True)
        dataframe1.varsta.loc[(dataframe1.varsta >90) | (dataframe1.varsta<5)] = np.nan
        dataframe1.varsta = dataframe1.varsta.fillna(dataframe1.varsta.mean())
        dataframe1.varsta = dataframe1.varsta.astype(np.int32)
        dataframe1.id = dataframe1.id.astype(np.int32)
    
    # Return value must be of a sequence of pandas.DataFrame
    return dataframe1,
