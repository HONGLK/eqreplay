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
                    mqtt_obj = {
                        "Date": None,
                        "Time": None,
                        "Sites": []
                    }
                    i = json.loads(i)
                    #print(i)
                    Date = i["EventTime"].split(" ")[0]
                    Time = i["EventTime"].split(" ")[1]
                    Areas = []
                    mqtt_obj["Date"] = Date
                    mqtt_obj["Time"] = Time

                    for area in i["Arealist"]:
                        payload = {
                            "AreaCode": None,
                            "Source": None,
                            "Intensity": None,
                            "PGA": None
                        }
                        payload["AreaCode"]  = area["AreaCode"]
                        payload["Intensity"] = area["IntensityX"]
                        payload["PGA"] = area["PGAx"]
                        payload["Source"] = area["Source"]
                        #print(payload)
                        #Areas.append(payload)
                        #mqtt_obj["Areas"].append()
                        mqtt_obj["Sites"].append(payload)
                    mqtt.append(mqtt_obj)
                #print(mqtt)
                with open("4_18_replay_sites.json", mode="w") as f:
                    f.write(str(mqtt))
                
            except:
                return "資料格式錯誤"
    except:
        return "找不到mqtt檔案"
    
data = MQTT_to_EQreplay("4_18.json")