import datetime
from struct import unpack

from main.save_data import mysql_con
from main.utils import time_to_datetime


def insert_pdalert(BoardCardNo, ChannelNo, real_time, pd_data):
    select_sql = '''select DataID,EquipmentID,SensorID,Datatime 
                                    from tb_rawdata
                                    where EquipmentID=%s and SensorID=%s and Datatime=%s'''
    id = mysql_con.op_select(select_sql, (BoardCardNo, ChannelNo, real_time))[0]['DataID']
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
    mysql_con.op_insert(sql1,
                        [id, BoardCardNo, ChannelNo, real_time, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, pd_data])


# mysql_con.closeall()


def unpack_data(data, save_times):
    # print(data)
    if data[:4] == b'\xe0\xe9\xe0\xe9':
        pd_header = unpack('<4s2sbhibbbib', data[:21])
        if not data[6]:
            BoardCardNo = pd_header[4]
            ChannelNo = pd_header[5]
            PDFlag = pd_header[6]
            DataTime = pd_header[8]
            real_time = time_to_datetime(DataTime)
            pd_data = data[21:]
            sql = 'insert into tb_rawdata (EquipmentID,SensorID,Datatime,Content) value (%s,%s,%s,%s)'

            mysql_con.op_insert(sql, [BoardCardNo, ChannelNo, real_time, pd_data])
            if PDFlag:
                save_pd = save_times[str(BoardCardNo)][ChannelNo - 1]
                cha_time = real_time - save_pd['last_pd_time']
                if cha_time.days > 0 or (cha_time.days == 0 and cha_time.seconds > 900):
                    insert_pdalert(BoardCardNo, ChannelNo, real_time, pd_data)
                    save_pd['now_times'] = 1
                    save_pd['last_pd_time'] = real_time
                else:
                    if save_pd['now_times'] < 9:
                        insert_pdalert(BoardCardNo, ChannelNo, real_time, pd_data)
                        save_pd['now_times'] += 1
                    elif save_pd['now_times'] == 9:
                        print(save_pd)
                        print(real_time)


def rec_consumer():
    r = ''
    Device_list = mysql_con.op_select('select equipmentid from tb_device;')
    save_time_list = {}
    for i in Device_list:
        save_time_list[str(i['equipmentid'])] = [
            {'last_pd_time': datetime.datetime(2018, 1, 1, 0, 0, 0), 'now_times': 0} for i in
            range(10)]
    while True:
        data = yield r
        if not data:
            return
        try:
            start_time = datetime.datetime.now()
            unpack_data(data, save_time_list)
            # print(data)
            print(datetime.datetime.now() - start_time)
            r = 'success'
        except:
            r = 'error'
