import hashlib
import datetime

import flask

try:
    import database 
except ModuleNotFoundError:
    import module.database as database

class Admin:

    __slots__=('FireBase','HashModel','Session')

    def __init__(self,Database:database.DB)->None:
        self.FireBase=Database
        self.HashModel=hashlib.sha256()
        #清除Session
        self.Session=list()
    
    def SessionUpdateDelete(self,Type,Account,Token=None,LoginTime=None):
        if Type=='update':
            self.Session.append({'Account':Account,'Token':Token,'LoginTime':LoginTime})
        elif Type=='delete':
            for Data in self.Session:
                if Data['Account']==Account:
                    self.Session.remove(Data)
        return

    def HandleAdminLogin(self):
        
        '''流程
        
        管理員登入後會回傳auth到cookie，1小時內使用該auth都可以正常使用
        判斷30分鐘內使用者有沒有登出，沒登出的話1小時後那個auth將無法使用
        及要求重新登入

        '''
        UserName=flask.request.values.get('account')
        Password=flask.request.values.get('password')
        for Account in self.FireBase.DataBase.collection('AdminAccount').get():
            if Account.id==UserName:
                self.HashModel.update(Password.encode('utf-8'))
                if self.HashModel.hexdigest()==self.FireBase.DataBase.collection('AdminAccount').document(Account.id).get().to_dict()['Password']:
                    #成功登入
                    self.HashModel=hashlib.sha256()
                    LoginTime=datetime.datetime.now()
                    self.HashModel.update((LoginTime.strftime('%Y/%m/%d-%H:%M:%S')+UserName).encode('utf-8'))
                    Token=self.HashModel.hexdigest()
                    self.SessionUpdateDelete('update',UserName,Token,LoginTime.strftime('%Y/%m/%d-%H:%M:%S'))
                    self.HashModel=hashlib.sha256()
                    Cookie=flask.make_response(flask.redirect('/op'))
                    Cookie.set_cookie(key='LoginAccount',value=UserName,expires=LoginTime+datetime.timedelta(hours=1))
                    Cookie.set_cookie(key='Token',value=Token,expires=LoginTime+datetime.timedelta(hours=1))
                    return True,Cookie
        return False,''
    

    def LoginAuth(self):
        LoginAccount=flask.request.cookies.get('LoginAccount')
        for SessionData in self.Session:
            if SessionData['Account']==LoginAccount:
                if flask.request.cookies.get('Token')==SessionData['Token']:
                    if datetime.datetime.now()-datetime.datetime.strptime(SessionData['LoginTime'],'%Y/%m/%d-%H:%M:%S')<=datetime.timedelta(hours=1): # 超過生存時間
                        return True
                    else:
                        self.HandleReLogin()
        return False
    

    def HandleAdminRegist(self,Key,Username,Password):
        if Key!=self.FireBase.DataBase.collection('Secret').document('AdminRegistKey').get().to_dict()['Key']:
            return
        else:
            self.HashModel.update(Password.encode('utf-8'))
            self.FireBase.CreateUpdate('AdminAccount',Username,self.HashModel.hexdigest())
            self.HashModel=hashlib.sha256()
        return
    
    
    def HandleAdminLogout(self):
        if self.LoginAuth():
            UserName=flask.request.cookies.get('LoginAccout')
            self.SessionUpdateDelete('delete',Account=UserName)
            Cookie=flask.make_response(flask.redirect('/op/login'))
            Cookie.delete_cookie('LoginAccount')
            Cookie.delete_cookie('Token')
            return True,Cookie
        return False,''

    def HandleReLogin(self):
        UserName=flask.request.cookies.get('LoginAccout')
        Cookie=flask.make_response(flask.redirect('/op/login'))
        Cookie.delete_cookie('LoginAccount')
        Cookie.delete_cookie('Token')
        self.SessionUpdateDelete('delete',Account=UserName)
        return

if __name__=='__main__':
    Test=Admin(database.DB())
    key=input('Key:')
    username=input('Username:')
    password=input('password:')
    Test.HandleAdminRegist(key,username,password)    
