################################### time ####################################
import time
import numpy as np
import datetime
import calendar

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
