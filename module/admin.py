import hashlib
import datetime

import flask

try:
    import database 
except ModuleNotFoundError:
    import module.database as database

class Admin:

    __slots__=('FireBase','Account','HashModel')

    def __init__(self,Database:database.DB)->None:
        self.FireBase=Database
        self.HashModel=hashlib.sha256()
        #清除Session
        for Doc in self.FireBase.DataBase.collection('Session-Admin').get():
            self.FireBase.DataBase.collection('Session-Admin').document(Doc.id).delete()

    def HandleAdminLogin(self):
        
        '''流程
        
        管理員登入後會回傳auth到cookie，30分鐘內使用該auth都可以正常使用
        判斷30分鐘內使用者有沒有登出，沒登出的話30分鐘後那個auth將無法使用
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
                    self.FireBase.DataBase.collection('Session-Admin').document(UserName).set({
                        'Token':Token,
                        'LoginTime':LoginTime.strftime('%Y/%m/%d-%H:%M:%S')
                    })
                    self.HashModel=hashlib.sha256()
                    Cookie=flask.make_response(flask.redirect('/op'))
                    Cookie.set_cookie(key='LoginAccount',value=UserName,expires=LoginTime+datetime.timedelta(hours=1))
                    Cookie.set_cookie(key='Token',value=Token,expires=LoginTime+datetime.timedelta(hours=1))
                    return True,Cookie
        return False,''
    

    def LoginAuth(self):
        LoginAccount=flask.request.cookies.get('LoginAccount')
        for SessionAccount in self.FireBase.DataBase.collection('Session-Admin').get():
            if SessionAccount.id==LoginAccount:
                Session=self.FireBase.DataBase.collection('Session-Admin').document(SessionAccount.id).get().to_dict()
                if flask.request.cookies.get('Token')==Session['Token']:
                    if datetime.datetime.now()-datetime.datetime.strptime(Session['LoginTime'],'%Y/%m/%d-%H:%M:%S')<=datetime.timedelta(hours=1):
                        return True
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
            self.FireBase.DataBase.collection('Session-Admin').document(flask.request.cookies.get('LoginAccount')).delete()
            Cookie=flask.make_response(flask.redirect('/op/login'))
            Cookie.delete_cookie('LoginAccount')
            Cookie.delete_cookie('Token')
            return True,Cookie
        return False,''


if __name__=='__main__':
    Test=Admin(database.DB())
    key=input('Key:')
    username=input('Username:')
    password=input('password:')
    Test.HandleAdminRegist(key,username,password)    
