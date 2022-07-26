import json
from numpy import append
import pandas as pd
from datetime import datetime
import os
def load_data(filename):
    with open(filename, "r", encoding='utf-8') as d:
        data = json.loads(d.read())
    #data_df = pd.DataFrame(columns=["DateTime", "Areas"])
    #for i in data:
        #li = list()
        #li.append(datetime.strptime(i["Date"]+" "+i["Time"], "%Y-%m-%d %H:%M:%S.%f"))
        #li.append(i["Areas"])
        #df = pd.Series((li), index=data_df.columns)
        #data_df = data_df.append(df, ignore_index=True)
    return data#data_df
 
def load_site(filename):
    with open(filename, "r", encoding="utf-8") as d:
        data = json.loads(d.read())
    site_data = pd.DataFrame(columns=["Site_ID", "Site_Lat", "Site_Lon", "Site_Level", "PGAx", "Trigger_Time"])
    print(os.getcwd())
    loc = pd.read_csv(f"C:\\Git\\eqreplay\\Source\\Site_loc.csv")
    

    for i in data:
        Date = i["Date"]
        Time = i["Time"]
        pga = i["PGAx"]
        site_id = i["Site_ID"]
        site_Lat = loc.loc[site_id == loc["Site_ID"], ["Site_Lat", "Site_Lon"]].values[0][0]
        site_Lon = loc.loc[site_id == loc["Site_ID"], ["Site_Lat", "Site_Lon"]].values[0][1]
        level = pga_to_level(pga)
        li = list()
        li.append(site_id)
        li.append(site_Lat)
        li.append(site_Lon)
        li.append(level)
        li.append(pga)
        li.append(datetime.strptime(str(Date+" "+Time), "%Y-%m-%d %H:%M:%S.%f"))
        #li.append(str(Date+" "+Time))
        #print(li)
        df = pd.Series((li), index=site_data.columns)
        site_data = site_data.append(df, ignore_index=True)
        #print(site_data)

    return site_data

def pga_to_level(pga=float):
    if pga < 0.8:
        level = 0
        return level
    elif pga >= 0.8 and pga < 2.5:
        level = 1.0
        return level
    elif pga >= 2.5 and pga < 8.0:
        level = 2.0
        return level
    elif pga >= 8.0 and pga < 25:
        level = 3.0
        return level
    elif pga >= 25 and pga < 80:
        level = 4.0
        return level
    elif pga >= 80 and pga < 140:
        level = 5.0
        return level
    elif pga >= 140 and pga < 250:
        level = 5.5
        return level
    elif pga >= 250 and pga < 440:
        level = 6.0
        return level
    elif pga >= 440 and pga < 800:
        level = 6.5
        return level
    elif pga >= 800 and pga < 2000:
        level = 7.0
        return level

#print(pga_to_level(float("188.8")))
#print(load_data(".//4.18//Alarms_026.json"))