# Demo for scraping data from Fang.com
The repo provides two demo for scraping data from property listing sites.

The main.py program scraps all property listing data for Beijing and ShengZheng. The data is stored in MongoDB. (Please refer to the section below for access details)

The search.py program will search the property name in Fang.com and return the property information.

## Main.py
The idea behind the scraping is to figure out the hidden API. Usually, Website uses API to return data from their database. Therefore, if we can find it, we can get the data in a more computer friendly way.

To access the demo data, please connect to the Cloud MongoDB server via this link: mongodb+srv://admin:admin@propertychina-xxlht.mongodb.net/test?retryWrites=true&w=majority (You may download [mongodb compass](https://www.mongodb.com/products/compass) or [nosqlbooster](https://nosqlbooster.com/downloads)).

screencap of data:
![](main_cap.png)

### Why MongoDB?
The first database I tried to use is SQL (more precise sqlite). Soon, I encountered the problem that the download data has inconsistent columns. For example, fewer columns in some data, and more columns in some data.

NoSQL is more flexible in terms of table schema. Therefore, I use MongoDB.

## search.py
The logic is the same as Main.py. The codes are similar. The only difference is that search string is passed to the API.

The program will take a CSV input file containing City, District, and Name. Then it returns all matched data. The result is outputted as searchResult.csv. For not found property, it will output a file called notFound.txt.

You can see the files in the git repo.

## Challenges ahead
1. This demo only takes care one property listing site.
2. There will be inconsistency between different property listing sites.
3. The search strings or keywords provided by colleagues may not be exact match with databases.

Solutions:
* We need to write different scripts for different sites. But the logic or methods should be similar.
* We need to build an intermediate database (similar to datawarehouse) to transform the data from different sites into the same format, for example units.
* We need to build a search enginee to take care of exact match problem. For example, by typing 錦安家園 (朝陽區東壩項目), the program will need to know it means 錦安家園 in our database. (In the search.py example, since I just use the search function from Fang.com. It is not a problem. But if we scale it to 20 property sites, we need to have our own search function)

    For search enginee, we may use [elasticsearch](https://www.elastic.co/) which I do not have many experience with it. Still, I think I can manage to figure it out.

## Location search
There is one use case where the program will need to filter all the property listing within a certain area.

As you can see in the database, the data returned contains X, Y coordinates. The filtering can easily be done using Geographical Information System (GIS). I have good knowledge in GIS due to my previous work as an Environmental Consultant. I deal with a lot of Geo Data.

Actually, if the search area can be approximate by a rectangle, we don't even need GIS. We can just filter by coordinates. But, if the search area is a polygon, then GIS is needed.

## How to run
1. Git clone the repo
2. Install the dependencies in the pip file
3. Python program.py to run
