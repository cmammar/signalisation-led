from flask import Flask, escape, request
from astar import *
import socket
from json import dumps
from time import sleep
import threading

shops = fileToList('shops.json')
bandes = fileToList('bandes.json')
servers = fileToList('servers.json')
shopsObj = createShopObjects(deepcopy(shops))
app = Flask(__name__)

@app.route('/')
def home():
    return {'message': 'api signalisation'}

def my_thread(src, dest, speed, color):
    path = calcPath(src, dest)
    print(path)
    for i in range(1, len(path)):
        print(path[i - 1]+" => "+path[i])
        start = path[i - 1]
        end = path[i]
        bandeId = findBandeFromPath(shopsObj, bandes, start, end)
        print("band id: "+str(bandeId))
        ip, port = getServerFromBand(servers, bandeId)
        print(ip)
        startIndex, endIndex = getFirstLastLed(shopsObj, bandes, start, end)
        datas = {'bandeId': bandeId, 'src': start, 'dest': end, 'startIndex': startIndex, 'endIndex': endIndex, 'speed': speed, 'color': color}
        datas = dumps(datas)
        print(datas)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(datas.encode(), (ip, port))
        sleep(400*speed/1000*abs(endIndex-startIndex))
        #le faire attendre en fc de la speed et de la distance parcourue

@app.route('/destination')
def destination():
    src = request.args.get('src')
    dest = request.args.get('dest')
    speed = float(request.args.get('speed'))
    color = request.args.get('color')
    x = threading.Thread(target=my_thread, args=(src, dest, speed, color))
    x.start()
    # speed = int(request.args.get('speed'))
    # color = request.args.get('color')
    # path = calcPath(src, dest)
    # print(path)
    # for i in range(1, len(path)):
    #     print(path[i - 1]+" => "+path[i])
    #     start = path[i - 1]
    #     end = path[i]
    #     bandeId = findBandeFromPath(shopsObj, bandes, start, end)
    #     print("band id: "+str(bandeId))
    #     ip, port = getServerFromBand(servers, bandeId)
    #     print(ip)
    #     startIndex, endIndex = getFirstLastLed(shopsObj, bandes, start, end)
    #     datas = {'bandeId': bandeId, 'src': start, 'dest': end, 'startIndex': startIndex, 'endIndex': endIndex, 'speed': speed, 'color': color}
    #     datas = dumps(datas)
    #     print(datas)
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     sock.sendto(datas.encode(), (ip, port))
        # sleep(1.5)

    # UDP_IP = "127.0.0.1"
    # UDP_PORT = 5005
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.sendto(" ".join(path).encode(), (UDP_IP, UDP_PORT))
    return src+" => "+dest