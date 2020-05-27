# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd


def azureml_main(dataframe1 = None, dataframe2 = None):
    # dataframe1 = books data
    # dataframe2 = filter data
    
    
    isbns_result =[]
    
    filter_columns = list(dataframe2.columns)

    criterii = ['titlu','autor','an','editor','categorie']    
    all_none = True
    
    for criteriu in criterii:
        if criteriu in filter_columns:
            elements = dataframe2[criteriu].dropna().unique().tolist()
            if len(elements) > 0:
                all_none = False
                
            dataframe1[criteriu] = dataframe1[criteriu].astype("category")
            for elem in elements:
                isbns_result = isbns_result + dataframe1['isbn'][dataframe1[criteriu].apply(lambda x: True if str(elem) in str(x) else False)].unique().tolist()
    
    if all_none:
        isbns_result = dataframe1['isbn'].dropna().unique()
           
    df = pd.DataFrame(list(set(isbns_result)),columns =['isbn'])
    

    return df,
