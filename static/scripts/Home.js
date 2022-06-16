$.get('/api/TravelInfo',function (Data){
    var Flag=[0,0,0,0,0,0,0,0]
    var i=0;
    while(Data[i]!=undefined){
        var RowData=Data[i];
        if(Flag[Number(RowData['Type'])]==0){
            $('#carousel'+RowData['Type']+' .carousel-inner').append('<div class="carousel-item active"><img src="'+RowData['ImageUrl']+'" class="d-block w-100"><div class="carousel-caption d-none d-md-block">'+RowData['ShortContent']+'<a href="/Info/'+RowData['No']+'">查看更多</a></div>');
        }else{
            $("#carousel"+RowData['Type']+" .carousel-indicators").append('<button type="button" data-bs-target="#carousel'+RowData['Type']+'" data-bs-slide-to="'+Flag[Number(RowData['Type'])]+'" aria-label="Slide '+Flag[Number(RowData['Type'])]+'"></button>');
            $("#carousel"+RowData['Type']+" .carousel-inner").append('<div class="carousel-item"><img src="'+RowData['ImageUrl']+'" class="d-block w-100"><div class="carousel-caption d-none d-md-block">'+RowData['ShortContent']+'<a href="/Info/'+RowData['No']+'">查看更多</a></div>')
        }
        Flag[Number(RowData['Type'])]++;
        i++;
    }
    
});