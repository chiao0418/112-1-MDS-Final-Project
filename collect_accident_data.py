# import os, sys
# sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))

from flask import Flask
import database as db
import pandas as pd

app = Flask(__name__)

data = pd.read_csv('./data/accident_data(cleansed).csv')

climate_dict = {
    1: '暴雨', 2: '強風', 3: '風沙', 4: '霧或煙',
    5: '雪', 6: '雨', 7: '陰',8: '晴'
}

category_dict = {
    1: '對向通行中',    
    2: '同向通行中',
    3: '穿越道路中',
    4: '在路上嬉戲',
    5: '在路上作業中',
    6: '衝進路中',
    7: '從停車後(或中)穿出',
    8: '佇立路邊(外)',
    9: '其他',
    10: '對撞',
    11: '對向擦撞',
    12: '同向擦撞',
    13: '追撞',
    14: '倒車撞',
    15: '路口交岔撞',
    16: '側撞',
    17: '其他',
    18: '路上翻車、摔倒',
    19: '衝出路外',
    20: '撞護欄(樁)',
    21: '撞號誌、標誌桿',
    22: '撞收費亭',
    23: '撞交通島',
    24: '撞非固定設施',
    25: '撞橋梁、建築物',
    26: '撞路樹、電桿',
    27: '撞動物',
    28: '撞工程施工',
    29: '其他',
    30: '衝過(或撞壞)遮斷器',
    31: '正越過平交道中',
    32: '暫停位置不當',
    33: '在平交道內無法行動',
    34: '其他',
}


road_type_dict = {
    1: '有遮斷器',
    2: '無遮斷器',
    3: '三岔路',
    4: '四岔路',
    5: '多岔路',
    6: '隧道',
    7: '地下道',
    8: '橋梁',
    9: '涵洞',
    10: '高架道路',
    11: '彎曲路及附近',
    12: '坡路',
    13: '巷弄',
    14: '直路',
    15: '其他',
    16: '圓環',
    17: '廣場'
}

road_condition_1_dict = {
    1: '柏油',
    2: '水泥',
    3: '碎石',
    4: '其他鋪裝',
    5: '無鋪裝',
}

road_condition_2_dict = {
    1: '冰雪',
    2: '油滑',
    3: '泥濘',
    4: '濕潤',
    5: '乾燥',
}

road_condition_3_dict = {
    1: '路面鬆軟',
    2: '突出(高低)不平',
    3: '有坑洞',
    4: '無缺陷'
}

keep_columns = ['發生年度', '發生月', '發生日', '發生時-Hours', '發生分', '肇事地點', '死亡人數', '2-30日死亡人數', '受傷人數', '天候','道路類別','座標-X', '座標-Y','路面狀況1', '路面狀況2', '路面狀況3','事故類型及型態', 'LinkID']
data = data[keep_columns]

with app.app_context():
    TDX_Database = db.get_db()
    cursor = TDX_Database.cursor()

    cursor.execute("SELECT COUNT(1) from accident")
    before_count = cursor.fetchone()[0]
    print(f'Before Insert: {before_count}')

    sql = "INSERT INTO accident VALUES "
    for i in range(data.shape[0]):
        item = data.iloc[i]
        part_sql = f"( \
            {item['發生年度']}, \
            {item['發生月']}, \
            {item['發生日']}, \
            {item['發生時-Hours']}, \
            {item['發生分']}, \
            '{item['肇事地點']}', \
            {item['死亡人數']}, \
            {item['2-30日死亡人數']}, \
            {item['受傷人數']}, \
            '{climate_dict[item['天候']]}', \
            '{road_type_dict[item['道路類別']]}', \
            {item['座標-X']}, \
            {item['座標-Y']}, \
            '{road_condition_1_dict[item['路面狀況1']]}', \
            '{road_condition_2_dict[item['路面狀況2']]}', \
            '{road_condition_3_dict[item['路面狀況3']]}', \
            '{category_dict[item['事故類型及型態']]}', \
            '{item['LinkID']}' \
            )"
        
        if i != data.shape[0] - 1:
            part_sql += ','
            sql += part_sql
        else:
            part_sql += ';'
            sql += part_sql

    cursor.execute(sql)

    cursor.execute("SELECT COUNT(1) from accident")
    after_count = cursor.fetchone()[0]
    print(f'After Insert: {after_count}')

    TDX_Database.commit()
    print('Commit!')

    TDX_Database.close()