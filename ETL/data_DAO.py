from sqlalchemy import create_engine
# import pandas as pd
# import os
import psycopg2

class DAO:
  def __init__(self):
        db_user = "ubj1eoeaku13t6"
        db_password = "pdef0051a9c37a2f131b786f09aaeb192dffcbe140fe7d048dcc6c62342c3dbcc"
        db_name = "d4i4fjj12gdddt"
        db_host = "c3cj4hehegopde.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
        db_port = 5432
        self.conn2 = create_engine(
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        self.conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port,
        )
        with open("schema.sql", "r") as file:
            sql_query = file.read()
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        self.conn.commit()

dao = DAO