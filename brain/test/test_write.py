import os

def ahoj():
    path = '/home/pi/stream/jpg0a'
    print(path)

    txt = 'as\n'*10
    with open(path, 'wb') as f:
        f.write(bytes(txt, 'utf-8'))


ahoj()
