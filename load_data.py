import json
def load_data():
    with open("testdata.json", "r", encoding='utf-8') as d:
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
