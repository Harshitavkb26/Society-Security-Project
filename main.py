import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, requests, cv2, numpy, pyodbc, sys,os,subprocess
from urllib import response
from httplib2 import Response
import importlib as il
import mysql.connector
flag=1
flag1=True
wg="A"
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
    # cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FPS, 0.1)

    personScanned = ''

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '88c2b7ffcd274fa7ab53b70ec20f7b54',
    }

    def fetchSQLData(self):
        #mydb = mysql.connector.connect(server='harshita.database.windows.net',username= 'Harshi',password= 'Anjali123',database='society')

        #mycursor = mydb.cursor()

        cursor.execute()
        result = cursor.fetchall()

        for i in result:
        return result

    def createGroup(self, groupId, groupName):

        params = urllib.parse.urlencode({})

        body = {
            "name" : '{}'.format(groupName),
        }

        try:
            self.conn.request("PUT","/face/v1.0/persongroups/"+ groupId +"?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("Group Created")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    def addPerson(self, name, flatnumber, targetGroup):

        params = urllib.parse.urlencode({})

        body = {
            "name": '{}'.format(name),
            "flatnumber": '{}'.format(flatnumber),
        }

        try:
            self.conn.request("POST","/face/v1.0" + targetGroup + "/persons?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("Person Added: ", name)
            print("Flat Added: ", flatnumber)
        
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno,e.strerror))

    def addFace(self, targetName, flatnumber, targetGroup, URL):

        # WARNING : going off the assumption that there are no duplicate names
        listOfPersons = json.loads(self.listPersonsInGroup(targetGroup))
        personId = ""
        for person in listOfPersons:
            if person["name"] == targetName and person["flatnumber"] == flatnumber :
                personId = person["personId"]
                break
        
        params = urllib.parse.urlencode({})

        body = {
            "url" : '{}'.formate(URL)
        }

        try:
            self.conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/persons/" + personId + "/persistedFaces?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("Face Added To: ", targetName)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))



    #returns a json list of people in the group
    def listPersonsInGroup(self, targetGroup):

        params = urllib.parse.urlencode({})

        try:
            self.conn.request("GET","/face/v1.0/persongroups" + targetGroup + "/persons?%s" % params, "{body}", self.headers)
            response = self.conn.getresponse()
            data = response.read()
            return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    #to train the group
    def trainGroup(self, targetGroup):

        params = urllib.parse.urlencode({})

        try:
            self.conn.request("POST","face/v1.0/persongroups" + targetGroup + "/train?%s" % params, "{body}", self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("Group Trained")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        

    # Returns faceId to be fed into identifyFace, returns -1(integer) if no face found
    def detectFace(self, imgData):

         detectHeaders = {'Content-Type': 'application/octet-stream',
                   'Ocp-Apim-Subscription-Key': '88c2b7ffcd274fa7ab53b70ec20f7b54'}

         url = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0/detect'
    
         params = urllib.parse.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
         })

         try:
        
            response = requests.post(url, headers=detectHeaders, data=imgData)
            return response.json()[0]["faceId"]
         except IndexError:
            print("NO FACE DETECTED")
            return -1
         except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # To identify face returns name of the person 
    def identifyFace(self, faceId, targetGroup): 
        params = urllib.parse.urlencode({})

        body = {
            'faceIds' : [faceId],
            'personGroupId' : targetGroup
        }

        try:
            self.conn.request("POST", "/face/v1.0/identify?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = json.loads(response.read())

            if not data or not data[0]["candidates"]:
                raise IndexError()

            candidatePersonId = data[0]["candidates"][0]["personId"]
            listOfPersons = json.loads(self.listPersonsInGroup(targetGroup))
            for person in listOfPersons:
                if person["personId"] == candidatePersonId:
                    print("PERSON IDENTIFIED: " + person["name"])
                    print("persons flat identify: " + person["flatnumber"])
                    return [person["name"], person["flatnumber"]]

        except IndexError:
            print("***** Idk something went wrong *****")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror)) 

    def addPersonToDatabase(self, name, flat, wing, contactnumber):
        query = "INSERT INTO societymembers (flatnumber, name, wing, contactnumber) VALUES ('" + flat + "', '" + name + "', '" + wing + "', '" + contactnumber + "');"
        cursor.execute(query)
        cursor.commit()

    # to take entries
    def takeEntries(self, wing, flag):

        i=0
        try:
            while True:
                # cam = cv2.VideoCapture(0)
                s, img = self.cam.read()

                img = cv2.resize(img, (1000, 500))
                cv2.imshow('frame', img)
                imgData = cv2.imencode(".jpg",img)[1].tostring()

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                i=i+1;
                if i % 10000 == 0:

                    detectedFaceId = self.detectFace(imgData)
                    if detectedFaceId != -1:
                        known = 0
                        person = self.identifyFace(detectedFaceId, wing)
                        randperson = self.identifyFace(detectedFaceId, "knownMembers")
                        if not person :
                            if randperson :
                                known = 1
                        if person :
                            known = 2
                        
                        if known == 1 :
                            checkQuery = "SELECT * FROM societymembers WHERE (flatnumber = '" + person[1] + "' AND name = '" + person[0]  + "' AND wing = '" + "knownMembers" + "');"
                            cursor.execute(checkQuery)
                            data = cursor.fetchone()
                            print('Adding person into wing entry table')
                            addQuery = "INSERT INTO knownmembers" + wing + " (flatnumber, name , contactnumber, timestamp) VALUES ('" + person[1] + "', '" + person[0]  + "', '" + data["contactnumber"] + "');"


                        if known == 2 :
                            checkPresentQuery = "SELECT * FROM societymembers WHERE (flatnumber = '" + person[1] + "' AND name = '" + person[0]  + "' AND wing = '" + wing + "');"
                            cursor.execute(checkPresentQuery)
                            data = cursor.fetchone()
                            print('Adding person into wing entry table')
                            addQuery = "INSERT INTO wing" + wing + " (flatnumber, name , contactnumber, timestamp) VALUES ('" + person[1] + "', '" + person[0]  + "', '" + data["contactnumber"] + "');"


                            
                            


    def getLastPersonScanned(self):
        return self.personScanned 

    def getPersonDetails(self, name):

    def wipeEntryLog(self, timetablekey):

    def TrainInit(self):

        self.createGroup("A","Wing A")
        self.createGroup("B","Wing B")
        self.createGroup("C","Wing C")
        self.createGroup("Random","Routine People")

        self.addPerson("harshita","1","A")
        self.addPerson("Nikita","2","B")

        self.addFace("harshita","1","A","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h2.jpg?raw=true")
        self.addFace("harshita","1","A","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h3.jpg?raw=true")
        self.addFace("harshita","1","A","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h4.jpg?raw=true")
        self.addFace("harshita","1","A","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h5.jpg?raw=true")
        self.addFace("harshita","1","A","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h6.jpg?raw=true")
        self.addFace("harshita","1","A","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h7.jpg?raw=true")
        self.addFace("Nikita","2","B","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n1.jpg?raw=true")
        self.addFace("Nikita","2","B","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n2.jpg?raw=true")
        self.addFace("Nikita","2","B","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n3.jpg?raw=true")
        self.addFace("Nikita","2","B","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n4.jpg?raw=true")
        self.addFace("Nikita","2","B","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n5.jpg?raw=true")

        self.trainGroup("A")
        self.trainGroup("B")
        self.trainGroup("C")
        self.trainGroup("knownMembers")
        time.sleep(2) # Give a second to train database
        



    def DatabaseInit(self):
        self.addPersonToDatabase("harshita","1","A","7225051539")
        self.addPersonToDatabase("Nikita","2","B","9770350519")

    def getPersonJson(self):

    def main(self, flag, wg):

        print('--------------------------------')
        #self.fetchSQLData()
        if wg=="A":
            self.takeEntries("A",flag)
        elif wg=="B":
            self.takeEntries("B",flag)
        elif wg=="C":
            self.takeEntries("C",flag)
        elif wg=="knownMembers":
            self.takeEntries("knownMembers",flag)

        else:
            self.cam.release()

if __name__ == "__main__":
    app = FaceID()
    #flag=1

    app.main(flag,sub)  
    #app.main() 
