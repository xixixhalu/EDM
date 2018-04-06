import parser.parse_dm_file as p

import os
from parser.parse_dm_file import Analyzer as p
from parser.domain_model import DomainModel as dmo
from database_setup.setup import DBUtilities as dbu


ana = p()
dom = ana.DM_File_Analyze('../Input', {'DM_Input_type': "Simple_XML"})


# dbutils = dbu()
# dbutils.setup(configDictionary={"host":"127.0.0.1","port":32768})
# dbutils.createOrUpdateDB(dom)
# dbutils.shutdown()