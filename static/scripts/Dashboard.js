var DataBase;

$.get('../api/TravelInfo',function (Data){
    var i=0;
    DataBase=Data;
    while (Data[i]!=undefined){
        RowData=Data[i];
        $("#InfoTable tbody").append('<tr><td>'+RowData['No']+'</td><td>'+RowData['Title']+'</td><td>'+RowData['EventTime']+'</td><td>'+RowData['Quota']+'</td><td><button class="btn btn-warning"><a href="/Info/'+RowData['No']+'">連結</a></button></td>')
        i++;
    }
});

function Edit(i){
    $('#No').attr('value',DataBase[i]['No']);
    $('#Title').attr('value',DataBase[i]['Title']);
    $('#ShortContent').val(DataBase[i]['ShortContent']).change()
    $('#Content').val(DataBase[i]['Content']).change();
    $('#EventTime').attr('value',DataBase[i]['EventTime']);
    $("#Type").val(DataBase[i]['Type']).change();
    $('#Quota').attr('value',DataBase[i]['Quota']);
    $('#Price').attr('value',DataBase[i]['Price']);
}