import gpxpy
import pandas as  pd
import folium
import webview

import serial
import time
from decimal import *
from threading import Thread

def LatitudeM1():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port= 'COM4'
    ser.open()

    search = ser.readline()
    line = str(search)
    if "GPRMC" in line:
        line = line.split(",")

        #Convert Latitude from GPRMC to Decimal Grades
        a1 = Decimal(line[3])
        a2 = a1 / 100
        a3 = int(a2)
        a4 = a3 * 100
        a5 = a1 - a4
        a6 = a5 / 60
        a7 = a3 + a6
        
        return a7
    
    ser.close()

def LongitudeM1():

    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port= 'COM4'
    ser.open()

    search = ser.readline()
    line = str(search)
    if "GPRMC" in line:
        line = line.split(",")

        #Convert Longitude from GPRMC to Decimal Grades
        b1 = Decimal(line[5])
        b2 = b1 / 100
        b3 = int(b2)
        b4 = b3 * 100
        b5 = b1 - b4
        b6 = b5 / 60
        b7 = b3 + b6
        b8 = b7 * -1
        
        return b8

    ser.close()



class getData:
    c = 0
    

    #webview.create_window('m1circuit', 'index.html')
    #webview.start(http_server=True)

    a7 = LatitudeM1()
    try:
        M1LA = Decimal(a7)
        fla = open('lat.txt', 'w')
        wrla = str(M1LA)
        fla.write(wrla)
        fla.close()
    except:
        flo = open('lat.txt', 'r')
        i = flo.readline()
        M1LA = Decimal(i)
        flo.close()

    time.sleep(2)

    b8 = LongitudeM1()
    try:
        M1LO = Decimal(b8)
        pla = open('lon.txt', 'w')
        wrlo = str(M1LO)
        pla.write(wrlo)
        pla.close()
    except:
        plo = open('lon.txt')
        h = plo.readline()
        M1LO = Decimal(h)
        plo.close()

    gpx = gpxpy.parse(open('./durango.gpx'))


        
    #print('[Tracks] ' + str(len(gpx.tracks)))
    track = gpx.tracks[0]
    #print('[Segments]' + str(len(track.segments)))
    segment = track.segments[0]
    #print('[Points]' + str(len(segment.points)))

    data = []
    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude, point.elevation, point.time, segment.get_speed(point_idx)])

    columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
    df = pd.DataFrame(data, columns=columns)

    mymap = folium.Map(location=[ M1LA, M1LO], zoom_start=14)

    for coord in df[['Latitude', 'Longitude']].values:
        folium.CircleMarker(location=[coord[0],coord[1]], radius=1, color='red').add_to(mymap)

    folium.CircleMarker(location=[M1LA, M1LO],  radius= 2, color='blue').add_to(mymap)

    mymap.save('inex.html')
    time.sleep(3)

    c = c + 1

    t = str(c)

    print("[Sequence]" + t)

def destroy(window):
    time.sleep(5)
    window.destroy()

class getBrowser():  
    window = webview.create_window('Hey', 'index.html')
    webview.start(destroy, window, http_server=True)

if __name__ == '__main__':
    while True:
        Thread(target= getBrowser).start()   
        Thread(target= getData).start()
        
