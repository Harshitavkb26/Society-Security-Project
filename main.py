import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, requests, cv2, numpy, pyodbc, sys,os,subprocess
from wsgiref import headers
import importlib as il
import mysql.connector

def connectSQLDatabase():
    server = 'societymembers.database.windows.net'
    database = 'society'
    username = 'Harshi'
    password = 'Anjali123'
    driver= "{SQL Server}"
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

cursor = connectSQLDatabase()
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

class FaceID(object):
    """The FaceID class"""

    conn = http.client.HTTPConnection('centralindia.api.cognitive.microsoft.com')
    cam = cv2.CascadeClassifier('rtsp://admin:admin@123@192.168.43.200/1')
    #may be have to change the values

    personScanned = ''

    headers = {
        #Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '88c2b7ffcd274fa7ab53b70ec20f7b54',
    }

    def fetchSQLData(self):
