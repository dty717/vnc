from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
from random import randint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
dbClient = MongoClient("mongodb://admin:SUPERSECRETPASSWORD@localhost:27017/")

dbSmartFloating = dbClient.SmartFloating

dbDeviceLog = dbSmartFloating.DeviceLog


def dbLogging(currentTime,systemType,info,otherInfo):
    dbDeviceLog.insert_one({
        "time": currentTime,
        "systemType": systemType,
        "info": info,
        "otherInfo": otherInfo
    })

# Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)

def getPosition(img, test1, test2):
    # a = {
    #     'mouseX': 1,
    #     'mouseY': 2,
    #     'effectiveList': [
    #         {
    #             'x':1,
    #             'y':2
    #         }
    #     ]
    # }
    return None


def insertPosition(mouseX, mouseY, heroX, heroY):
    mousePos = db.position.find_one(
        {"mouseX": mouseX, "mouseY": mouseY})
    # _position = {
    #     "x": x,
    #     "y": y
    # }
    if not mousePos:
        db.position.insert_one({
            "mouseX": mouseX,
            "mouseY": mouseY,
            "heroX": heroX,
            "heroY": heroY
        })
    else:
        # mousePos['effectiveList'].append(_position)
        print(mousePos,heroX,heroY)
        db.position.update_one({'_id': mousePos.get('_id')}, {
            "$set": {'heroX': heroX, 'heroY': heroY}})
    return

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