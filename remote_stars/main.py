import numpy as np
import matplotlib.pyplot as plt
import socket

host = '84.237.21.36'
port = 5152

def get_points(image, p):
    pos1 = np.unravel_index(np.argmax(image), image.shape)
    temp = image.copy()
    y, x = pos1
    temp[max(0, y - p): y + p, max(0, x - p): x + p] = 0
    pos2 = np.unravel_index(np.argmax(temp), temp.shape)
    return pos1, pos2

def recvall(sock, nbytes: int) -> bytearray | None:
    data = bytearray()
    while len(data) < nbytes:
        packet = sock.recv(nbytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

plt.ion()
plt.figure()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    sock.connect((host, port))
    sock.send(b'124ras1')
    print(sock.recv(10))
    beat = b'nope'

    while beat != b'yep':
        sock.send(b'get')
        bts = recvall(sock, 40_002)

        im = np.frombuffer(bts[2:], dtype='uint8').reshape(bts[0], bts[1])

        pos1, pos2 = get_points(im, 15)
        dist = ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5
        sock.send(f'{round(dist, 1)}'.encode())
        print(sock.recv(10))

        plt.clf()
        plt.imshow(im)
        plt.show()
        plt.pause(2)

        sock.send(b'beat')
        beat = sock.recv(10)