# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd
import datetime
import pyodbc
import time

server = "book-storage.database.windows.net"
database = 'BookDB'
username = "book-storage"
password = "B00kB00k123"
driver= '{SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()



# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):
    # 1 = user_id
    # 2 = users 
    user_id = dataframe1['Col1'].unique().tolist()[0]
    user_info = dataframe2[dataframe2['id'] == user_id]

    if user_info.empty:
        return pd.DataFrame(columns = ['close']),

    premium_acc = user_info['premium'].unique().tolist()[0]
    
    if premium_acc == 0:
        last_date_str = user_info['ultimaDataAdvisor'].astype(str).unique().tolist()[0]
        date_last = datetime.datetime.strptime(last_date_str.split(' ')[0], '%Y-%m-%d').date()
        date_now = datetime.datetime.now().date()
        
        if date_last >= date_now:
            return pd.DataFrame(columns = ['close']),
        
    # update the table with the current date


    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count < 5:
        try:
            cursor.execute("""
        update utilizator
        set ultimaDataAdvisor = CURRENT_TIMESTAMP  
        where id = {};
        """.format(user_id))
            retry_flag = False
            cnxn.commit()
        except:
            retry_count = retry_count + 1
            time.sleep(1)
 
    
    # cursor.close()


    return dataframe1,
