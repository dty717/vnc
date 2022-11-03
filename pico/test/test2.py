ser.close()
# insert air data
blueList0 = blueList
redList0 = redList
greenList0 = greenList

air = Element('air',
  np.average(redList0[-300:]),
  np.max(redList0[-300:]),
  np.min(redList0[-300:]),
  np.std(redList0[-300:]),
  np.average(greenList0[-300:]),
  np.max(greenList0[-300:]),
  np.min(greenList0[-300:]),
  np.std(greenList0[-300:]),
  np.average(blueList0[-300:]),
  np.max(blueList0[-300:]),
  np.min(blueList0[-300:]),
  np.std(blueList0[-300:])
)
insertElement(air,'all black')



airList = list(db.element.find({'name': 'air',"description":"all black"}))
# np.min([])
air = Element('air',
  (np.min([_air["redAverage"] for _air in airList]),np.max([_air["redAverage"] for _air in airList])),
  (np.min([_air["redMax"] for _air in airList]),np.max([_air["redMax"] for _air in airList])),
  (np.min([_air["redMin"] for _air in airList]),np.max([_air["redMin"] for _air in airList])),
  (np.min([_air["redStd"] for _air in airList]),np.max([_air["redStd"] for _air in airList])),
  (np.min([_air["greenAverage"] for _air in airList]),np.max([_air["greenAverage"] for _air in airList])),
  (np.min([_air["greenMax"] for _air in airList]),np.max([_air["greenMax"] for _air in airList])),
  (np.min([_air["greenMin"] for _air in airList]),np.max([_air["greenMin"] for _air in airList])),
  (np.min([_air["greenStd"] for _air in airList]),np.max([_air["greenStd"] for _air in airList])),
  (np.min([_air["blueAverage"] for _air in airList]),np.max([_air["blueAverage"] for _air in airList])),
  (np.min([_air["blueMax"] for _air in airList]),np.max([_air["blueMax"] for _air in airList])),
  (np.min([_air["blueMin"] for _air in airList]),np.max([_air["blueMin"] for _air in airList])),
  (np.min([_air["blueStd"] for _air in airList]),np.max([_air["blueStd"] for _air in airList]))
)
elementList = [water,air]



