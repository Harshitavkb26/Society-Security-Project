import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, requests, cv2, numpy, pyodbc, sys,os,subprocess
from urllib import response
import cv2
from httplib2 import Response
import importlib as il
import mysql.connector
flag=1
flag1=True
wg="winga"
def connectSQLDatabase():
    server = 'harshita.database.windows.net'
    database = 'society'
    username = 'Harshi'
    password = 'Anjali123'
    driver= "{ODBC Driver 17 for SQL Server}"
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

cursor = connectSQLDatabase()
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')



class FaceID(object):
    """The FaceID class"""

    conn = http.client.HTTPSConnection('buildfaceapi.cognitiveservices.azure.com')
    # cam = cv2.CascadeClassifier('rtsp://admin:admin@123@192.168.43.200/1')
    #may be have to change the values
    # cam = cv2.VideoCapture(1)
    # cam.set(cv2.CAP_PROP_FPS, 0.1)
    personScanned = ''

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'c1e050016f4241a28aefb095318529e8',
    }

    def fetchSQLData(self):
        #mydb = mysql.connector.connect(server='harshita.database.windows.net',username= 'Harshi',password= 'Anjali123',database='society')

        #mycursor = mydb.cursor()

        cursor.execute("SELECT * FROM [dbo].[societymembers]")
        result = cursor.fetchall()

        for i in result:
            print(i)
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
            # print(data)
            print("Group Created")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    def addPerson(self, name, targetGroup):

        params = urllib.parse.urlencode({})

        body = {
            "name": '{}'.format(name),
        }

        try:
            self.conn.request("POST", "/face/v1.0/persongroups/" + targetGroup + "/persons?%s" % params, json.dumps(body), self.headers)
            response = self.conn.getresponse()
            data = response.read()
            # print(data)
            print("Person Added: ", name)
        
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno,e.strerror))
        

    def addFace(self, targetName, targetGroup, URL):

        # WARNING : going off the assumption that there are no duplicate names
        listOfPersons = json.loads(self.listPersonsInGroup(targetGroup))
        personId = ""
        for person in listOfPersons:
            # print(person)
            if person["name"] == targetName :
               
                personId = person["personId"]
                # print("PersonId added")
                break

        
        params = urllib.parse.urlencode({})

        body = {
            "url" : '{}'.format(URL)
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
            self.conn.request("GET","/face/v1.0/persongroups/" + targetGroup + "/persons?%s" % params, "{body}", self.headers)
            response = self.conn.getresponse()
            data = response.read()
            # print(data)
            return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    #to train the group
    def trainGroup(self, targetGroup):

        params = urllib.parse.urlencode({})

        try:
            self.conn.request("POST","/face/v1.0/persongroups/" + targetGroup + "/train?%s" % params, "{body}", self.headers)
            response = self.conn.getresponse()
            data = response.read()
            print("Group Trained")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        

    # Returns faceId to be fed into identifyFace, returns -1(integer) if no face found
    def detectFace(self, imgData):

         detectHeaders = {'Content-Type': 'application/octet-stream',
                   'Ocp-Apim-Subscription-Key': '88c2b7ffcd274fa7ab53b70ec20f7b54'}

         url = 'https://buildfaceapi.cognitiveservices.azure.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false'
    
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
            # print(response)
            

            data = json.loads(response.read())
            # print(data)

            if not data or not data[0]["candidates"]:
                raise IndexError()

            candidatePersonId = data[0]["candidates"][0]["personId"]
            listOfPersons = json.loads(self.listPersonsInGroup(targetGroup))
            for person in listOfPersons:
                if person["personId"] == candidatePersonId:
                    print("PERSON IDENTIFIED: " + person["name"])
                    return person["name"]

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
            cam = cv2.VideoCapture(1)
            while True:
                
                ret, img = cam.read()

                # img = cv2.resize(img, (1000, 500))
                cv2.imshow('frame', img)
                imgData = cv2.imencode(".jpg",img)[1].tobytes()
               

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                i=i+1
                if i % 100 == 0:

                    detectedFaceId = self.detectFace(imgData)
                    if detectedFaceId != -1:
                        # print(detectedFaceId)
                        known = 0
                        
                        person = self.identifyFace(detectedFaceId, wing)
                        # print(person)
                        if not person:
                            randperson = self.identifyFace(detectedFaceId, "knownmembers")
                        if not person :
                            if randperson :
                                known = 1
                                randperson_name , randperson_desd = randperson.split("_")
                        if person :
                            known = 2
                            person_name , person_flatnumber = person.split("_")
                            
                        
                        if known == 1 :
                            checkQuery = "SELECT * FROM societymembers WHERE (flatnumber = '" + randperson_desd + "' AND name = '" + randperson_name  + "' AND wing = '" + 'knownMembers' + "');"
                            cursor.execute(checkQuery)
                            data = cursor.fetchone()
                            print('Adding person into known members entry table')
                            addQuery = "INSERT INTO knownmembers (flatnumber, name , contactnumber, timestamp) VALUES ('" + randperson_desd + "', '" + randperson_name + "', '" + data[3] + "', '" + '123' + "');"


                        if known == 2 :
                            checkPresentQuery = "SELECT * FROM societymembers WHERE (flatnumber = '" + person_flatnumber + "' AND name = '" + person_name  + "' AND wing = '" + wing + "');"
                            cursor.execute(checkPresentQuery)
                            data = cursor.fetchone()
                            print('Adding person into wing entry table')
                            if wing =="winga":
                                addQuery = "INSERT INTO wingA (flatnumber, name , contactnumber, timestamp) VALUES ('" + person_flatnumber + "', '" + person_name + "', '" + data[3] + "', '" + '123' + "');"
                            elif wing =="wingb":
                                addQuery = "INSERT INTO wingB (flatnumber, name , contactnumber, timestamp) VALUES ('" + person_flatnumber + "', '" + person_name + "', '" + data[3] + "', '" + '123' + "');"
                            elif wing=="wingc" :
                                addQuery = "INSERT INTO wingC (flatnumber, name , contactnumber, timestamp) VALUES ('" + person_flatnumber + "', '" + person_name + "', '" + data[3] + "', '" + '123' + "');"
                            cursor.execute(addQuery)
                            cursor.commit()
                            

            if flag==0 :

                cam.release()
                cv2.destroyAllWindows()
        except KeyboardInterrupt:
            self.conn.close()
        print("takeEntries runs successfully")


                            
                            


    def getLastPersonScanned(self):
        return self.personScanned 

    def getPersonDetails(self, name):
        return 1

    def wipeEntryLog(self, timetablekey):
        return 1

    def TrainInit(self):

        self.createGroup("winga","Wing A")
        self.createGroup("wingb","Wing B")
        self.createGroup("wingc","Wing C")
        self.createGroup("knownmembers","Routine People")

        self.addPerson("HarshitaVerma_1","winga")
        self.addPerson("NikitaVerma_2","wingb")
        self.addPerson("DakshBerry_1","wingc")
        self.addPerson("AbhishekArya_Milkman","knownmembers")

        self.addFace("DakshBerry_1","wingc","https://github.com/dakshberry121/temp-pics/blob/master/1.jpg?raw=true")
        self.addFace("DakshBerry_1","wingc","https://github.com/dakshberry121/temp-pics/blob/master/2.jpg?raw=true")
        self.addFace("DakshBerry_1","wingc","https://github.com/dakshberry121/temp-pics/blob/master/3.jpg?raw=true")
        self.addFace("DakshBerry_1","wingc","https://github.com/dakshberry121/temp-pics/blob/master/4.jpg?raw=true")
        self.addFace("HarshitaVerma_1","winga","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h2.jpg?raw=true")
        self.addFace("HarshitaVerma_1","winga","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h3.jpg?raw=true")
        self.addFace("HarshitaVerma_1","winga","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h4.jpg?raw=true")
        self.addFace("HarshitaVerma_1","winga","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h5.jpg?raw=true")
        self.addFace("HarshitaVerma_1","winga","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h6.jpg?raw=true")
        self.addFace("HarshitaVerma_1","winga","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/harshita/h7.jpg?raw=true")
        self.addFace("NikitaVerma_2","wingb","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n1.jpg?raw=true")
        self.addFace("NikitaVerma_2","wingb","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n2.jpg?raw=true")
        self.addFace("NikitaVerma_2","wingb","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n3.jpg?raw=true")
        self.addFace("NikitaVerma_2","wingb","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n4.jpg?raw=true")
        self.addFace("NikitaVerma_2","wingb","https://github.com/Harshitavkb26/Society-Security-Project/blob/main/pics/Nikita/n5.jpg?raw=true")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/1.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/2.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/3.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/4.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/5.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/6.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/7.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/8.JPG")
        self.addFace("AbhishekArya_Milkman", "knownmembers", "https://raw.githubusercontent.com/abhishek4s/pics/master/9.JPG")
        

        self.trainGroup("winga")
        self.trainGroup("wingb")
        self.trainGroup("wingc")
        self.trainGroup("knownmembers")
        time.sleep(2) # Give a second to train database

        print("Traininit runs successfully")
        



    def DatabaseInit(self):
        self.addPersonToDatabase("HarshitaVerma","1","winga","7225051539")
        self.addPersonToDatabase("NikitaVerma","2","wingb","9770350519")
        self.addPersonToDatabase("DakshBerry","1","wingc","8959673327")

    def getPersonJson(self):
        return 1

    def main(self, flag, wg):
        # self.TrainInit() # Init only once
        # self.DatabaseInit() # Also init only once

        print('--------------------------------')
        # self.fetchSQLData()
        if flag ==1 :
            if wg=="winga":
                self.takeEntries("winga",flag)
            elif wg=="wingb":
                self.takeEntries("wingb",flag)
            elif wg=="wingc":
                self.takeEntries("wingc",flag)
            elif wg=="knownmembers":
                self.takeEntries("knownmembers",flag)

        # else:
        #     # self.cam.release()

if __name__ == "__main__":
    app = FaceID()
    # flag=1

    app.main(flag,wg)  
    #app.main() 
