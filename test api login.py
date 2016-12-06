import socket, sys, zlib
import threading
import time

CLIENT = 'saccfft'
SERVER = 'api.anidb.net'
PORT = 9000
MYPORT = 9334
CLIENTVER = 1
PROTOVER = 3

target = (SERVER, PORT)

username = 'SACCFFT'
password = 'CheeseCakeSteak'

login = 'AUTH user=SACCFFT&pass=CheeseCakeSteak&protover=3&client=saccfft&clientver=1'

print('Starting Up')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', MYPORT))

print('All Systems Go')
# sock.sendto(login, target)
# data = sock.recv(1400)
# print (data)
# command = data.split()
# sid = command[1]
# print(sid)

sid = "HK2jX"
session = 's='+sid
# time.sleep(5) #Max 1 request every 2 seconds
#
amask = 'B0A880800E0000'

anime = 6564 #Angel Beats!!!!
getAnime = 'ANIME aid=6564&amask='+amask+'&'+session
sock.sendto(getAnime, target)
data = sock.recv(1400)
print (data)
# #time.sleep(10)
#
# print 'Testo'
#
#
#
# getAnimeDesc = 'ANIMEDESC aid=6564&part=0&'+session
# sock.sendto(getAnimeDesc, target)
# data = sock.recv(1400)
# print (data)
# time.sleep(10)
#
# random = 'RANDOMANIME type=2&'+session
# sock.sendto(random, target)
# data = sock.recv(1400)
# print (data)
# time.sleep(10)


# logout = 'LOGOUT '+session
# print(logout)
#
# sock.sendto(logout, target)
# data = sock.recv(1400)
# print (data)


print('Success!')
