import time
import requests
import json
import math
from datetime import datetime
import numpy as np
import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@propertychina-xxlht.mongodb.net/test?retryWrites=true&w=majority")
db = client['propertyData']
db_propertyData = db.propertyData

cities = ['','sh.']
for city in cities: #loop through cities
    url_stats = "https://{}newhouse.fang.com/house/s/list/?strDistrict=&railway=&railway_station=&strPrice=&strRoom=&strPurpose=&housetag=&saling=&strStartDate=&strKeyword=&strComarea=&strSort=mobileyhnew&isyouhui=&x1=&y1=&x2=&y2=&newCode=&houseNum=&schoolDist=&schoolid=&PageNo=1&zoom=&city={}&a=ajaxSearch&mapmode=".format(city, city[:-1])

    res_stats = requests.get(url_stats)
    json_stats = json.loads(res_stats.text)

    json_stats = json_stats['stat']['stat']

    # loop through json_stats to get the location and number of records for detail information on property listing
    for dict_data in json_stats:
        location = dict_data['name']
        noOfRecords = int(dict_data['stat']) #max num of records per page: 50
        noOfPage = math.ceil(noOfRecords/50) #count num of page

        print("Working on {}:{}. Total number of records: {}. Total number of pages: {}".format(city, location, noOfRecords, noOfPage))

        #loop through all pages
        for page in list(range(noOfPage)):
            url_data ="https://{}newhouse.fang.com/house/s/list/?strDistrict={}&railway=&railway_station=&strPrice=&strRoom=&strPurpose=&housetag=&saling=&strStartDate=&strKeyword=&strComarea=&strSort=mobileyhnew&isyouhui=&x1=&y1=&x2=&y2=&newCode=&houseNum=&schoolDist=&schoolid=&PageNo={}&zoom=14&city={}&a=ajaxSearch&mapmode=".format(city,location,page+1,city[:-1])

            while True:
                try:
                    res_data = requests.get(url_data)
                    json_data = json.loads(res_data.text)
                    json_data = json_data['data'] #the reponse data just contains data and list
                    json_data = json.loads(json_data) #need to parse the json in string format again
                    json_data = json_data['hit']

                    df_data = pd.DataFrame(json_data)
                    df_data = df_data.astype(str)

                    #add more data
                    df_data['Area'] = city[:-1]
                    df_data['created_on'] = datetime.now()

                    #replace data
                    df_data = df_data.replace('待定', np.nan)
                    df_data[['newCode','zongfen','dianpingcount','tao','saling','x','y','price_num','minarea','maxarea']] = df_data[['newCode','zongfen','dianpingcount','tao','saling','x','y','price_num','minarea','maxarea']].astype(float)


                    records = json.loads(df_data.T.to_json()).values()
                    db_propertyData.insert_many(records)

                    break

                except requests.exceptions.ConnectionError:
                    print("Connection refused by the server..")
                    print("Let me sleep for 5 seconds")
                    print("ZZzzzz...")
                    time.sleep(5)
                    continue
