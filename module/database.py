import firebase_admin as firebase
from firebase_admin import firestore
import flask

try:
    import tool as tool
except ModuleNotFoundError:
    import module.tool as tool

class DB:

    __slots__=('DataBase')

    def __init__(self)->None:
        # 登入Firebase
        try:
            Cred=firebase.credentials.Certificate(tool.GetConfigData('Firebase','JsonFilePath'))
            firebase.initialize_app(Cred)
            # 使用Firebase的firestore
            self.DataBase=firestore.client()
        except:
            print('[database-ERROR] 登入Firebase失敗，請檢查config.ini key設定路徑')
            self.DataBase=''


    def CUTravelInfo(self,No,Title,ImageName,Content,StartTime,EndTime,Limit):
        if self.DataBase=='':
            print('[database-ERROR] 你尚未登入')
            return
        else:
            Data={
                'Title':Title,
                'ImageName':ImageName,
                'Content':Content,
                'StartTime':StartTime,
                'EndTime':EndTime,
                'Limit':Limit
            }
            for Docs in self.DataBase.collection('TravelInfo').get():
                if Docs.id==No:
                    if self.DataBase.collection('TravelInfo').document(No).get().to_dict()['Title']!=Title:
                        print('[database-ERROR] ID衝突')
                        return
                    else: #同ID 同Title->更新
                        self.DataBase.collection('TravelInfo').document(No).update(Data)
                        print('[database-INFO] 更新完成')
                        return
            self.DataBase.collection('TravelInfo').document(No).set(Data)
            print('[database-INFO] 新增完成')
            return
        

    def FormDataGet(self,Type):
        if Type=='CU':
            No=flask.request.values.get('No')
            Title=flask.request.values.get('Title')
            ImageName=flask.request.values.get('ImageName')
            Content=flask.request.values.get('Content')
            StartTime=flask.request.values.get('StartTime')
            EndTime=flask.request.values.get('EndTime')
            Limit=flask.request.values.get('Limit')
            self.CUTravelInfo(No,Title,ImageName,Content,StartTime,EndTime,Limit)
        return
# Debug 
if __name__=='__main__': 
    Test=DB()
    No=input('Enter No:')
    Title=input('Enter Title:')
    ImageName=input('ImageName:')
    Content=input('Content:')
    StartTime=input('StartTime(Format:yyyy-mm-dd ex:2022-06-04)')
    EndTime=input('EndTime(Format:yyyy-mm-dd ex:2022-06-04)')
    Limit=input('Limit:')
    Test.CUTravelInfo(No,Title,ImageName,Content,StartTime,EndTime,Limit)