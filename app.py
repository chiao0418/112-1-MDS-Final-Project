from flask import Flask, render_template, request
import database as db
import random
import json

app = Flask(__name__)

@app.route("/")
def index():
    TDX_database = db.get_db()
    cursor = TDX_database.cursor()

    district_list = []
    sql = "SELECT lat, lng, name FROM district;"
    for data in cursor.execute(sql):
         district_list.append([[data[0], data[1]],data[2]])

    weekend_list = []
    sql = "SELECT DISTINCT is_weekend FROM demo where climate = '雨';"
    for data in cursor.execute(sql):
         weekend_list.append(data[0])

    time_list = []
    sql = "SELECT DISTINCT time_category FROM demo;"
    for data in cursor.execute(sql):
         time_list.append(data[0])

    climate_list = []
    sql = "SELECT DISTINCT climate FROM demo;"
    for data in cursor.execute(sql):
         climate_list.append(data[0])

    return render_template('index.html', district_list = district_list, weekend_list = weekend_list, time_list = time_list, climate_list = climate_list)


@app.route("/get_geo_data", methods=['POST'])
def get_geo_data():
    weekend, time, climate = request.values.get('weekend'), request.values.get('time'), request.values.get('climate')
    TDX_database = db.get_db()
    cursor = TDX_database.cursor()
    sql = f"""
          SELECT geo_json, label 
          from roads r, demo d
          where r.link_id = d.link_id
          and d.is_weekend = '{weekend}'
          and d.time_category = '{time}'
          and d.climate = '{climate}'
          """
    response_data = []
    for data in cursor.execute(sql):
            json_data = eval(data[0])
            json_data['severity'] = data[1] #random.randint(0, 2)
            response_data.append(json_data)
    return {'geo_data': response_data}


@app.route("/get_accident_data", methods=['GET'])
def get_accident():
    TDX_database = db.get_db()
    cursor = TDX_database.cursor()

    sql = """
           SELECT lat, lon, year || '/' || month || '/' || day as date,
           hour || ':' || minute as time, 
           address,
           death + death_in_month + injured as death_injured,
           climate,
           road_type,
           category
           FROM accident
           WHERE link_id IS NOT NULL
           AND death > 0;
          """

    response_data = []
    for data in cursor.execute(sql):
         info = f"""
               <div>
                    <li>事故時間：{data[2]} {data[3]}</li>
                    <li>事故地址：{data[4]}</li>
                    <li>事故傷亡人數：{data[5]}</li>
                    <li>事故當下氣候：{data[6]}</li>
                    <li>事故類型：{data[8]}</li>
                    <li>道路類型：{data[7]}</li>
               </div>
               """
         json_data = {'location': [data[0], data[1]], 'info': info, 'death_injured': data[5]}
         response_data.append(json_data)
    
    response_data = json.dumps(response_data)
    return {'accident_data': response_data}