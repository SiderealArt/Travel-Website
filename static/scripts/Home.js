$.get('/api/TravelInfo', function (Data) {
    console.log(Data);
    var Flag = [0, 0, 0, 0, 0, 0, 0, 0]
    var i = 0;
    while (Data[i] != undefined) {
        var RowData = Data[i];
        if (Flag[Number(RowData['Type'])] == 0) {
            $('#carousel' + RowData['Type'] + ' .carousel-inner').append('<div class="carousel-item active"><img src="' + RowData['ImageUrl'] + '" class="d-block w-100"><div class="carousel-caption d-none d-md-block">' + RowData['ShortContent'] + '<a class="btn btn-success" role="button" href="/Info/' + RowData['No'] + '">查看更多</a></div>');
        } else {
            $("#carousel" + RowData['Type'] + " .carousel-indicators").append('<button type="button" data-bs-target="#carousel' + RowData['Type'] + '" data-bs-slide-to="' + Flag[Number(RowData['Type'])] + '" aria-label="Slide ' + Flag[Number(RowData['Type'])] + '"></button>');
            $("#carousel" + RowData['Type'] + " .carousel-inner").append('<div class="carousel-item"><img src="' + RowData['ImageUrl'] + '" class="d-block w-100"><div class="carousel-caption d-none d-md-block">' + RowData['ShortContent'] + '<a class="btn btn-success" role="button" href="/Info/' + RowData['No'] + '">查看更多</a></div>')
        }
        Flag[Number(RowData['Type'])] = Flag[Number(RowData['Type'])] + 1;
        i++;
    }
    for (var j = 0; j < 3; j++) {
        console.log(j);
        var RowData = Data[j];
        $("#carouselExampleControls" + " .carousel-indicators").append('<button type="button" data-bs-target="#carouselExampleControls' + '" data-bs-slide-to="' + j + '" aria-label="Slide ' + j + '"></button>');
        $('#carouselExampleControls'+' .carousel-inner').append('<div class="carousel-item"><img src="' + RowData['ImageUrl'] + '" class="d-block w-100 object-cover"><div class="carousel-caption d-none d-md-block bottom-36">' +'<h3 class="text-5xl drop-shadow-2xl font-bold">'+ RowData['Title'] + '</h3><p class="text-2xl font-bold">只需 '+RowData['Price']+' 起</p>');
        
    }
    document.querySelector('#carouselExampleControls > div.carousel-inner > div:nth-child(1)').classList.add("active"); 
    document.querySelector('#carouselExampleControls > div.carousel-indicators > button:nth-child(1)').classList.add("active"); 
});