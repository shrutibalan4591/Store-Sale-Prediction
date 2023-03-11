import pandas as pd
from transformer import Transformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pickle
import logging

logger = logging.getLogger()
file_handler = logging.FileHandler(filename='LogFiles/logfile.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

class Modeler:

    def __init__(self):
        pass

    @staticmethod
    def normalizer():
        try:
            obj = Transformer()
            df = obj.transformData()

            X = df.drop(['Item_Outlet_Sales', 'Unnamed: 0', 'Table_Id'], axis=1)
            y = df['Item_Outlet_Sales']

            scaler = StandardScaler()
            X = scaler.fit_transform(X)

            return (X,y)
        except Exception as Argument:
            logging.exception("Error occurred in Modeler.normalizer()")


    @staticmethod
    def fitModel(X, y):
        try:
            rf_reg2 = RandomForestRegressor(max_depth=18, max_features=None, max_leaf_nodes=18, n_estimators=50)
            rf_reg2.fit(X, y)

            return rf_reg2
        except Exception as Argument:
            logging.exception("Error occurred in Modeler.fitModel()")

    #@staticmethod
    def createModel(self):
        try:
            X, y = self.normalizer()
            model = self.fitModel(X, y)
            pickle.dump(model, open('model.pkl', 'wb'))
        except Exception as Argument:
            logging.exception("Error occurred in Modler.createModel()")