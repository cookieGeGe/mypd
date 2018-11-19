from struct import pack

c = pack('iiis', 4,4,4,'4'.encode())
print(len(c))
a = b'\xe0\xe9\xe0\xe9\x11\x11'
print(len(a))
print(a[4:])
print(a[:4])