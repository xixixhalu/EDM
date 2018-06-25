from pymongo import MongoClient
import pytz
import time
from pytz import reference
import calendar
from iso8601 import parse_date
from bson.objectid import ObjectId
def db(start,end):
        Client = MongoClient()
        db = Client.bdr_db_restore
        collection = db.baddriverreports
        start=str(start)[2:]+"0000000000000000"
        end=str(end)[2:]+"0000000000000000"
        for data in collection.find({"_id":{"$gte":ObjectId(start),"$lte":ObjectId(end)}}):
                print data

def iso2unix(starttime,endtime):
        start=time.mktime(parse_date(starttime).timetuple())
        start=int(start)
        end=time.mktime(parse_date(endtime).timetuple())
        end=int(end)
        return hex(start), hex(end)

if  __name__ == '__main__':
        import sys
        from datetime import datetime, timedelta
        #print sys.argv[1]
        if len(sys.argv)>2:
                starttime=sys.argv[1]+"T00:00:00Z"
                endtime=sys.argv[2]+"T00:00:00Z"
        if starttime[4]!="-" or endtime[4]!="-":
                print "Error input arguments!\nUsage: python [filename].py xxxx-xx-xx xxxx-xx-xx"
                os._exit(-1)
        else:
                start,end=iso2unix(starttime,endtime)
                db(start,end)