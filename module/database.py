import firebase_admin as firebase
from firebase_admin import firestore
import flask

try:
    import tool as tool
except ModuleNotFoundError:
    import module.tool as tool

class DB:

    __slots__=('DataBase','Datalist')

    def __init__(self)->None:

        self.Datalist=list()
        # 登入Firebase
        try:
            Cred=firebase.credentials.Certificate(tool.GetConfigData('Firebase','JsonFilePath'))
            firebase.initialize_app(Cred)
            # 使用Firebase的firestore
            self.DataBase=firestore.client()
        except:
            print('[database-ERROR] 登入Firebase失敗，請檢查config.ini key設定路徑')
            self.DataBase=''


    def CreateUpdate(self,TargetCollection,No,Title,ImageName,Content,StartTime,EndTime,Limit):
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
            for Docs in self.DataBase.collection(TargetCollection).get():
                if Docs.id==No:
                    if self.DataBase.collection(TargetCollection).document(No).get().to_dict()['Title']!=Title:
                        print('[database-ERROR] ID衝突')
                        return
                    else: #同ID 同Title->更新
                        self.DataBase.collection(TargetCollection).document(No).update(Data)
                        print('[database-INFO] 更新完成')
                        return
            self.DataBase.collection(TargetCollection).document(No).set(Data)
            print('[database-INFO] 新增完成')
            return


    def Search(self,TargetCollection)->list:
        if self.DataBase=='':
            print('[database-ERROR] 你尚未登入')
            return
        else:
            self.Datalist=list()
            for Doc in self.DataBase.collection(TargetCollection).get():
                Data=self.DataBase.collection(TargetCollection).document(Doc.id).get().to_dict()
                # print(f'{Doc.id} {Data}')
                self.Datalist.append(Data)
            return self.Datalist
    
    def Delete(self,TargetCollection,No):
        if No =='':
            return 
        else:
            try:
                self.DataBase.collection(TargetCollection).document(No).delete()
                print('[database-INFO] 刪除請求成功')
            except:
                print('[database-ERROR] 刪除請求失敗')
            return 
    
    def HandleUpdateDatabase(self,Type,TargetCollection):
        if Type=='CU':
            if TargetCollection=='TravelInfo':
                No=flask.request.values.get('No')
                Title=flask.request.values.get('Title')
                ImageName=flask.request.values.get('ImageName')
                Content=flask.request.values.get('Content')
                StartTime=flask.request.values.get('StartTime')
                EndTime=flask.request.values.get('EndTime')
                Limit=flask.request.values.get('Limit')
                self.CreateUpdate(TargetCollection,No,Title,ImageName,Content,StartTime,EndTime,Limit)
        elif Type=='D':
            if TargetCollection=='TravelInfo':
                No=flask.request.values.get('No')
                self.Delete(TargetCollection,No)
        return

        