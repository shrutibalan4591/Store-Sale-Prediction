import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
import numpy as np
import os
import csv

class DatabaseConnection:
  @staticmethod
  def db_connect():
    ASTRA_DB_TOKEN="AstraCS:iQyLbOiYUpxBBjOpKxYMKvnQ"
    ASTRA_DB_SECURE_BUNDLE_LOCATION="secure-connect-personal-project-data.zip"

    username = "token"
    token = ASTRA_DB_TOKEN
    secureBundleLocation = ASTRA_DB_SECURE_BUNDLE_LOCATION

    keyspace = 'sales_prediction'
    table_name = 'sales_prediction_data'         # Name of the table to be accessed

    client_id = 'iQyLbOiYUpxBBjOpKxYMKvnQ'
    client_secret = '6RXh7D4EW,3KrwO_xGASH0ElpjiLBQYH97SzAgatFMN,EXxYlPWMm96LtB1RIE_fm6bPyClhM74kDtXdBAt3LegqcCdErrU_Jj9OsH9OSW+2J1G+FOG4yop8uim9v0Go'

    cloud_config = {'secure_connect_bundle':secureBundleLocation}
    auth_provider = PlainTextAuthProvider(client_id, client_secret)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    session.execute("USE {keyspace};".format(keyspace=keyspace))

    def pandas_factory(colnames, rows):
      return pd.DataFrame(rows, columns=colnames)

    session.row_factory = pandas_factory
    session.default_fetch_size = None

    result = session.execute("SELECT * FROM {table_name};".format(table_name=table_name), timeout=None)

    df=result._current_rows
    os.remove('Data/data.csv')
    df.to_csv('Data/data.csv')