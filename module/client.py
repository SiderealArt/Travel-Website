import hashlib
import datetime

import flask
try:
    import database 
except ModuleNotFoundError:
    import module.database as database

class client:

    __slots__=('FireBase','HashModel','ClientAccount','Session')

    def __init__(self,Database:database.DB) -> None:
        self.FireBase=Database
        self.HashModel=hashlib.sha256()
        self.AccountListGet()
        #清除Session
        self.Session=list()

    def AccountListGet(self):
        self.ClientAccount=list()
        for Doc in self.FireBase.DataBase.collection('ClientAccount').get():
            Data=self.FireBase.DataBase.collection('ClientAccount').document(Doc.id).get().to_dict()
            self.ClientAccount.append({**Data,**{'Username':Doc.id}}) #username 加入dict
        return

    def SessionUpdateDelete(self,Type,Account,Token=None,LoginTime=None):
        if Type=='update':
            self.Session.append({'Account':Account,'Token':Token,'LoginTime':LoginTime})
        elif Type=='delete':
            for Data in self.Session:
                if Data['Account']==Account:
                    self.Session.remove(Data)
        return

    def HandleRegist(self):
        Username=flask.request.values.get('username')
        Password=flask.request.values.get('password')
        Check=flask.request.values.get('check')
        if Check!=Password:
           return False,flask.flash('密碼不一致')  # 確認密碼錯誤
        for Acc in self.ClientAccount:
            if Acc['Username']==Username: # 重複註冊
                print(f'[ClientReg-ERROR] {Username}已存在')
                return False,flask.flash('帳號已存在')
        self.HashModel.update(Password.encode('utf-8'))
        self.FireBase.DataBase.collection('ClientAccount').document(Username).set({
            'Password':self.HashModel.hexdigest()
        })
        self.ClientAccount.append({'Username':Username,'Password':self.HashModel.hexdigest()})
        self.HashModel=hashlib.sha256()
        self.AccountListGet()
        return True,flask.flash('申請帳號成功。請重新登入')
    
    def HandleLogin(self):
        UserName=flask.request.values.get('username')
        Password=flask.request.values.get('password')
        for Account in self.ClientAccount:
            if Account['Username']==UserName:
                self.HashModel.update(Password.encode('utf-8'))
                if self.HashModel.hexdigest()==Account['Password']:
                    #成功登入
                    self.HashModel=hashlib.sha256()
                    LoginTime=datetime.datetime.now()
                    self.HashModel.update((LoginTime.strftime('%Y/%m/%d-%H:%M:%S')+UserName).encode('utf-8'))
                    Token=self.HashModel.hexdigest()
                    self.SessionUpdateDelete('update',UserName,Token,LoginTime.strftime('%Y/%m/%d-%H:%M:%S'))
                    self.HashModel=hashlib.sha256()
                    Cookie=flask.make_response(flask.redirect('/'))
                    Cookie.set_cookie(key='UserLoginAccount',value=UserName,expires=LoginTime+datetime.timedelta(hours=1))
                    Cookie.set_cookie(key='Token',value=Token,expires=LoginTime+datetime.timedelta(hours=1))
                    return True,Cookie
        return False,''
    
    def LoginAuth(self):
        LoginAccount=flask.request.cookies.get('UserLoginAccount')
        for Account in self.Session:
            if Account['Account']==LoginAccount:
                if flask.request.cookies.get('Token')==Account['Token']:
                    if datetime.datetime.now()-datetime.datetime.strptime(Account['LoginTime'],'%Y/%m/%d-%H:%M:%S')<=datetime.timedelta(hours=1): # 超過生存時間
                        return True
                    else:
                        self.HandleReLogin()
        return False
    
    def HandleReLogin(self):
        UserName=flask.request.cookies.get('UserLoginAccount')
        Cookie=flask.make_response(flask.redirect('/login'))
        Cookie.delete_cookie('UserLoginAccount')
        Cookie.delete_cookie('Token')
        self.FireBase.DataBase.collection('Session-Client').document(UserName).delete()
        return

    def HandleLogout(self):
        if self.LoginAuth():
            self.SessionUpdateDelete('delete',Account=flask.request.cookies.get('UserLoginAccount'))
            Cookie=flask.make_response(flask.redirect('/'))
            Cookie.delete_cookie('UserLoginAccount')
            Cookie.delete_cookie('Token')
            return True,Cookie
        return False,''

    def HandleTicket(self):
        pass


