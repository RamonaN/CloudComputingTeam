# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd
import numpy as np

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):

    ratings_new = dataframe1[dataframe1.utilizator.isin(dataframe2.id)]
    
    ratings_explicit = ratings_new[ratings_new.rating != 0]
    ratings_implicit = ratings_new[ratings_new.rating == 0]
    
    users_exp_ratings = dataframe2[dataframe2.id.isin(ratings_explicit.utilizator)]
    users_imp_ratings = dataframe2[dataframe2.id.isin(ratings_implicit.utilizator)]
    
    counts1 = ratings_explicit['utilizator'].value_counts()
    ratings_explicit = ratings_explicit[ratings_explicit['utilizator'].isin(counts1[counts1 >= 1].index)]
    counts = ratings_explicit['rating'].value_counts()
    ratings_explicit = ratings_explicit[ratings_explicit['rating'].isin(counts[counts >= 1].index)]
    
    ratings_matrix = ratings_explicit.pivot(index='utilizator', columns='isbn', values='rating')
    ratings_matrix.fillna(0, inplace = True)
    ratings_matrix = ratings_matrix.astype(np.int32)
    
    return ratings_matrix,
