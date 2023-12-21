# import os, sys
# sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))

from flask import Flask
import database as db
import requests

app = Flask(__name__)

url = 'http://api.opencube.tw/twzipcode'
para = {
    'city': '台北市'
}
response = requests.get(url=url, params=para)
data = eval(response.text)['data']

with app.app_context():
    TDX_Database = db.get_db()
    cursor = TDX_Database.cursor()
    for d in data:
        sql = f"INSERT INTO district VALUES ('{d['zip_code']}', '{d['city']}', '{d['district']}', {d['lat']}, {d['lng']})"
        cursor.execute(sql)

    sql = 'SELECT * FROM district;'
    for k in cursor.execute(sql):
        print(k)

    TDX_Database.commit()

    TDX_Database.close()