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

app_id = 'r12725034-16c23909-ef8c-4890'
app_key = '04a695da-a42c-4929-b8de-84f7ffe5b0ec'

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

class TDXAuth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = None
        self.request_count = 0

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        auth_header = {
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }

        auth_response = requests.post(auth_url, auth_header)
        self.request_count += 1

        if auth_response.ok:
            # print('Get TDX Auth!')
            self.auth_response = auth_response
        else:
            raise ConnectionRefusedError(f'TDX Auth Error! Error Code: {auth_response.status_code}')
        
    def get_data_header(self):
        if not self.auth_response or self.request_count >= 45:
            self.get_auth_header()
            time.sleep(0.5)
            self.request_count = 0 # reset

        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')
        self.request_count += 1
        
        return{
            'authorization': 'Bearer '+access_token
        }
        
class RoadData():
    def __init__(self, TDXsever) -> None:
        self.sever = TDXsever
        
    def get_link_data(self, road_name, city, params = None):
        url = f"https://tdx.transportdata.tw/api/basic/v2/Road/Link/CityRoad/{city}/{road_name}?$format=JSON"
        data_response = requests.get(url, headers=self.sever.get_data_header(), params= params)
        if data_response.ok:
                return eval(data_response.text)
        else:
            raise ConnectionError(f'Not get response from TDX. Error Code: {data_response.status_code}')
        
    def get_link_list(self, road_name, city, params = None):
        data = self.get_link_data(road_name, city, params)
        link_id_list = [i['LinkID'] for i in data]
        road_id = data[0]['RoadID']
        return road_id, link_id_list

    def get_geo_json(self, link_id):
        url = f'https://tdx.transportdata.tw/api/basic/v2/Road/Link/Shape/Geometry/GeoJson/{link_id}'
        data_response = requests.get(url, headers=self.sever.get_data_header())
        if data_response.ok:
            return eval(data_response.text)
        else:
            raise ConnectionError(f'Not get response from TDX. Error Code: {data_response.status_code}')
    
    def get_all_geo_json(self, road_name, city = 'Taipei'):
        road_id, link_id_list = self.get_link_list(road_name, city)
        print(road_id, link_id_list)
        all_data = []
        for link_id in link_id_list:
            data = {}
            geo_json = self.get_geo_json(link_id)
            data['road_id'] = road_id
            data['road_name'] = road_name
            data['link_id'] = link_id
            data['geo_json'] = json.dumps(geo_json['features'][0])
            all_data.append(data)
        return all_data
    
    def get_link_info(self, link_id):
        url = f'https://tdx.transportdata.tw/api/basic/v2/Road/Link/LinkID/{link_id}?%24format=JSON'
        data_response = requests.get(url, headers=self.sever.get_data_header())
        if data_response.ok:
            if data_response.text:
                return eval(data_response.text)[0]
            else:
                return None
        else:
            raise ConnectionError(f'Not get response from TDX. Error Code: {data_response.status_code}')

if __name__ == '__main__':

    TDXsever = TDXAuth(app_id, app_key)
    data_loader = RoadData(TDXsever)
    error_log = []

    # # Get Geo Data By road_name
    # road_name = '羅斯福路四段'
    # all_geo_data = data_loader.get_all_geo_json(road_name)
    # print(f'Collect from TDX: {len(all_geo_data)}')

    # Get Geo Data By link_id
    data = [pd.read_csv(f'./data/accident_data(LinkID)_batch_{i}.csv') for i in range(5)]
    data = pd.concat(data)

    all_link_id = data['LinkID'].dropna().drop_duplicates().to_list()
    all_geo_data = []
    for link_id in tqdm(all_link_id):
        if len(link_id.split()) != 1:
            continue

        temp_data = {}
        info = data_loader.get_link_info(link_id)
        
        if not info:
            error_log.append(link_id)
            continue

        temp_data['road_id'] = info['RoadID']
        temp_data['road_name'] = info['RoadName']
        temp_data['link_id'] = link_id

        geo_json = data_loader.get_geo_json(link_id)
        temp_data['geo_json'] =  json.dumps(geo_json['features'][0])

        all_geo_data.append(temp_data)
    
    print(len(all_geo_data))
    

    # Insert into database
    with app.app_context():
        TDX_Database = db.get_db()
        cursor = TDX_Database.cursor()

        cursor.execute("SELECT COUNT(1) from roads")
        before_count = cursor.fetchone()[0]
        print(f'Before Insert: {before_count}')
        
        for item in all_geo_data:
            # check exists
            sql = f"SELECT COUNT(1) from roads WHERE link_id = '{item['link_id']}'"
            cursor.execute(sql)
            exists = cursor.fetchone()[0]

            if exists:
                continue
            else:            
                print('\tInsert...',item['link_id'], item['road_id'], item['road_name'])
                sql = f"INSERT INTO roads (link_id, road_id, road_name, geo_json) \
                        Values('{item['link_id']}', '{item['road_id']}', '{item['road_name']}', '{item['geo_json']}')"
                cursor.execute(sql)

        cursor.execute("SELECT COUNT(1) from roads")
        after_count = cursor.fetchone()[0]
        print(f'After Insert: {after_count}')

        print(f'New Data: {after_count - before_count}')


        TDX_Database.commit()
        print('Commit!')

        TDX_Database.close()

    # paras = {
    #     '$filter': "contains(RoadDirectionID,'3')",
    # }
