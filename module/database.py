import firebase_admin as firebase
from firebase_admin import firestore,storage
import os
import flask

try:
    import tool as tool
except ModuleNotFoundError:
    import module.tool as tool

class DB:

    __slots__=('DataBase','InfoData','Storage')

    def __init__(self)->None:

        self.InfoData=list()
        # 登入Firebase
        try:
            Cred=firebase.credentials.Certificate(tool.GetConfigData('Firebase','JsonFilePath'))
            firebase.initialize_app(Cred,{
                'storageBucket':tool.GetConfigData('Firebase','StorageUrl')
            })
            # 使用Firebase的firestore
            self.DataBase=firestore.client()
        except:
            print('[database-ERROR] 登入Firebase失敗，請檢查config.ini key設定路徑')
            self.DataBase=''
        self.HandleApiDataUpdate('TravelInfo')
        self.Storage=storage.bucket()


    def CreateUpdate(self,TargetCollection,DocumentName=None,Data1=None,Data2=None,Data3=None,Data4=None,Data5=None,Data6=None,Data7=None,Data8=None,Data9=None):
        if self.DataBase=='':
            print('[database-ERROR] 你尚未登入')
            return
        else:
            if TargetCollection=='TravelInfo':
                Data={
                    'No':DocumentName,
                    'Title':Data1, # str
                    'Type':Data7,
                    'ShortContent':Data8,
                    'ImageUrl':Data2, # str
                    'Content':Data3, # str
                    'EventTime':Data4, # str 
                    'Quota':Data5, # str
                    'Price':Data6
                }
            elif TargetCollection=='AdminAccount':
                Data={
                    'Password':Data1,
                }
            elif TargetCollection=='ClientAccount':
                Data={
                    'Password':Data1,
                }
            elif TargetCollection=='Ticket':
                Data={
                    'username':Data1,
                    'name':Data2,
                    'enname':Data3,
                    'birthday':Data4,
                    'cellphone':Data5,
                    'email':Data6,
                    'TravelInfo':Data7,
                    'People':Data8,
                    'UserID':Data9
                }
            for Docs in self.DataBase.collection(TargetCollection).get():
                if Docs.id==DocumentName:
                    if self.DataBase.collection(TargetCollection).document(DocumentName).get().to_dict()['Title']!=Data1:
                        print('[database-ERROR] ID衝突')
                        return
                    else: #同ID 同Title->更新
                        self.DataBase.collection(TargetCollection).document(DocumentName).update(Data)
                        self.HandleApiDataUpdate(TargetCollection)
                        print('[database-INFO] 更新完成')
                        return

            self.DataBase.collection(TargetCollection).document(DocumentName).set(Data)
            self.InfoData.append(Data)
            print('[database-INFO] 新增完成')
            return


    def HandleApiDataUpdate(self,TargetCollection):
        if self.DataBase=='':
            print('[database-ERROR] 你尚未登入')
            return
        else:
            self.InfoData=list()
            for Doc in self.DataBase.collection(TargetCollection).get():
                Data=self.DataBase.collection(TargetCollection).document(Doc.id).get().to_dict()
                # print(f'{Doc.id} {Data}')
                self.InfoData.append(Data)
            return 
    
    def Delete(self,TargetCollection,No):
        if No =='':
            return 
        else:
            try:
                self.DataBase.collection(TargetCollection).document(No).delete()
                print('[database-INFO] 刪除請求成功')
                self.HandleApiDataUpdate(TargetCollection)
            except:
                print('[database-ERROR] 刪除請求失敗')
            return 
    
    def HandleUpdateDatabase(self,Type,TargetCollection):
        if Type=='CU':
            if TargetCollection=='TravelInfo':
                No=flask.request.values.get('No')
                Title=flask.request.values.get('Title')
                Type=flask.request.values.get('Type')
                Content=flask.request.values.get('Content')
                ShortContent=flask.request.values.get('ShortContent')
                EventTime=flask.request.values.get('EventTime')
                Quota=flask.request.values.get('Quota')
                Price=flask.request.values.get('Price')
                self.CreateUpdate(TargetCollection,No,Title,self.HandleUploadFile(),Content,EventTime,Quota,Price,Type,ShortContent)
        elif Type=='D':
            if TargetCollection=='TravelInfo':
                No=flask.request.values.get('No')
                self.Delete(TargetCollection,No)
        return
    
    def HandleUploadFile(self)->str:
        AllowFileType=set(['jpg','png'])
        if flask.request.files.get('Image'):
            File=flask.request.files['Image']
            if File.filename.split('.')[1].lower() in AllowFileType:
                TempPath=os.path.join(os.getcwd()+'/temp',File.filename)
                try:
                    os.mkdir(os.getcwd()+'/temp')
                except:
                    pass
                File.save(TempPath)
                blob=self.Storage.blob(File.filename)
                blob.upload_from_filename(TempPath)
                os.remove(TempPath)
                blob.make_public()
                return blob.public_url
            else:
                return ''
        else:
            return ''

    def HandleUserDataApi(self):
        username=flask.request.cookies.get('UserLoginAccount')
        Resp=list()
        for Doc in self.DataBase.collection('UserData').get():
            Data=self.DataBase.collection('UserData').document(Doc.id).get().to_dict()
            if Data['username']==username:
                Resp.append(Data)
        return Resp
    
    def HandleTicketApi(self):
        Username=flask.request.cookies.get('UserLoginAccount')
        Resp=list()
        for Doc in self.DataBase.collection('Ticket').get():
            Data=self.DataBase.collection('Ticket').document(Doc.id).get().to_dict()
            if Data['username']==Username:
                Resp.append(Data)
        return Resp
