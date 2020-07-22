from script_cred import UserDBA
from script_cred import PasswdDBA
from script_cred import HostDBA
from script_cred import DBA

import pymysql
from sqlalchemy import create_engine

#Datenbank einloggen

class ConnectMySQL:
    connection_dba = pymysql.connect(host=HostDBA.hostname,
        user=UserDBA.name,
        password=PasswdDBA.secret,
        db=DBA.database)

    db_data='mysql+mysqldb://'+'{}'.format(UserDBA.name)+':'+'{}'.format(PasswdDBA.secret)+'@'+'{}'.format(HostDBA.hostname)+':3306/'+'{}'.format(DBA.database)+'?charset=utf8mb4'
    
    engine=create_engine(db_data)
    #get_it=connection_dba.cursor()

#oo = ConnectMySQL()
#print(oo.engine)
