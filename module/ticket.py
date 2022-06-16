import flask


try:
    import database
except ModuleNotFoundError:
    import module.database as database

def HandleTicketApply(DataBase:database.DB):
    username=flask.request.cookies.get('UserLoginAccount')
    name=flask.request.values.get('name')
    enname=flask.request.values.get('enname')
    birthday=flask.request.values.get('birthday')
    cellphone=flask.request.values.get('cellphone')
    email=flask.request.values.get('email')
    TravelInfo=flask.request.values.get('TravelInfo')
    People=flask.request.values.get('people')
    DataBase.CreateUpdate('Ticket',Data1=username,Data2=name,Data3=enname,Data4=birthday,Data5=cellphone,Data6=email,Data7=TravelInfo,Data8=People)
    Data=DataBase.DataBase.collection('TravelInfo').document(TravelInfo).get().to_dict()
    DataBase.DataBase.collection('TravelInfo').document(TravelInfo).update({
        'Quota':str(int(Data['Quota'])-int(People))
    })
    return 

def HandleTicketApi(DataBase:database.DB,Username):
    Resp=list()
    for Doc in DataBase.DataBase.collection('Ticket').get():
        Data=DataBase.DataBase.collection('Ticket').document(Doc.id).get().to_dict()
        if Data['username']==Username:
            Resp.append(Data)
    return Resp