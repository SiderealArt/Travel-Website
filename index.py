# pipreqs . --encoding=utf8 --force
import module as module

import flask
# Init flask
App=flask.Flask(__name__)
App.config['JSON_AS_ASCII'] = False

# Init Firebase
FireBase=module.database.DB()
Admin=module.admin.Admin(FireBase)
Client=module.client.client(FireBase)

@App.template_global()
def LoginAuth():
    return Client.LoginAuth()


@App.route('/')
def Home():
    return flask.render_template('home.html')

@App.route('/Info')
@App.route('/Info/')
def RE_0():
    return flask.redirect('/Info/0')

@App.route('/Info/<No>')
def Info(No):
    Data=module.tool.FindData(FireBase.InfoData,No)
    return flask.render_template('Info.html',Title=Data['Title'],ImageUrl=Data['ImageUrl'],Content=Data['Content'],EventTime=Data['EventTime'],Quota=Data['Quota'],Price=Data['Price'],No=No,ShortContent=Data['ShortContent'])

@App.route('/login',methods=['GET','POST'])
def Clientlogin():
    if not Client.LoginAuth():
        if flask.request.method=='POST':
            Flag,Cookie=Client.HandleLogin()
            if Flag:
                return Cookie
        return flask.render_template('login.html')
    else:
        return flask.redirect('/')

@App.route('/ticket',methods=['GET','POST'])
def ticket():
    if flask.request.method=='POST':
        module.ticket.HandleTicketApply(FireBase)
        return flask.redirect('/')
    if not Client.LoginAuth():
        return flask.redirect('/login')
    else:
        return flask.render_template('ticket.html')

@App.route('/member',methods=['GET','POST'])
def member():
    return flask.render_template('member.html')


@App.route('/logout')
def Clientlogout():
    Flag,Cookie=Client.HandleLogout()
    if Flag:
        return Cookie
    else:
        return flask.redirect('/login')

@App.route('/register',methods=['GET','POST'])
def ClientRegister():
    if flask.request.method=='POST':
        Flag,flash=Client.HandleRegist()
        if Flag:
            return flask.redirect('/login')
    return flask.render_template('register.html')

@App.route('/api/TravelInfo')
def TravelInfo():
    #FireBase.HandleApiDataUpdate() #若使用 會犧牲載入速度
    return flask.jsonify(FireBase.InfoData)
    
@App.route('/api/MemberTicket')
def MemberTicket():
    if not Client.LoginAuth():
        return flask.redirect('/login')
    else:
        return flask.jsonify(module.ticket.HandleTicketApi(FireBase,flask.request.cookies.get('UserLoginAccount')))

@App.route('/op')
@App.route('/op/')
def Dashboard():
    if Admin.LoginAuth():
        return flask.render_template('Dashboard.html')
    else:
        return flask.redirect('/op/login')


@App.route('/op/login',methods=['GET','POST'])
def AdminLogin():
    if Admin.LoginAuth():
        return flask.redirect('/op')
    else:
        if flask.request.method=='POST':
            Flag,Cookie=Admin.HandleAdminLogin()
            if not Flag:
                return flask.render_template('Adminlogin.html',ERROR='管理員帳號或密碼錯誤')
            else:
                return Cookie
    return flask.render_template('Adminlogin.html')

@App.route('/op/Info',methods=['GET','POST'])
def CUDInfo():
    if Admin.LoginAuth():
        if flask.request.method=='POST':
            if flask.request.values.get('ActionType')=='CU':
                FireBase.HandleUpdateDatabase('CU','TravelInfo')
            elif flask.request.values.get('ActionType')=='D':
                FireBase.HandleUpdateDatabase('D','TravelInfo')
        return flask.render_template('CUDInfo.html')
    else:
        return flask.redirect('/op/login')

@App.route('/op/logout')
def AdminLogout():
    Flag,Cookie=Admin.HandleAdminLogout()
    if Flag:
        return Cookie
    else:
        return flask.redirect('/op/login')


App.secret_key=module.tool.GetConfigData('Flask','SecretKey')
if __name__ == '__main__':
    App.run(host='127.0.0.1',port=8000,debug=True)