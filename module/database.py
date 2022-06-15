import firebase_admin as firebase
from firebase_admin import firestore,storage
import os
import flask

try:
    import tool as tool
except ModuleNotFoundError:
    import module.tool as tool

class DB:

    __slots__=('DataBase','Datalist','Storage')

    def __init__(self)->None:

        self.Datalist=list()
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
        
        self.Storage=storage.bucket()


    def CreateUpdate(self,TargetCollection,DocumentName,Data1,Data2=None,Data3=None,Data4=None,Data5=None,Data6=None):
        if self.DataBase=='':
            print('[database-ERROR] 你尚未登入')
            return
        else:
            if TargetCollection=='TravelInfo':
                Data={
                    'No':DocumentName,
                    'Title':Data1, # str
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
            for Docs in self.DataBase.collection(TargetCollection).get():
                if Docs.id==DocumentName:
                    if self.DataBase.collection(TargetCollection).document(DocumentName).get().to_dict()['Title']!=Data1:
                        print('[database-ERROR] ID衝突')
                        return
                    else: #同ID 同Title->更新
                        self.DataBase.collection(TargetCollection).document(DocumentName).update(Data)
                        print('[database-INFO] 更新完成')
                        return
            self.DataBase.collection(TargetCollection).document(DocumentName).set(Data)
            print('[database-INFO] 新增完成')
            return


    def Search(self,TargetCollection)->list:
        '''
        Search用於document名稱無意義時使用
        '''
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
                Content=flask.request.values.get('Content')
                EventTime=flask.request.values.get('EventTime')
                Quota=flask.request.values.get('Quota')
                Price=flask.request.values.get('Price')
                self.CreateUpdate(TargetCollection,No,Title,self.HandleUploadFile(),Content,EventTime,Quota,Price)
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

        