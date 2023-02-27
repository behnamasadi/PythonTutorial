################################### time ####################################
import time
import datetime
import calendar
import numpy as np


# Unix system, January 1, 1970, 00:00:00
print(time.time())
print(time.time() / (24*365*3600))
print(time.ctime())
print(time.localtime(24*3600*365))
print(time.gmtime(24*3600*365))

t = (2018, 12, 28, 8, 44, 4, 4, 362, 0)
print(time.mktime(t))
named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
print(time_string)

microsecond_since_epoch = np.int64(
    datetime.datetime.now().timestamp() * 1000_000)


epoch = datetime.datetime.utcfromtimestamp(0)
print(calendar.timegm(epoch.timetuple()))

i = 0
while True:
    time.sleep(1)
    i += 1
    print(i)
    
    
t = datetime.datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
print(calendar.timegm(t.timetuple()))



epoch = datetime.datetime.utcfromtimestamp(0)
print(calendar.timegm(epoch.timetuple()) )


milliseconds_since_epoch =datetime.datetime.now().timestamp() * 1000

print(milliseconds_since_epoch)


microsecond_since_epoch = np.int64(datetime.datetime.now().timestamp() * 1000_000)

print(microsecond_since_epoch)




print(calendar.timegm(time.gmtime()))

print("1403636579758555392 in nano second: ",datetime.datetime.fromtimestamp(1403636579758555392/1000000000))

print("1675701249184511000 in nano second: ",datetime.datetime.fromtimestamp(1675701249184511000/1000000000))



t0=np.int64(datetime.datetime.now().timestamp() * 1000_000)
time.sleep(2.4)
t1=np.int64(datetime.datetime.now().timestamp() * 1000_000)
print(t1-t0)    
