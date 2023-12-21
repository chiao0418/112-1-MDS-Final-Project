CREATE TABLE roads (
    link_id TEXT PRIMARY KEY,
    road_id TEXT NOT NULL,
    road_name TEXT NOT NULL,
    geo_json JSON 
)


CREATE TABLE district(
    id TEXT NOT NULL,
    city TEXT NOT NULL,
    name TEXT  PRIMARY KEY NOT NULL,
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL
)


CREATE TABLE accident(
    year INT NOT NULL, 
    month INT NOT NULL, 
    day INT NOT NULL, 
    hour INT NOT NULL, 
    minute INT NOT NULL, 
    -- process_id INT NOT NULL, 
    -- district_id INT NOT NULL, 
    -- district_name TEXT NOT NULL, 
    address TEXT NOT NULL, 
    death INT NOT NULL, 
    death_in_month INT NOT NULL, 
    injured INT NOT NULL, 
    -- climate_id INT NOT NULL, 
    climate TEXT NOT NULL, 
    -- road_category_id INT NOT NULL, 
    -- speed_limit FLOAT NOT NULL, 
    -- road_type_id INT NOT NULL, 
    road_type TEXT NOT NULL, 
    lon FLOAT NOT NULL, 
    lat FLOAT NOT NULL, 
    road_condition_1 INT NOT NULL, 
    road_condition_2 INT NOT NULL, 
    road_condition_3 INT NOT NULL, 
    -- road_barrier_1 INT NOT NULL, 
    -- road_barrier_2 INT NOT NULL, 
    -- sign_1_id INT NOT NULL, 
    -- sign_2_id INT NOT NULL, 
    -- divide_id INT NOT NULL, 
    -- separate_lane_1_id INT NOT NULL, 
    -- separate_lane_2_id INT NOT NULL, 
    -- separate_lane_3_id INT NOT NULL, 
    -- category_id INT NOT NULL, 
    category TEXT NOT NULL, 
    link_id TEXT
)


CREATE TABLE demo(
    link_id TEXT NOT NULL,
    time_category TEXT NOT NULL,
    is_weekend TEXT NOT NULL,
    climate TEXT NOT NULL,
    label INT NOT NULL
)