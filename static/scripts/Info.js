var DataBase;

$.get('../api/TravelInfo',function (Data){
    var i=0;
    DataBase=Data;
    while (Data[i]!=undefined){
        var RowData=Data[i];
        $(".InfoTable tbody").append('<tr><td>'+RowData['No']+'</td><td>'+RowData['Title']+'</td><td>'+RowData['EventTime']+'</td><td>'+RowData['Quota']+'</td><td><a href="../Info/'+RowData['No']+'">連結</a></td><td><button onclick="Edit('+RowData['No']+')">點我編輯</button></td></tr>')
        i++;
    }
});

function Edit(i){
    var j=0;
    while (DataBase[j]['No']!=i){ //找json中第j項 編號=i
        j++;
    }
    $('#No').attr('value',i);
    $('#Title').attr('value',DataBase[j]['Title']);
    $('#ShortContent').val(DataBase[j]['ShortContent']).change()
    $('#Content').val(DataBase[j]['Content']).change();
    $('#EventTime').attr('value',DataBase[j]['EventTime']);
    $("#Type").val(DataBase[j]['Type']).change();
    $('#Quota').attr('value',DataBase[j]['Quota']);
    $('#Price').attr('value',DataBase[j]['Price']);
}