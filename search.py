import time
import requests
import json
import math
from datetime import datetime
import numpy as np
import pandas as pd

df_requests = pd.read_csv("test_data_gz.csv")

df_result = pd.DataFrame()
notFound = []
for index, row in df_requests.iterrows():
    district = row['District']
    city = row['City'] + '.'
    searchString = row['Name']

    print("Working on {} {} : {}".format(district, city, searchString))

    if city == 'bj.':
        url_data ="https://{}newhouse.fang.com/house/s/list/?strDistrict={}&railway=&railway_station=&strPrice=&strRoom=&strPurpose=&housetag=&saling=&strStartDate=&strKeyword={}&strComarea=&strSort=mobileyhnew&isyouhui=&x1=&y1=&x2=&y2=&newCode=&houseNum=&schoolDist=&schoolid=&PageNo={}&zoom=14&city={}&a=ajaxSearch&mapmode=".format('', district,
            searchString,1,city[:-1])
    else:
        url_data ="https://{}newhouse.fang.com/house/s/list/?strDistrict={}&railway=&railway_station=&strPrice=&strRoom=&strPurpose=&housetag=&saling=&strStartDate=&strKeyword={}&strComarea=&strSort=mobileyhnew&isyouhui=&x1=&y1=&x2=&y2=&newCode=&houseNum=&schoolDist=&schoolid=&PageNo={}&zoom=14&city={}&a=ajaxSearch&mapmode=".format(city, district,
            searchString,1,city[:-1])

    while True:
        try:
            res_data = requests.get(url_data)
            json_data = json.loads(res_data.text)
            json_data = json_data['data'] #the reponse data just contains data and list
            if json_data == 'false':
                print("No data found")
                notFound.append(searchString)
            else:
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

                try:
                    df_result = pd.concat([df_result,df_data], axis = 0)
                except:
                    df_result = df_data

            break

        except requests.exceptions.ConnectionError:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            continue

with open('notFound.txt', 'w') as f:
    for item in notFound:
        f.write("%s\n" % item)


df_result.to_csv("searchResult.csv")
