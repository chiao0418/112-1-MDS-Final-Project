# import os, sys
# sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))

from flask import Flask
import requests
import json
import database as db
import time
import pandas as pd
from tqdm import tqdm

app = Flask(__name__)

if __name__ == '__main__':

    data = pd.read_csv(f'./data/demo_data.csv')

    # Insert into database
    with app.app_context():
        TDX_Database = db.get_db()
        cursor = TDX_Database.cursor()

        cursor.execute("SELECT COUNT(1) from demo")
        before_count = cursor.fetchone()[0]
        print(f'Before Insert: {before_count}')
        
        for idx in range(data.shape[0]):
                item = data.iloc[idx]
                print('\tInsert...',item['LinkID'], item['TimeCategory'])
                sql = f"INSERT INTO demo \
                        Values('{item['LinkID']}', '{item['TimeCategory']}', '{item['IsWeekend']}', '{item['天候']}', {item['label']})"
                cursor.execute(sql)

        cursor.execute("SELECT COUNT(1) from demo")
        after_count = cursor.fetchone()[0]
        print(f'After Insert: {after_count}')

        print(f'New Data: {after_count - before_count}')


        TDX_Database.commit()
        print('Commit!')

        TDX_Database.close()
