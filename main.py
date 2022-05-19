import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, requests, cv2, numpy, pyodbc, sys,os,subprocess
from wsgiref import headers
import importlib as il
import mysql.connector

def connectSQLDatabase():
    server = 'harshita.database.windows.net'
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
        #mydb = mysql.connector.connect(server='harshita.database.windows.net',username= 'Harshi',password= 'Anjali123',database='society')

        #mycursor = mydb.cursor()

    def createGroup(self, wing, name):

        params = urllib.parse.urlencode({})

        body = {
            "name" :'{}'.format(name),
        }

        try:
            self.conn.request("PUT","/face/v1.0/persongroups/"+ wing +"?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("Group Created")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    def addperson(self, name, targetGroup):

        params = urllib.parse.urlencode({})

        body = {
            "name": '{}'.format(name),
        }

        try:
            self.conn.request("POST","/face/v1.0" + targetGroup + "/persons?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("Person Added: ", name)
        
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno,e.strerror))
    def addFace(self, targetName, targetGroup, URL):


    #returns a json list of people in the group
    def listPersonsInGroup(self, targetGroup):

    #to train the group
    def trainGroup(self, targetGroup):

    # Returns faceId to be fed into identifyFace, returns -1(integer) if no face found
    def detectFace(self, imgData):

    # To identify face returns name of the person 
    def identifyFace(self, faceId, targetGroup):  

    def addPersonToDatabase(self, name, flat, wing)

    # to take entries
    def takeEntries():

    def getLastPersonScanned(self):
        return self.personScanned 

    def getPersonDetails(self, name):

    def wipeEntryLog(self, timetablekey):

    def TrainInit(self):

    def DatabaseInit(self):

    def getPersonJson(self):

    def main(self, flag, sub):


if __name__ == "__main__":
    app = FaceID()
    #flag=1

    app.main(flag,sub)  
    #app.main() 
