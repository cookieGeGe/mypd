from struct import unpack

import pymysql

from main.save_data import mysql_con


def unpack_data(data):
    if data[:4] == b'\xe0\xe9\xe0\xe9':
        if data[6]:
            # Header,Cmd,Rcode,SLength,BoardCardNo,ChannelNo
            pd_header = unpack('4s2schicccii',data[:24])
            Header = pd_header[0]
            SLength = pd_header[3]
            BoardCardNo = pd_header[4]
            ChannelNo = pd_header[5]
            PDFlag = pd_header[6]
            DataTime = pd_header[8]
            pd_data = data[24:3274]
            db = mysql_con.getmysqlconn()
            sql = '''
            insert into tb_rawdata (EquipmentID,SensorID,Datatime,Content) 
            value (%d,%d,%s, %s)
            ''' % (BoardCardNo,ChannelNo,DataTime,pymysql.Binary(pd_data))
            db.op_insert(sql)
            if PDFlag:

                select_sql = '''select DataID,EquipmentID,SensorID,Datatime 
                                from tb_rawdata
                                where EquipmentID=%d and SensorID=%d and Datatime=%s''' % (BoardCardNo,ChannelNo,DataTime)
                id = db.op_select(select_sql)[0]
                sql1 = '''
                insert into tb_pdalert(DataID,
                EquipmentID,
                SensorID,
                Datatime,,
                AlmLev,
                DschType,
                AppPaDsch,
                AcuPaDsch,
                AvDsch,
                MaxDsch,
                DschCnt,
                PriHarRte,
                SecHarRte,
                SmpProd,
                Content) value 
                (%d,%d,%d,%s,0,10,0,0,0,0,0,0,0,0,%s)
                ''' % (id, BoardCardNo,ChannelNo,DataTime,pymysql.Binary(pd_data))
                db.op_insert(sql1)
            db.closeall()



def rec_consumer():
    r = ''
    while True:
        data = yield r
        if not data:
            return
        unpack_data(data)