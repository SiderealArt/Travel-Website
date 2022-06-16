$.get('../api/TravelInfo',function (Data){
    var i=0;
    while (Data[i]!=undefined){
        $("#TravelInfo").append('<option value="'+Data[i]['No']+'">'+Data[i]['Title']+'</option>')
        i++;
    }
});