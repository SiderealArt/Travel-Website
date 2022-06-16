$.get('../api/TravelInfo',function (Data){
    var i=0;
    while (Data[i]!=undefined){
        $("#TravelInfo").append('<option value="'+Data[i]['No']+'">'+Data[i]['Title']+'</option>')
        i++;
    }
});

function InputUserData(){
    $.get('../api/UserData',function (Data){
        var i=0;
        while (Data[i]!=undefined){
            var RowData=Data[i];
            $('#name').attr('value',RowData['name']);
            $('#enname').attr('value',RowData['enname']);
            $('#birthday').attr('value',RowData['birthday'])
            $('#UserID').attr('value',RowData['UserID'])
            $('#cellphone').attr('value',RowData['cellphone'])
            $('#email').attr('value',RowData['email'])
            i++;
        }
    });
}