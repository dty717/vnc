from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
from random import randint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
dbClient = MongoClient("mongodb://admin:SUPERSECRETPASSWORD@localhost:27017/")

dbSmartFloating = dbClient.SmartFloating

dbDeviceLog = dbSmartFloating.DeviceLog
dbDeviceHistory = dbSmartFloating.SmartFloatingHistories
dbConcentration1History = dbSmartFloating.Concentration1Histories
dbConcentration2History = dbSmartFloating.Concentration2Histories
dbConcentration3History = dbSmartFloating.Concentration3Histories
dbLocation = dbSmartFloating.location

def dbLogging(currentTime, systemType, info, otherInfo):
    dbDeviceLog.insert_one({
        "time": currentTime,
        "systemType": systemType,
        "info": info,
        "otherInfo": otherInfo
    })

def dbGetLogging(logQuery={}, page=0, nPerPage=30):
    deviceLog = dbDeviceLog.find(logQuery)
    return deviceLog.skip(page * nPerPage).limit(nPerPage)

def dbGetHistory(logQuery={}, page=0, nPerPage=30):
    deviceHistory = dbDeviceHistory.find(logQuery)
    return deviceHistory.skip(page * nPerPage).limit(nPerPage)

def dbSaveHistory(currentTime, value, maxValue, AValue, CValue):
    dbDeviceHistory.insert_one({
        "time": currentTime,
        "value": value,
        "maxValue": maxValue,
        "AValue": AValue,
        "CValue": CValue
    })

def dbGetLastHistory():
    return dbDeviceHistory.find({}).sort('time', -1).limit(1)

def dbSaveConcentration1History(currentTime, value, maxValue, AValue, CValue):
    dbConcentration1History.insert_one({
        "time": currentTime,
        "value": value,
        "maxValue": maxValue,
        "AValue": AValue,
        "CValue": CValue
    })

def dbGetConcentration1History(logQuery={}, page=0, nPerPage=30):
    concentration1History = dbConcentration1History.find(logQuery)
    return concentration1History.skip(page * nPerPage).limit(nPerPage)

def dbSaveConcentration2History(currentTime, value, maxValue, AValue, CValue):
    dbConcentration2History.insert_one({
        "time": currentTime,
        "value": value,
        "maxValue": maxValue,
        "AValue": AValue,
        "CValue": CValue
    })

def dbGetConcentration2History(logQuery={}, page=0, nPerPage=30):
    concentration2History = dbConcentration2History.find(logQuery)
    return concentration2History.skip(page * nPerPage).limit(nPerPage)

def dbSaveConcentration3History(currentTime, value, maxValue, AValue, CValue):
    dbConcentration3History.insert_one({
        "time": currentTime,
        "value": value,
        "maxValue": maxValue,
        "AValue": AValue,
        "CValue": CValue
    })

def dbGetConcentration3History(logQuery={}, page=0, nPerPage=30):
    concentration3History = dbConcentration3History.find(logQuery)
    return concentration3History.skip(page * nPerPage).limit(nPerPage)

def insertLocation(time, latitude, longitude):
    location = dbLocation.find_one(
        {"time": time})
    if not location:
        dbLocation.insert_one({
            "time": time,
            "latitude": latitude,
            "longitude": longitude
        })
    return

def getLastLocation():
    return dbLocation.find({}).sort('time', -1).limit(1)

# insertPosition(1,2,3,4)

# #Step 2: Create sample data
# names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City',
#          'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich', 'Lazy', 'Fun']
# company_type = ['LLC', 'Inc', 'Company', 'Corporation']
# company_cuisine = ['Pizza', 'Bar Food', 'Fast Food',
#                    'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
# for x in range(1, 501):
#     business = {
#         'name': names[randint(0, (len(names)-1))] + ' ' + names[randint(0, (len(names)-1))] + ' ' + company_type[randint(0, (len(company_type)-1))],
#         'rating': randint(1, 5),
#         'cuisine': company_cuisine[randint(0, (len(company_cuisine)-1))]
#     }
#     #Step 3: Insert business object directly into MongoDB via insert_one
#     result = db.position.insert_one(business)
#     #Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 500 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done

# print('finished creating 500 business position')

# fivestar = db.position.find_one({'rating': 5})
# print(fivestar)

# fivestarcount = db.position.find({'rating': 5}).count()
# print(fivestarcount)
