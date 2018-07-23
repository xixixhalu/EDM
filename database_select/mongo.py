from pymongo import MongoClient
import pytz
import time
import json
import sys
from pytz import reference
import calendar
from iso8601 import parse_date
from bson.objectid import ObjectId
from datetime import datetime, timedelta
class DBselect:
        def __init__(self):
        #initial the dictionary data structure
                self.dbjson={} #form json
        def db(self,start,end): 
        """
	    Find the query result of one semester in a database
	    :param start: the start time as UNIX timestamp of one semester
	    :param end: the end time as UNIX timestamp of the corresponding semester
	    :return: query result as json/dict format
	    """
                Client = MongoClient()
                db = Client[sys.argv[1]]
        		#convert UNIX timestamp to ObjectId               
                start=str(start)[2:]+"0000000000000000"
                end=str(end)[2:]+"0000000000000000"
                dic={}
                #traverse the collections of database
                for collec in db.collection_names():
                        if collec=="fs.chunks":
                                continue
                        collection = db[collec]
                        res=[]
                        #get the data from start time to end time
                        for data in collection.find({"_id":{"$gte":ObjectId(start),"$lte":ObjectId(end)}}):
                                items=self.process_data(data)
                                if sorted(items) not in res:
                                        res.append(sorted(items))
                        collec=str(collec).replace('u\'','\'')
                        collec.decode("unicode-escape")
                        dic[collec]=res
                return dic

        def process_data(self,json):
        """
	    Convert unicode to string
	    :param json: unicode format data of query
	    :return: data as the string format
	    """
                item=[]
                for key in json.keys():
                        key=str(key).replace('u\'','\'')
                        key.decode("unicode-escape")
                        item.append(key)
                return item
        
        def iso2unix(self,starttime,endtime):
        """
	    Convert a timestamp formatted in ISO 8601 into a UNIX timestamp
	    :param start: the start time of one semester
	    :param end: the end time of the corresponding semester
	    :return: UNIX timestamp of start and end time
	    """
                start=time.mktime(parse_date(starttime).timetuple())
                start=int(start)
                end=time.mktime(parse_date(endtime).timetuple())
                end=int(end)
                return hex(start), hex(end)

        def start(self):
        		#set the start time and end time for every semester
                period=[["2017-01-08","2017-05-10"],["2017-05-16","2017-08-07"],["2017-08-16","2017-12-13"],["2018-01-08","2018-05-10"]]                
                #process the data
                i=1
                for date in period:
                		#transfer normal time to iso format
                        starttime=date[0]+"T00:00:00Z"
                        endtime=date[1]+"T00:00:00Z"
                        #if not correct format, give the usage
                        if starttime[4]!="-" or endtime[4]!="-":
                                print "Error input arguments!\nUsage: python [filename].py [database_name]"
                                os._exit(-1)
                        else:
                                start,end=self.iso2unix(starttime,endtime)
                                entity=self.db(start,end)
                        #store to json format
                        self.dbjson[str(i)]={"start":date[0],"end":date[1],"entities":entity}
                        i+=1
                #write the json data into a file: mongo.txt
                res=json.dumps(self.dbjson, indent=4, sort_keys=True)
                f=open('./mongo.txt','w')
                f.write(res)
                f.close()
                

if __name__ == "__main__":
	#for testing        
        test=DBselect()
        test.start()