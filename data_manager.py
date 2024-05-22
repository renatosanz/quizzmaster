from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import  OperationFailure
import os,pickle,random

class Data_Manager():
    def __init__(self):
        self.problems_data = None
        self.backup_file = "data.pickle" 
        self.username = None
        self.psw = None
        self.topic = None
        self.topic_list = ["math","biology","history","art"]

    def requestData(self):
        uri = "mongodb+srv://"+self.username+":"+self.psw+"@cluster0.mic475y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            database = client['GTN_DATABASE']
            collection = database[self.topic]
            self.problems_data = list(collection.find())
            for doc in self.problems_data:
                print(doc)
        except Exception as e:
            print(e)
        finally:
            print(len(self.problems_data))
            print("Disconection!")
            self.saveLocalData()

    def chargeLocalData(self):
        if os.path.isfile(self.backup_file):
            with open(self.backup_file, 'rb') as file:
                self.problems_data = pickle.load(file)
                print("data charged")
        if self.problems_data == None:
            self.requestData()
    
    def saveLocalData(self):
        with open(self.backup_file, 'wb') as file:
            pickle.dump(self.problems_data, file)
            print("data saved")
    
    def getQuestions(self,n):
        if len(self.problems_data) < n:
            return self.problems_data
        return random.sample(self.problems_data,n)
    
    def requestLogin(self,username,psw,topic):
        res = {"label":"","data":None}
        if username == "" or  psw == "" or topic == "":
            res["label"] = "Sign in data is empty!"
            res["data"] = False
            return res
        
        uri = "mongodb+srv://"+username+":"+psw+"@cluster0.mic475y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        response_auth = self.authenticate_to_mongodb(uri)
        if response_auth:
            self.username = username
            self.psw = psw
            res["label"] = "Sign in Succesfull"
            res["data"] = True
        else:
            res["label"] = "User or password incorrect!"
            res["data"] = False
        return res
    
    def authenticate_to_mongodb(self,uri):
        try:
            # Crear una instancia del cliente MongoDB
            client = MongoClient(uri)
            
            # Probar la conexión y autenticación
            client.admin.command('ismaster')
            print("Authentication successful!")
            return client
        except ( OperationFailure) as e:
            print(f"An error occurred: {e}")
            return None
    def setTopic(self,sender,app_data,user_data):
        self.topic = app_data
        print(self.topic)