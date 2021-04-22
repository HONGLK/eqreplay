import json
import pandas as pd
def load_data(filename):
    with open(filename, "r", encoding='utf-8') as d:
        data = json.loads(d.read())
        #for i in data:
            #data_structure = []
            #yield i["date"], i["time"]
            #for j in i["Areas"]:
            #    AreaCode = j["AreaCode"]
            #    Source = j["Source"]
            #    Intensity = j["Intensity"]
            #    PGA = j["PGA"]
    return data
 
def load_site(filename):
    with open(filename, "r", encoding="utf-8") as d:
        data = json.loads(d.read())
    site_data = pd.DataFrame(columns=["Site_Name", "Site_ID", "Site_Lat", "Site_Lon", "Site_Level", "PGAx", "Datetime"])

    for i in data:
        Date = i["Date"]
        Time = i["Time"]
        for site in i["Sites"]:
            li = list(site.values())
            li.append(str(Date+" "+Time))
            df = pd.Series((li), index=site_data.columns)
            site_data = site_data.append(df, ignore_index=True)

    return site_data