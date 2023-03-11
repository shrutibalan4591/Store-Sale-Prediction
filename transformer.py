import pandas as pd
from cleaner import Cleaner
import warnings
warnings.filterwarnings('ignore')
import logging

logger = logging.getLogger()
file_handler = logging.FileHandler(filename='LogFiles/logfile.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)



class Transformer:

    #def __init__(self):
    #    self.obj = Cleaner()

    @staticmethod
    def transformData():
        try:
            obj = Cleaner()
            df = obj.inconsistancy_corrector()
            df = obj.missingValueImputer(df)

            df['Item_Category'] = df['Item_Identifier'].apply(lambda x: x[:2])
            df['Item_Category'] = df['Item_Category'].replace({'FD':'Food', 'NC':'Non_Consumables', 'DR':'Drinks'})
            df.loc[df['Item_Category']=='Non_Consumables', 'Item_Fat_Content'] = 'Non_Edible'
            df.drop('Item_Identifier', axis=1, inplace=True)

            cat_columns = ['Item_Fat_Content', 'Item_Type', 'Item_Category', 'Outlet_Identifier', 
                            'Outlet_Establishment_Year', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
            df = pd.get_dummies(df, columns=cat_columns)

            df.to_csv('Data/Final_Data.csv', index=False)

            return df
        except Exception as Argument:
            logging.exception("Error occurred in Transformer.transformData()")