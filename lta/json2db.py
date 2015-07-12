import os
import sys
import MySQLdb
import datetime
import re
import json
from pprint import pprint

columns = {}
columns["traffic_incident"] = ["incident_id", "create_date", "incident_type",
                               "latitude", "longitude", "message"]
columns["bus_arrival"] = ["timestamp", "bus_stop_id", "eta", "bus_load"]
columns["expw_travel_time"] = ["id", "timestamp", "expw_name", "direction",
                               "start_pt", "end_pt", "est_travel_time"]
columns["taxi_avail"] = ["timestamp", "latitude", "longitude"]

def make_column_tuple(columns):
    return "(" + ",".join([str(column) for column in columns]) + ")"

def make_values_placeholder(columns):
    return "(" + ",".join(["%s" for column in columns]) + ")"

def insert_many(table, values):
    conn = MySQLdb.connect("localhost", "root", "", "hackathon")
    cur = conn.cursor()

    cols = columns[table]
    ins_query = ("INSERT INTO " + table + " " +
                 make_column_tuple(cols) + " " +
                 "VALUES " + make_values_placeholder(cols))
    # print ins_query

#    create_date = datetime.datetime.strptime("20150130113752", "%Y%m%d%H%M%S")
#    create_date_str = create_date.strftime("%Y-%m-%d %H:%M:%S")

#    ins_value = (123, create_date_str, "accident", "1.3768290", "183.0", "hello world")
 
    try:
        cur.executemany(ins_query, values)
        conn.commit()
    except:
        conn.rollback()

    conn.close()

def j2v_traffic_incident(obj):
    d = obj["CreateDate"]
    lat = obj["Latitude"]
    lon = obj["Longitude"]
    msg = obj["Message"]
    typ = obj["Type"]
    iid = obj["IncidentID"]
    d = d[6:-2]
    cdate = datetime.datetime.fromtimestamp(int(d) / 1000)
    cdate_str = cdate.strftime("%Y-%m-%d %H:%M:%S")
    return (iid, cdate_str, typ, lat, lon, msg)

def parse_traffic_incident(path):
    with open(path) as infile:
        jsonObj = json.load(infile)

    values = []
    for obj in jsonObj:
        values.append(j2v_traffic_incident(obj))

    insert_many("traffic_incident", values)

def j2v_expw_travel_time(obj):
    tid = obj["TravelTimeID"]
    d = obj["CreateDate"]
    expw_name = obj["Name"]
    direction = obj["Direction"]
    start_pt = obj["StartPoint"]
    end_pt = obj["EndPoint"]
    ett = obj["EstimatedTime"]
    d = d[6:-2]
    cdate = datetime.datetime.fromtimestamp(int(d) / 1000)
    cdate_str = cdate.strftime("%Y-%m-%d %H:%M:%S")
    return (tid, cdate_str, expw_name, direction, start_pt, end_pt, ett)

def parse_expw_travel_time(path):
    with open(path) as infile:
        jsonObj = json.load(infile)

    values = []
    for obj in jsonObj:
        values.append(j2v_expw_travel_time(obj))

    insert_many("expw_travel_time", values)

def j2v_taxi_avail(obj, cdate_str):
    lat = obj["Latitude"]
    lon = obj["Longitude"]
    return (cdate_str, lat, lon)

def parse_taxi_avail(path):
    with open(path) as infile:
        jsonObj = json.load(infile)

    d = os.getcwd().split('/')[-1]
    year = d[0:4]
    month = d[4:6]
    day = d[6:8]
    hour = d[8:10]
    minute = d[10:12]
    second = d[12:14]

    cdate_str = "%s-%s-%s %s:%s:%s" % (year, month, day, hour, minute, second)
    values = []
    for obj in jsonObj["value"]:
        values.append(j2v_taxi_avail(obj, cdate_str))

    insert_many("taxi_avail", values)
    
parse_traffic_incident("IncidentSet.json")
parse_expw_travel_time("TravelTimeSet.json")
# parse_taxi_avail(sys.argv[1])

