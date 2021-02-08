import pymongo
import datetime
import csv

client = pymongo.MongoClient("mongodb+srv://admin_3:*mongo3@clusterew1-uogmd.mongodb.net/aqi_tulp?retryWrites=true&w=majority")
db = client.aqi_tulp
col = db.datas

def insert():
    with open('demo1.csv', 'r') as csvfile:
        # reader = csv.DictReader(csvfile)
        
        for row in reversed(list(csv.reader(csvfile))):
            print(row[0])
    # data = {}
    # col.insert(data)
    

def update():
    Filter = {}
    NewData = {} 
    col.update(Filter, NewData)

def delete():
    col.delete_one()

def printOne():
    col.find_one()

def printAll():
    for x in col.find():
        print(x)

if __name__ == "__main__": 
    print('init')
    insert()
    # printAll()