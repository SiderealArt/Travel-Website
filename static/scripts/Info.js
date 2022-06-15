var DataBase;

$.get('../api/TravelInfo',function (Data){
    var i=0;
    DataBase=Data;
    while (Data[i]!=undefined){
        RowData=Data[i];
        $(".InfoTable tbody").append('<tr><td>'+RowData['No']+'</td><td>'+RowData['Title']+'</td><td>'+RowData['EventTime']+'</td><td>'+RowData['Quota']+'</td><td><a href="../Info/'+RowData['No']+'">連結</a></td><td><button onclick="Edit('+i+')">點我編輯</button></td></tr>')
        i++;
    }
});

function Edit(i){
    $('#Content').val('');
    $('#No').attr('value',DataBase[i]['No']);
    $('#Title').attr('value',DataBase[i]['Title']);
    $('#Content').val(DataBase[i]['Content']);
    $('#EventTime').attr('value',DataBase[i]['EventTime']);
    $('#Quota').attr('value',DataBase[i]['Quota']);
    $('#Price').attr('value',DataBase[i]['Price']);
}