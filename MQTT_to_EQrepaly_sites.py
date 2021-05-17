import os
import json

def MQTT_to_EQreplay(file_name):
    file_path = os.path.join(os.path.join(os.getcwd(), "mqtt"), file_name)
    #yield(file_path)
    try:
        with open(file_path, encoding="utf-8") as mqtt_file:
            mqtt = []

            try:
                data = mqtt_file.readlines()
                #print(data)
                print("取得檔案成功")
                print("行數:", len(data))


                for i in data:
                    print(i)
                    mqtt_obj = {
                        "Date": None,
                        "Time": None,
                        "Sites": None
                    }              

                    payload = {
                        "Site_Name": None,
                        "Site_ID": None,
                        "Site_Lat": None,
                        "Site_Lon": None,
                        "Site_Level": None,
                        "PGAx": None
                    }
                    i = json.loads(i)
                    #print(i)
                    Date = i["EventTime"].split(" ")[0]
                    Time = i["EventTime"].split(" ")[1]

                    mqtt_obj["Date"] = Date
                    mqtt_obj["Time"] = Time


                    payload["Site_ID"]  = i["SiteID"]
                    payload["PGAx"] = i["PGAx"]

                    #print(payload)
                    #Areas.append(payload)
                    #mqtt_obj["Areas"].append()
                    mqtt_obj["Sites"] = payload
                    mqtt.append(mqtt_obj)
                #print(123)
                with open("4_18_replay_sites.json", mode="a") as f:
                    f.write(str(mqtt))
                
            except:
                return "資料格式錯誤"
    except:
        return "找不到mqtt檔案"
    
data = MQTT_to_EQreplay("RAW-site.json")
print(data)