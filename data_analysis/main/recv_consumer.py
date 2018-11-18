from struct import unpack


def unpack_data(data):
    pass


def rec_consumer():
    r = ''
    while True:
        data = yield r
        if not data:
            return
        print(data)