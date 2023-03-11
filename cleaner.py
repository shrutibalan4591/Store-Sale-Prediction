import pandas as pd
import numpy as np
from loader import Loader
import warnings
warnings.filterwarnings('ignore')
import logging

logger = logging.getLogger()
file_handler = logging.FileHandler(filename='LogFiles/logfile.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class Cleaner:
    #def __init__(self):
    #    self.obj = Loader()

    @staticmethod
    def inconsistancy_corrector():
        try:
            # Load data
            ld = Loader()
            df = ld.load_data()  

            df['Item_Fat_Content'].replace({'low fat':'Low Fat',
                                            'LF':'Low Fat',
                                            'reg':'Regular'}, inplace=True)
            return df
        except Exception as Argument:
            logging.exception("Error occurred in Cleaner.inconsistancy_corrector()")
    
    @staticmethod
    def missingValueImputer(df):
        #----------------------------Imputing Item_Weight------------------------------
        # Create a function to impute Item_Weight
        def impute_itemWeight(item_id):
            try:
                if len(id_weight[item_id])==0:
                    return np.nan
                else:
                    return id_weight[item_id][0]
            except Exception as Argument:
                logging.exception("Error occurred in Cleaner.misingValueImputer.impute_itemWeight()")

        try:
            # Find the Item_Identifier for the missing values
            item_id_list = df[df['Item_Weight'].isnull()]['Item_Identifier'].unique()

            # For each Item_Identifier in item_id_list, find the different item weights available (excluding the missing values, of course)
            id_weight = {}
            for id in item_id_list:
                id_weight[id] = list(df[(df['Item_Identifier']==id) & (df['Item_Weight'].isnull()==False)]['Item_Weight'].unique())

            ## Looping through the dataframe to replace null Item_Weight with appropriate values using function impute_itemWeight()
            indices = df[df['Item_Weight'].isnull()].index.values
            for i in indices:
                df['Item_Weight'][i] = impute_itemWeight(df['Item_Identifier'][i])

            # Drop those 4 rows with null Item_Weight
            df.dropna(subset=['Item_Weight'], inplace=True)
        except Exception as Argument:
            logging.exception("Error occurred in Cleaner.missingValueImputer()")

        #---------------------------Imputing Outlet_Size------------------------------
        # function to impute Item_Weight
        def impute_outletSize(outlet_type):
            try:
                if outlet_type == 'Supermarket Type1' :
                    return np.nan
                else:
                    return size_type[outlet_type][0]
            except Exception as Argument:
                logging.exception("Error occurred in Cleaner.missingValueImputer.impute_outletSize()")

        # Find unique values of Outlet_Size for each Outlet_Type (excluding the missing values, of course)
        try:
            size_type = {}
            for type in df['Outlet_Type'].unique():
                size_type[type] = list(df[(df['Outlet_Type']==type) & (df['Outlet_Size'].isnull()==False)]['Outlet_Size'].unique())

            ## Looping through the dataframe to replace null Outlet_Size with appropriate values using function impute_outletSize()
            indices = df[df['Outlet_Size'].isnull()].index.values
            for i in indices:
                df['Outlet_Size'][i] = impute_outletSize(df['Outlet_Type'][i])

            # Find the Item_Identifier for the missing Outlet_Size (if any)
            outlet_id_list = df[df['Outlet_Size'].isnull()]['Outlet_Identifier'].unique()  

            # We have only one outlet size here ie, 'Small'. Therefore, we impute the remaining missing Outlet_Size as Small
            df['Outlet_Size'].fillna('Small', inplace=True)     

            df.to_csv('Data/Data_Clean.csv')

            return df
        except Exception as Argument:
            logging.exception("Error occurred in Cleaner.missingValueImputer()")
                

        