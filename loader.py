import pandas as pd
from databaseConnection import DatabaseConnection
import warnings
warnings.filterwarnings('ignore')
import logging

logger = logging.getLogger()
file_handler = logging.FileHandler(filename='LogFiles/logfile.log', mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class Loader:
	@staticmethod
	def load_data():
		try:
			obj = DatabaseConnection()
			obj.db_connect()
			df = pd.read_csv('Data/data.csv')
			
			return df
		except Exception as Argument:
			logging.exception("Error occurred in Loader.load_data()")