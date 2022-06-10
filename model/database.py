import random

import firebase_admin as firebase
from firebase_admin import firestore


try:
    import tool as tool
except ModuleNotFoundError:
    import model.tool as tool

class DB:


    def __init__(self) -> None:
        # 登入Firebase
        try:
            Cred=firebase.credentials.Certificate(tool.GetConfigData('Firebase','JsonFilePath'))
            firebase.initialize_app(Cred)
            # 使用Firebase的firestore
            self.DataBase=DataBase=firestore.client()
        except:
            print('[ERROR] 登入Firebase失敗，請檢查config.ini key設定路徑')
            self.DataBase=''


    def NewTravelInfo(self,Title,ImageName,Text,StartTime,EndTime,Limit):
        if self.DataBase=='':
            print('[ERROR] 你尚未登入')
            return
        else:
            Data={
                'No':'',
                'Title':Title,
                'ImageName':ImageName,
                'Text':Text,
                'StartTime':StartTime,
                'EndTime':EndTime,
                'Limit':Limit
            }
            self.DataBase.collection('TravelInfo').document(Title).set(Data)
            print('Well Done!')
            return
    

# Debug 
if __name__=='__main__': 
    Test=DB()
    Test.NewTravelInfo('TESTTitle2','TEST2','TESTTEXT','2022-06-20T14:00','2022-06-22T22:00','20')