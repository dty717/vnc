
ser.close()
# insert water data
blueList1 = blueList
redList1 = redList
greenList1 = greenList

water = Element('water',
  np.average(redList1[-300:]),
  np.max(redList1[-300:]),
  np.min(redList1[-300:]),
  np.std(redList1[-300:]),
  np.average(greenList1[-300:]),
  np.max(greenList1[-300:]),
  np.min(greenList1[-300:]),
  np.std(greenList1[-300:]),
  np.average(blueList1[-300:]),
  np.max(blueList1[-300:]),
  np.min(blueList1[-300:]),
  np.std(blueList1[-300:])
)
insertElement(water,'all black')



waterList = list(db.element.find({'name': 'water',"description":"all black"}))
# np.min([])
water = Element('water',
  (np.min([_water["redAverage"] for _water in waterList]),np.max([_water["redAverage"] for _water in waterList])),
  (np.min([_water["redMax"] for _water in waterList]),np.max([_water["redMax"] for _water in waterList])),
  (np.min([_water["redMin"] for _water in waterList]),np.max([_water["redMin"] for _water in waterList])),
  (np.min([_water["redStd"] for _water in waterList]),np.max([_water["redStd"] for _water in waterList])),
  (np.min([_water["greenAverage"] for _water in waterList]),np.max([_water["greenAverage"] for _water in waterList])),
  (np.min([_water["greenMax"] for _water in waterList]),np.max([_water["greenMax"] for _water in waterList])),
  (np.min([_water["greenMin"] for _water in waterList]),np.max([_water["greenMin"] for _water in waterList])),
  (np.min([_water["greenStd"] for _water in waterList]),np.max([_water["greenStd"] for _water in waterList])),
  (np.min([_water["blueAverage"] for _water in waterList]),np.max([_water["blueAverage"] for _water in waterList])),
  (np.min([_water["blueMax"] for _water in waterList]),np.max([_water["blueMax"] for _water in waterList])),
  (np.min([_water["blueMin"] for _water in waterList]),np.max([_water["blueMin"] for _water in waterList])),
  (np.min([_water["blueStd"] for _water in waterList]),np.max([_water["blueStd"] for _water in waterList]))
)
elementList = [water,air]

print(water.match(
          np.average(redList[-30:]),
          np.max(redList[-30:]),
          np.min(redList[-30:]),
          np.std(redList[-30:]),
          np.average(greenList[-30:]),
          np.max(greenList[-30:]),
          np.min(greenList[-30:]),
          np.std(greenList[-30:]),
          np.average(blueList[-30:]),
          np.max(blueList[-30:]),
          np.min(blueList[-30:]),
          np.std(blueList[-30:])
        ),
        air.match(
          np.average(redList[-30:]),
          np.max(redList[-30:]),
          np.min(redList[-30:]),
          np.std(redList[-30:]),
          np.average(greenList[-30:]),
          np.max(greenList[-30:]),
          np.min(greenList[-30:]),
          np.std(greenList[-30:]),
          np.average(blueList[-30:]),
          np.max(blueList[-30:]),
          np.min(blueList[-30:]),
          np.std(blueList[-30:])
        ))