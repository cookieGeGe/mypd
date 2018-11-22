from struct import pack

import datetime

c = pack('iiis', 4, 4, 4, '4'.encode())
print(len(c))
a = b'\xe0\xe9\xe0\xe9\x11\x11'
print(len(a))
print(a[4:])
print(a[:4])

b = datetime.datetime(2018, 1, 1, 0, 0, 0)
print(b)
d = datetime.datetime(2018, 1, 1, 0, 0, 20)
f = d-b
print(f)
