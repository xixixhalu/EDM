from pymongo import MongoClient
import pytz
import time
from pytz import reference
import calendar
from iso8601 import parse_date
from bson.objectid import ObjectId
from datetime import datetime, timedelta
class DBselect:
        def __init__(self):
                self.dbjson={}
        def db(self,start,end):
                Client = MongoClient()
                db = Client.bdr_db_restore
                start=str(start)[2:]+"0000000000000000"
                end=str(end)[2:]+"0000000000000000"
                dic={}
                for collec in db.collection_names():
                        if collec=="fs.chunks":
                                continue
                        collection = db[collec]
                        res=[]

                        for data in collection.find({"_id":{"$gte":ObjectId(start),"$lte":ObjectId(end)}}):
                                items=self.process_data(data)
                                if sorted(items) not in res:
                                        res.append(sorted(items))
                        collec=str(collec).replace('u\'','\'')
                        collec.decode("unicode-escape")
                        dic[collec]=res
                return dic


        def process_data(self,json):
	            item=[]
                for key in json.keys():
                        key=str(key).replace('u\'','\'')
                        key.decode("unicode-escape")
                        item.append(key)
                return item

        def iso2unix(self,starttime,endtime):
                start=time.mktime(parse_date(starttime).timetuple())
                start=int(start)
                end=time.mktime(parse_date(endtime).timetuple())
                end=int(end)
                return hex(start), hex(end)

        def start(self):
                period=[["2017-01-08","2017-05-10"],["2017-05-16","2017-08-07"],["2017-08-16","2017-12-13"],["2018-01-08","2018-05-10"]]
                i=1
                for date in period:

                        starttime=date[0]+"T00:00:00Z"
                        endtime=date[1]+"T00:00:00Z"
                        if starttime[4]!="-" or endtime[4]!="-":
                                print "Error input arguments!\nUsage: python [filename].py xxxx-xx-xx xxxx-xx-xx"
                                os._exit(-1)
                        else:
                                start,end=self.iso2unix(starttime,endtime)
                                entity=self.db(start,end)
                        self.dbjson[str(i)]={"start":date[0],"end":date[1],"entities":entity}
                        i+=1
                print self.dbjson
test=DBselect()
test.start()