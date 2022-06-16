$.get('../api/TravelInfo',function (Data){
    var i=0;
    while (Data[i]!=undefined){
        var RowData=Data[i];
        RowData['No'];//編號
        RowData['Title'];//名稱
    }
});

$.get('../api/MemberTicket',function (Data){
    var i=0;
    while (Data[i]!=undefined){
        RowData=Data[i];
        $("#InfoTable tbody").append('<tr><td>'+RowData['TravelInfo']+'</td><td>'+RowData['People']+'</td></tr>')
        i++;
    }
});