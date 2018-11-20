from struct import unpack

import pymysql

from main.save_data import mysql_con
from main.utils import time_to_datetime


def unpack_data(data):
    if data[:4] == b'\xe0\xe9\xe0\xe9':
        pd_header = unpack('<4s2sbhibbbib', data[:21])
        if not data[6]:
            # Header = pd_header[0]
            # SLength = pd_header[3]
            BoardCardNo = pd_header[4]
            ChannelNo = pd_header[5]
            PDFlag = pd_header[6]
            DataTime = pd_header[8]
            real_time = time_to_datetime(DataTime)
            pd_data = data[21:]
            # db = mysql_con.getmysqlconn()
            sql = 'insert into tb_rawdata (EquipmentID,SensorID,Datatime,Content) value (%s,%s,%s,%s)'

            mysql_con.op_insert(sql, [BoardCardNo, ChannelNo, real_time, pd_data])
            if PDFlag:
                select_sql = '''select DataID,EquipmentID,SensorID,Datatime 
                                from tb_rawdata
                                where EquipmentID=%s and SensorID=%s and Datatime=%s'''
                id = mysql_con.op_select(select_sql, (BoardCardNo, ChannelNo, real_time))['DataID']
                sql1 = '''
                insert into tb_pdalert(DataID,
                EquipmentID,
                SensorID,
                Datatime,
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
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                '''
                # mysql_con.op_insert(sql1,
                #                     [id, BoardCardNo, ChannelNo, real_time, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, pd_data])
            # mysql_con.closeall()


def rec_consumer():
    r = ''
    while True:
        data = yield r
        if not data:
            return

        unpack_data(data)
